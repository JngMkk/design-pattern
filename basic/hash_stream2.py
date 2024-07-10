from hashlib import md5, sha1
from typing import IO

"""
재사용이 더 쉬워지면서 다양한 해싱 알고리즘과 함께 동작하는 다용도의 구현을 원한다고 가정하자.
첫 번째 시도는 이전 코드를 수정하는 것이지만, 많은 양의 코드를 다시 작성해야 하기 때문에 그리 현명한 방법은 아니다.
"""


def hash_stream_sha1(stream: IO, chunk_size: int = 4096) -> str:
    """Hash a stream of data using sha1"""

    shash = sha1()
    for chunk in iter(lambda: stream.read(chunk_size), ""):
        shash.update(chunk.encode("utf-8"))

    return shash.hexdigest()


def hash_stream_md5(stream: IO, chunk_size: int = 4096) -> str:
    """Hash a stream of data using md5"""

    shash = md5()
    for chunk in iter(lambda: stream.read(chunk_size), ""):
        shash.update(chunk.encode("utf-8"))

    return shash.hexdigest()


print(hash_stream_sha1(open(__file__)))
print(hash_stream_md5(open(__file__)))
