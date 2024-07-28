from math import floor, radians

"""
슬롯으로 이름 정의를 관리하는 것은 애플리케이션이 이런 객체를 대량으로 생성할 때 도움이 될 수 있음.
하지만 많은 경우에 애플리케이션은 클래스에 대해 하나 또는 매우 적은 수의 인스턴스를 빌드하기 때문에 __slots__ 도입으로 인한 메모리 절약은 무시할 수 있음.
어떤 경우에는 NamedTuple을 사용하는 것이 __slots__를 사용하는 것만큼 메모리를 절약하는 데 효과적일 수 있음.
"""


class Point:
    __slots__ = ("latitude", "longitude")

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) -> str:
        return f"Point(latitude={self.latitude}, longitude={self.longitude})"

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


if __name__ == "__main__":
    p = Point.from_bytes(b"4916.45", b"N", b"12311.12", b"W")
    print(p)
    print(str(p))

    print(p.lat)
    print(p.lon)

    p2 = Point(latitude=49.274, longitude=-123.185)
    p2.extra_attribute = 42
    """
    Traceback (most recent call last):
    File "", line 60, in <module>
        p2.extra_attribute = 42
    AttributeError: 'Point' object has no attribute 'extra_attribute'
    """
