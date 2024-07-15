class C:
    def f(self):
        return "hi"


class D:
    pass


if __name__ == "__main__":
    c = C()
    print(c)  # <__main__.C object at 0x10222bf70>
    print(c.f())  # hi

    c.__class__ = D
    print(c)  # <__main__.D object at 0x10222bf70>
    print(c.f())  # AttributeError: 'D' object has no attribute 'f'


"""
런타임에 객체 c의 클래스를 변경할 수 있음. 예에서 C와 D는 관련이 없는 클래스들이어서 c를 바꾸는 것은 위험한 일로 판명됨.
런타임에 클래스를 변경하는 것은 현명한 방법이 아님. 클래스 D의 인스턴스를 변경하면 c가 자신의 메서드 f를 잊어버릴 것이 명백함.

보다 구체적으로, 관련된 클래스에 대한 부모 클래스의 서브클래스를 구현하는 동일 인터페이스에서 런타임에서의 객체 변경은 강력함을 제공하며 상태 패턴 같은 패턴들의 구현에 사용될 수 있음.
상태 패턴을 구현하려면 이 방법을 사용해야 함.
"""
