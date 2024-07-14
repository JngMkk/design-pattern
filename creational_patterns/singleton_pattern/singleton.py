def test_singleton(cls):
    """Test if passed class is a singleton"""

    return cls() == cls()


class Singleton(object):
    """파이썬에서 가장 단순한 싱글톤 구현"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

        return cls._instance


class SingletonA(Singleton):
    pass


if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()

    print(s1 is s2)  # True
    print(s1 == s2)  # True

    print(test_singleton(Singleton))  # True
    print(test_singleton(Singleton))  # True

    print(test_singleton(SingletonA))  # True
    print(test_singleton(SingletonA))  # True
    print(test_singleton(SingletonA))  # True
