from typing import Any

from creational_patterns._singleton.singleton import test_singleton


class SingletonMeta(type):
    """A type for Singleton classes (overrides __call__)"""

    def __init__(cls, *args: Any) -> None:
        print(cls, "__init__ method called with args", args)
        type.__init__(cls, *args)
        cls.instance = None

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if not cls.instance:
            print(cls, "creating instance", args, kwds)
            cls.instance = type.__call__(cls, *args, **kwds)

        return cls.instance


class Singleton(metaclass=SingletonMeta):
    pass


if __name__ == "__main__":
    # <class '__main__.Singleton'> __init__ method called with args ('Singleton', (), {'__module__': '__main__', '__qualname__': 'Singleton'})
    print(test_singleton(Singleton))
    """
    <class '__main__.Singleton'> creating instance () {}
    True
    """

"""
- 클래스 변수 초기화
    : 앞의 구현에서 봤듯, 클래스 수준에서 클래스 변수의 초기화를 수행하거나(클래스 선언 다음에) 메타클래스의 __init__ 메서드에서 클래스 변수를 초기화할 수 있음.
      클래스의 단일 인스턴스를 유지하는 instance 클래스 변수에 수행하는 작업임.

- 클래스 생성 오버라이딩
    : 클래스의 __new__ 메서드를 오버라이딩해 클래스 수준에서 수행하거나 이와 똑같이 메타클래스에서 __call__ 메서드를 오버라이딩 할 수 있음.
"""

"""
클래스의 __call__ 메서드를 오버라이드하면 클래스의 인스턴스에 영향을 미치며 인스턴스를 호출할 수 있게 됨.
이와 비슷하게 메타클래스의 __call__ 메서드를 오버라이드하면 클래스에 영향을 미치고 클래스들이 호출되는 방법.
즉, 클래스가 인스턴스를 생성하는 방법을 변경시킴.
"""

"""
클래스 vs 메타클래스

메타클래스를 통해 싱글톤 동작을 하는 새로운 최상위 수준의 클래스를 여러 개 생성할 수 있는 것이 이점 중 하나.
기본 구현을 사용해, 모든 클래스는 최상위 클래스인 Singleton이나 이 클래스의 하위 클래스를 상속받아 싱글톤 동작을 가져갈 수 있음.
메타클래스 방식은 클래스 계층 구조 측면에서 더 많은 유연성을 제공함.

메타클래스 방식은 클래스 방식과 달리 약간 모호하고 유지하기 어려운 코드를 생성하는 것으로 해석되기도 함.
클래스를 이해하는 프로그래머의 수에 비해 메타클래스와 메타 프로그래밍을 이해하는 파이썬 프로그래머가 적기 때문인데, 이는 메타클래스 솔루션의 단점이기도 함.
"""
