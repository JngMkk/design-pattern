from typing import Iterable, Iterator, cast


class NMEAState:
    def __init__(self, message: "Message") -> None:
        self.message = message

    def feed_byte(self, _input: int) -> "NMEAState":
        return self

    def valid(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message})"


class Message:
    def __init__(self) -> None:
        self.body = bytearray(80)
        self.checksum = bytearray(2)
        self.body_len = 0
        self.checksum_len = 0
        self.checksum_computed = 0

    def reset(self) -> None:
        self.body_len = 0
        self.checksum_len = 0
        self.checksum_computed = 0

    def body_append(self, _input: int) -> int:
        self.body[self.body_len] = _input
        self.body_len += 1
        self.checksum_computed ^= _input

        return self.body_len

    def checksum_append(self, _input: int) -> int:
        self.checksum[self.checksum_len] = _input
        self.checksum_len += 1

        return self.checksum_len

    @property
    def valid(self) -> bool:
        return self.checksum_len == 2 and int(self.checksum, 16) == self.checksum_computed

    def __repr__(self) -> str:
        body_str = self.body[: self.body_len].decode(errors="replace")
        checksum_str = self.checksum.decode(errors="replace")
        checksum_computed_str = f"{self.checksum_computed:02X}"
        return f"Message(body=bytearray(b'{body_str}'), checksum=bytearray(b'{checksum_str}'), computed={checksum_computed_str})"


class Reader:
    def __init__(self) -> None:
        self.buffer = Message()
        self.state: NMEAState = Waiting(self.buffer)

    def read(self, source: Iterable[bytes]) -> Iterator[Message]:
        for byte in source:
            self.state = self.state.feed_byte(cast(int, byte))
            if self.buffer.valid:
                yield self.buffer
                self.buffer = Message()
                self.state = Waiting(self.buffer)


class Waiting(NMEAState):
    def feed_byte(self, _input: int) -> NMEAState:
        if _input == ord(b"$"):
            return Header(self.message)

        return self


class Header(NMEAState):
    def __init__(self, message: Message) -> None:
        super().__init__(message)
        self.message.reset()

    def feed_byte(self, _input: int) -> NMEAState:
        if _input == ord(b"$"):
            return Header(self.message)

        size = self.message.body_append(_input)
        if size == 5:
            return Body(self.message)

        return self


class Body(NMEAState):
    def feed_byte(self, _input: int) -> NMEAState:
        if _input == ord(b"$"):
            return Header(self.message)

        if _input == ord(b"*"):
            return Checksum(self.message)
        self.message.body_append(_input)

        return self


class Checksum(NMEAState):
    def feed_byte(self, _input: int) -> NMEAState:
        if _input == ord(b"$"):
            return Header(self.message)

        if _input in {ord(b"\n"), ord(b"\r")}:
            return End(self.message)

        size = self.message.checksum_append(_input)
        if size == 2:
            return End(self.message)

        return self


class End(NMEAState):
    def feed_byte(self, _input: int) -> NMEAState:
        if _input == ord(b"$"):
            return Header(self.message)

        elif _input not in {ord(b"\n"), ord(b"\r")}:
            return Waiting(self.message)

        return self

    def valid(self) -> bool:
        return self.message.valid


if __name__ == "__main__":
    message = b"""
$GPGGA,161229.487,3723.2475,N,12158.3416,W,1,07,1.0,9.0,M,,,,0000*18
$GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A*41
"""

    reader = Reader()
    for result in reader.read(message):
        print(result)

"""
Message(body=bytearray(b'GPGGA,161229.487,3723.2475,N,12158.3416,W,1,07,1.0,9.0,M,,,,0000'), checksum=bytearray(b'18'), computed=18)
Message(body=bytearray(b'GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A'), checksum=bytearray(b'41'), computed=41)
"""
