class Borg(object):
    """Not a singleton, but a class whose instances share state."""

    __shared_state = {}

    def __init__(self) -> None:
        self.__dict__ = self.__shared_state


class IBorg(Borg):
    def __init__(self) -> None:
        super().__init__()
        self.state = "init"

    def __str__(self) -> str:
        return self.state


if __name__ == "__main__":
    i1 = IBorg()
    i2 = IBorg()
    print(i1)
    # init
    print(i2)
    # init

    i1.state = "running"
    print(i1)
    # running
    print(i1.__dict__)
    # {'state': 'running'}

    print(i2)
    # running
    print(i2.__dict__)
    # {'state': 'running'}

    print(i1 == i2)
    # False
    print(i1 is i2)
    # False

"""
싱글톤과 비교해 보그 패턴의 장점

- 기본 Singleton 클래스를 상속하는 여러 개의 클래스를 갖는 복잡한 시스템에서 import 문제나 경쟁 조건으로 인해 인스턴스의 요구사항을 강제하는 것이 어려울 수 있음.
  예를 들어, 시스템이 스레드를 사용한다면 보그 패턴 메모리에서 단일 인스턴스 요구사항을 제거해 문제를 깔끔하게 회피함.

- 보그 패턴은 보그 클래스와 모든 서브클래스에 걸쳐 간단하게 상태를 공유할 수 있음. 각 서브클래스가 자체적인 상태를 생성하기 때문에 싱글톤이 아님.

1. 상태 공유 - 보그 vs 싱글톤
    보그 패턴은 최상위 클래스에서 모든 서브클래스까지 항상 같은 상태를 공유하는 점에서 싱글톤과 다름.
    보그 패턴은 하나의 인스턴스를 보장하는 번거로움이나 오버헤드 없이 상태를 공유할 수 있음.
"""
