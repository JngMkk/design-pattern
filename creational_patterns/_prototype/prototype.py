import copy

"""
깊은 복사 vs 얕은 복사

얕은 복사를 하면 모든 객체가 참조를 통해 복사됨. 이것은 튜플이나 문자열 같은 불변 객체는 변경할 수 없기 때문에 아무런 문제가 되지 않음.
그러나 리스트나 딕셔너리 같이 변경 가능한 객체는 인스턴스의 상태가 인스턴스에 의해 완전히 소유되지 않고 공유되기 때문에 문제가 됨.
그리고 한 인스턴스에서 변경한 모든 수정 사항은 복제된 인스턴스의 동일한 객체를 수정할 것임.
"""


class Prototype:
    def clone(self):
        """Return a clone of self"""

        return copy.deepcopy(self)


class Register(Prototype):
    """A student Register class"""

    def __init__(self, names=[]) -> None:
        self.names = names


class SPrototype:
    """A prototype base class using shallow copy"""

    def clone(self):
        return copy.copy(self)


class SRegister(SPrototype):
    def __init__(self, names: list[str] = []) -> None:
        self.names = names


if __name__ == "__main__":
    r1 = Register(names=["Kang", "Kim", "Park"])
    r2 = r1.clone()

    print(r1)
    # <__main__.Register object at 0x100872f80>

    print(r2)
    # <__main__.Register object at 0x100873a30>

    print(r2.__class__)
    # <class '__main__.Register'>

    r1 = SRegister(names=["Kang", "Kim", "Park"])
    r2 = r1.clone()
    r1.names.append("Choi")

    print(r2.names)
    # ['Kang', 'Kim', 'Park', 'Choi']

"""
얕은 복사로 인해 객체 전체가 아닌 참조만 복사되기 때문에, 결국 r1과 r2는 모두 같은 names 리스트를 공유함.
깊은 복사는 모든 객체를 재귀적으로 복사함. 따라서 아무 것도 공유되지 않지만 모든 복제본마다 참조된 객체의 자체 복사본을 갖게 됨.
"""
