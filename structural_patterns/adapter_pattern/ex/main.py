class TimeSince:
    """시간은 구두점 없이 6자리여야 함"""

    def __init__(self, starting_time: str) -> None:
        self.hr, self.min, self.sec = self.parse_time(starting_time)
        self.start_seconds = ((self.hr * 60) + self.min) * 60 + self.sec

    def parse_time(self, time: str) -> tuple[float, float, float]:
        return float(time[0:2]), float(time[2:4]), float(time[4:])

    def interval(self, log_time: str) -> float:
        log_hr, log_min, log_sec = self.parse_time(log_time)
        log_seconds = ((log_hr * 60) + log_min) * 60 + log_sec

        return log_seconds - self.start_seconds


class LogProcessor:
    def __init__(self, log_entries: list[tuple[str, str, str]]) -> None:
        self.log_entries = log_entries
        self.time_convert = IntervalAdapter()

    def report(self) -> None:
        first_time, _, _ = self.log_entries[0]
        for log_time, severity, message in self.log_entries:
            if severity == "ERROR":
                first_time = log_time

            interval = self.time_convert.time_offset(first_time, log_time)
            print(f"{interval:8.2f} | {severity:7s} | {message}")


class IntervalAdapter:
    """
    필요할 때 TimeSince 객체를 생성함. TimeSince가 없으면 새로 생성.
    기존 TimeSince 객체가 있고 이미 설정된 시작 시간을 사용하는 경우에는 TimeSince 인스턴스를 재사용할 수 있음.
    그러나 LogProcessor 클래스가 분석의 초점을 새로운 오류 메시지로 옮겼다면 새로운 TimeSince를 생성해야 함.
    """

    def __init__(self) -> None:
        self.ts: TimeSince | None = None

    def time_offset(self, start: str, now: str) -> float:
        if self.ts is None:
            self.ts = TimeSince(start)

        else:
            h_m_s = self.ts.parse_time(start)
            if h_m_s != (self.ts.hr, self.ts.min, self.ts.sec):
                self.ts = TimeSince(start)

        return self.ts.interval(now)


if __name__ == "__main__":
    ts = TimeSince("000123")
    print(ts.interval("020304"))  # 7301.0
    print(ts.interval("030405"))  # 10962.0

    data = [
        ("000123", "INFO", "System start"),
        ("010234", "INFO", "System stop"),
        ("020345", "ERROR", "Disk full"),
        ("030456", "ERROR", "System crash"),
    ]
    lp = LogProcessor(data)
    lp.report()

    """
       0.00 | INFO    | System start
    3671.00 | INFO    | System stop
       0.00 | ERROR   | Disk full
       0.00 | ERROR   | System crash
    """
