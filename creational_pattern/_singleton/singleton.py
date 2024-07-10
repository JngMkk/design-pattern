from typing_extensions import Self


class Singleton(object):
    """파이썬에서 가장 단순한 싱글톤 구현"""

    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = object.__new__(cls)

        return cls._instance


def test_singleton(cls):
    """Test if passed class is a singleton"""

    return cls() == cls()


s1 = Singleton()
s2 = Singleton()

print(s1 is s2)  # True
print(s1 == s2)  # True


class SingletonA(Singleton):
    pass


print(test_singleton(Singleton))  # True
print(test_singleton(Singleton))  # True

print(test_singleton(SingletonA))  # True
print(test_singleton(SingletonA))  # True
