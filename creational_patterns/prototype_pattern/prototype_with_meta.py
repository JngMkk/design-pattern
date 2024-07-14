import copy


class MetaPrototype(type):
    def __init__(cls, *args):
        type.__init__(cls, *args)
        cls.clone = lambda self: copy.deepcopy(self)


class PrototypeMeta(metaclass=MetaPrototype):
    pass


class ItemCollection(PrototypeMeta):
    """An item collection class"""

    def __init__(self, items: list[str] = []) -> None:
        self.items = items


if __name__ == "__main__":
    i1 = ItemCollection(items=["Apple", "Banana", "Cherry"])
    print(i1)
    # <__main__.ItemCollection object at 0x100872f80>

    i2 = i1.clone()
    print(i2)
    # <__main__.ItemCollection object at 0x100407a90>
    print(i2.items is i1.items)
    # False. 복제본은 분명하게 다른 객체. 복제본은 자체 속성의 복사본을 가지고 있음.
