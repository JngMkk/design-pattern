import weakref
from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import floor, radians
from typing import Iterator, Sequence

from typing_extensions import overload


@dataclass(frozen=True)
class Point:
    latitude: float
    longitude: float

    @classmethod
    def from_bytes(
        cls,
        latitude: bytes,
        N_S: bytes,
        longitude: bytes,
        E_W: bytes,
    ) -> "Point":
        lat_deg = float(latitude[:2]) + float(latitude[2:]) / 60
        lat_sign = 1 if N_S.upper() == b"N" else -1
        lon_deg = float(longitude[:3]) + float(longitude[3:]) / 60
        lon_sign = 1 if E_W.upper() == b"E" else -1
        return Point(lat_deg * lat_sign, lon_deg * lon_sign)

    def __str__(self) -> str:
        lat = abs(self.latitude)
        lat_deg = floor(lat)
        lat_min_sec = 60 * (lat - lat_deg)
        lat_dir = "N" if self.latitude > 0 else "S"
        lon = abs(self.longitude)
        lon_deg = floor(lon)
        lon_min_sec = 60 * (lon - lon_deg)
        lon_dir = "E" if self.longitude > 0 else "W"
        return (
            f"({lat_deg:02.0f}°{lat_min_sec:07.4f}{lat_dir}, "
            f"{lon_deg:03.0f}°{lon_min_sec:07.4f}{lon_dir})"
        )

    @property
    def lat(self) -> float:
        return radians(self.latitude)

    @property
    def lon(self) -> float:
        return radians(self.longitude)


class Buffer(Sequence[int]):
    def __init__(self, content: bytes) -> None:
        self.content = content

    def __len__(self) -> int:
        return len(self.content)

    def __iter__(self) -> Iterator[int]:
        return iter(self.content)

    @overload
    def __getitem__(self, idx: int) -> int: ...  # noqa

    @overload
    def __getitem__(self, idx: slice) -> bytes: ...  # noqa

    def __getitem__(self, idx: int | slice) -> int | bytes:
        return self.content[idx]


class Message(ABC):
    def __init__(self) -> None:
        self.buffer: weakref.ReferenceType[Buffer]
        self.offset: int
        self.end: int | None
        self.commas: list[int]

    def from_buffer(self, buffer: Buffer, offset: int) -> "Message":
        # Buffer 객체가 사용되는 위치를 추적하기 위해 사용되지 않으므로 Message 객체가 여전히 신선하지 않은 참조를 갖고 있는 경우에도 Buffer 객체를 제거할 수 있게 해줌.
        self.buffer = weakref.ref(buffer)
        self.offset = offset
        self.end = None
        self.commas = [offset]

        for idx in range(offset, offset + 82):
            if buffer[idx] == ord(b","):
                self.commas.append(idx)
            elif buffer[idx] == ord(b"*"):
                self.commas.append(idx)
                self.end = idx + 3
                break

        if self.end is None:
            raise ValueError("Incomplete message")

        return self

    def __getitem__(self, field: int) -> bytes:
        if not hasattr(self, "buffer") or (buffer := self.buffer()) is None:
            raise RuntimeError("Broken reference")

        start, end = self.commas[field] + 1, self.commas[field + 1]
        return buffer[start:end]

    def get_fix(self) -> Point:
        return Point.from_bytes(self.latitude(), self.lat_n_s(), self.longitude(), self.lon_e_w())

    @abstractmethod
    def latitude(self) -> bytes: ...  # noqa

    @abstractmethod
    def lat_n_s(self) -> bytes: ...  # noqa

    @abstractmethod
    def longitude(self) -> bytes: ...  # noqa

    @abstractmethod
    def lon_e_w(self) -> bytes: ...  # noqa


class GPGLL(Message):
    """
    __getitem__ 메서드를 통해 전체 바이트 시퀀스에서 네 개의 특정 필드에 대한 바이트를 선택함.
    __getitem__ 메서드는 Buffer 객체에 대한 참조를 사용하기 때문에 전체 메시지의 바이트 시퀀스를 복제할 필요가 없음.
    대신 Buffer 객체에 다시 접근해 데이터를 가져오기 때문에 메모리를 복잡하게 만드는 것을 방지함.
    """

    def latitude(self) -> bytes:
        return self[1]

    def lat_n_s(self) -> bytes:
        return self[2]

    def longitude(self) -> bytes:
        return self[3]

    def lon_e_w(self) -> bytes:
        return self[4]


def message_factory(header: bytes) -> Message | None:
    if header == b"GPGLL":
        return GPGLL()
    return None


if __name__ == "__main__":
    buffer = Buffer(b"$GPGLL,3751.65,S,14507.36,E*77")
    flyweight = message_factory(buffer[1:6])
    flyweight.from_buffer(buffer, 0)

    print(flyweight.get_fix())
    # (37°51.6500S, 145°07.3600E)

    buffer_2 = Buffer(
        b"$GPGLL,3751.65,S,14507.36,E*77\\r\\n"
        b"$GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A*41\\r\\n"
    )
    start = 0
    flyweight = message_factory(buffer_2[start + 1 : start + 6])  # noqa
    p_1 = flyweight.from_buffer(buffer_2, start).get_fix()
    print(p_1)
    # (37°51.6500S, 145°07.3600E)

    print(flyweight.end)
    # 30
    next_start = buffer_2.index(ord(b"$"), flyweight.end)
    print(next_start)
    # 34

    p_2 = flyweight.from_buffer(buffer_2, next_start).get_fix()
    print(p_2)
    # (37°23.2475N, 121°58.3416W)
