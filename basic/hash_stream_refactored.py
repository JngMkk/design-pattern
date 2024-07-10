from hashlib import md5, sha1
from typing import IO


class StreamHasher(object):
    """Stream hasher class with configurable algorithm"""

    def __init__(self, algorithm, chunk_size=4096) -> None:
        self.hash = algorithm()
        self.chunk_size = chunk_size

    def get_hash(self, stream: IO) -> str:
        for chunk in iter(lambda: stream.read(self.chunk_size), ""):
            self.hash.update(chunk.encode("utf-8"))

        return self.hash.hexdigest()


md5h = StreamHasher(algorithm=md5)
sha1h = StreamHasher(algorithm=sha1)

print(md5h.get_hash(open(__file__)))  # 28a6551656f122998f038a9fdab1d4ee
print(sha1h.get_hash(open(__file__)))  # aa52349f858613c7984d787a0936940b80ff8f9a
