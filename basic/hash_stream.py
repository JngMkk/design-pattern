from hashlib import md5
from typing import IO

"""
입력 스트림(파일이나 네트워크 소켓)에서 데이터를 읽고 청크 방식으로 컨텐츠를 해싱하기 원한다면 아래와 같이 코드를 작성할 수 있음.
"""


def hash_stream(stream: IO, chunk_size: int = 4096) -> str:
    """Hash a stream of data using md5"""

    shash = md5()
    for chunk in iter(lambda: stream.read(chunk_size), ""):
        shash.update(chunk.encode("utf-8"))

    return shash.hexdigest()


print(hash_stream(open(__file__)))  # df5f3c2a829b62954410a3a09a1b7d37
