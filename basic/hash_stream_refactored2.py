"""
(hash_stream_refactored에 구현된) 클래스는 다양한 해싱 알고리즘 관점에서 다목적이며 더 많이 재사용할 수 있음.
그러나 함수처럼 클래스를 호출할 수 있는 방법이 있는가? 그 방법이 더 깔끔한 것이 맞는가?
"""

from hashlib import md5, sha1
from typing import IO


class StreamHasher(object):
    """Stream hasher class with configurable algorithm"""

    def __init__(self, algorithm, chunk_size: int = 4096) -> None:
        self.hash = algorithm()
        self.chunk_size = chunk_size

    def __call__(self, stream: IO) -> str:
        """클래스를 호출 가능하게 만들면 함수처럼 사용할 수 있음"""

        for chunk in iter(lambda: stream.read(self.chunk_size), ""):
            self.hash.update(chunk.encode("utf-8"))

        return self.hash.hexdigest()


md5h = StreamHasher(algorithm=md5)
sha1h = StreamHasher(algorithm=sha1)

print(md5h(open(__file__)))  # 355a06bc3518ec5fac05387590a959f4
print(sha1h(open(__file__)))  # 7f75b6a6f3dd5113e061bee1caaf4d856d4e132d

"""
전략 행위 패턴을 구현함으로써 클래스를 함수처럼 사용할 수 있게 되었음.
전략 패턴은 클래스와 다른 행위가 필요할 때 사용함. 그리고 다양한 행위와 알고리즘 중 하나로 클래스를 이용할 수 있어야 함.

이러한 경우 같은 청크를 사용해 스트림에서 데이터를 해싱하고 다이제스트를 반환하기 위해 다양한 알고리즘을 지원하는 클래스가 필요함.
클래스는 알고리즘을 파라미터로 받아들이고 모든 알고리즘은 데이터를 반환하기 위해 같은 메서드(hexdigest 메서드)를 지원하기 때문에 매우 간단한 방법으로 클래스를 구현할 수 있었음.
"""
