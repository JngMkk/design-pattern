import copy

"""
싱글톤은 하나의 인스턴스만 허용하고 프로토타입은 여러 인스턴스를 유도하는 복제를 허용하기 때문에 한 클래스에 서로 충돌하는 패턴임.
그러나 API 관점에서 패턴을 생각한다면 조금 더 자연스러움.

- 생성자를 사용하는 클래스의 호출은 항상 같은 인스턴스를 반환함. 인스턴스는 싱글톤 패턴처럼 행동함.
- 클래스 인스턴스에 관현 clone의 호출은 늘 복제된 인스턴스들을 반환함. 인스턴스들은 항상 싱글톤 인스턴스를 소스로 사용해 복제됨.
  인스턴스는 프로토타입 패턴처럼 동작함.
"""


class MetaSingletonPrototype(type):
    """A metaclass for Singleton & Prototype patterns"""

    def __init__(cls, *args):
        print(cls, "__init__ method called with args:", args)
        type.__init__(cls, *args)

        cls.instance = None
        cls.clone = lambda self: copy.deepcopy(cls.instance)

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            print(cls, "creating prototypical instance", args, kwargs)
            cls.instance = type.__call__(cls, *args, **kwargs)

        return cls.instance


class PrototypeMeta(metaclass=MetaSingletonPrototype):
    pass


class ItemCollection(PrototypeMeta):
    """An item collection class"""

    def __init__(self, items: list[str] = []) -> None:
        self.items = items


if __name__ == "__main__":
    i1 = ItemCollection(items=["Apple", "Banana", "Cherry"])
    """
    <class '__main__.PrototypeMeta'> __init__ method called with args: ('PrototypeMeta', (), {'__module__': '__main__', '__qualname__': 'PrototypeMeta'})
    <class '__main__.ItemCollection'> __init__ method called with args: ('ItemCollection', (<class '__main__.PrototypeMeta'>,), {'__module__': '__main__', '__qualname__': 'ItemCollection', '__doc__': 'An item collection class', '__init__': <function ItemCollection.__init__ at 0x1041e8ee0>})
    <class '__main__.ItemCollection'> creating prototypical instance () {'items': ['Apple', 'Banana', 'Cherry']}
    """
    print(i1)
    # <__main__.ItemCollection object at 0x104bd3bb0>

    i2 = i1.clone()
    print(i2)
    # <__main__.ItemCollection object at 0x104c08490>
    print(i2.items)
    # ["Apple", "Banana", "Cherry"]
    i2.items.append("DDDD")
    print(i2.items)
    # ['Apple', 'Banana', 'Cherry', 'DDDD'
    print(i1.items)
    # ['Apple', 'Banana', 'Cherry']

    i3 = ItemCollection(items=["Apple", "Banana", "Cherry"])
    print(i3 is i1)
    # True
    print(i3)
    # <__main__.ItemCollection object at 0x104bd3bb0>

"""
메타클래스는 클래스를 생성할 때 강력한 사용자 정의를 가능하게 함.
예제에서는 싱글톤 패턴과 프로토타입 패턴을 메타클래스를 통해 모두 하나의 클래스에 포함하는 행위의 조합을 만듦.
메타클래스를 사용하는 파이썬의 강력함은 프로그래머에게 전통적인 패턴을 넘어 창조적인 기법을 찾게 함.
"""
