from creational_patterns._prototype.prototype import SPrototype
from creational_patterns._singleton.borg import Borg

"""
프로토타입 클래스는 프로토타입 방식으로 구성 패밀리나 제품 그룹의 인스턴스 생성을 위한 팩토리 함수를 제공할 수 있는 프로토타입 팩토리나 레지스트리 클래스를 사용해 개선할 수 있음.
이 패턴은 팩토리 패턴의 변형으로 생각할 수 있음.
"""


class PrototypeFactory(Borg):
    """A prototype factory/registry class"""

    def __init__(self) -> None:
        super().__init__()
        self._registry = {}

    def register(self, instance):
        """Register a given instance"""

        self._registry[instance.__class__] = instance

    def clone(self, klass):
        """Return cloned instance of given class"""

        instance = self._registry.get(klass)
        if instance is None:
            print(f"Error {klass} not registered")

        else:
            return instance.clone()


class Name(SPrototype):
    def __init__(self, first, second) -> None:
        super().__init__()
        self.first = first
        self.second = second

    def __str__(self) -> str:
        return " ".join((self.first, self.second))

    def __eq__(self, value: object) -> bool:
        return self.__str__() == value.__str__()


class Animal(SPrototype):
    def __init__(self, name, _type="Wild") -> None:
        super().__init__()
        self.name = name
        self.type = _type

    def __str__(self) -> str:
        return " ".join((self.type, self.name))

    def __eq__(self, value: object) -> bool:
        return self.__str__() == value.__str__()


if __name__ == "__main__":
    name = Name("Kang", "In")
    animal = Animal("Tiger")

    print(name)  # Kang In
    print(animal)  # Wild Tiger

    factory = PrototypeFactory()
    factory.register(name)
    factory.register(animal)

    cloned_name = factory.clone(Name)
    cloned_animal = factory.clone(Animal)
    print(name == cloned_name)  # True
    print(name is cloned_name)  # False

    print(animal, cloned_animal)  # Wild Tiger Wild Tiger
    print(id(animal), id(cloned_animal))  # 4340464944 4340465520

    class C:
        pass

    factory.clone(C)
    # Error <class '__main__.C'> not registered


"""
여기서 보이는 팩토리는 등록된 모든 클래스가 프로토타입 클래스의 API를 준수하는지 확인하기 위해 등록된 클래스에 clone 메서드가 있는지 검사하도록 개선할 수 있음.

- PrototypeFactory 클래스는 팩토리 클래스이므로 거의 싱글톤임. 이때 클래스 계층에 걸쳐 상태를 공유하는데는 보그 패턴이 더 낫기 때문에 보그를 사용함.

- Name 클래스와 Animal 클래스는 속성이 불변인 정수와 문자열이기 때문에, Name 클래스와 Animal 클래스는 SPrototype 클래스를 상속함.
  따라서 여기에는 얕은 복사가 좋음.

- 프로토타입은 프로토타입의 인스턴스, 즉 clone 메서드에서 클래스 생성 시그니처를 유지함.
  프로그래머가 클래스 생성 시그니처 __new__와 __init__ 메서드의 파라미터 순서와 타입을 걱정할 필요가 없기 때문에 프로그래머는 고민할 필요가 없음.
  그러나 기존 인스턴스에서 clone을 호출해야만 함.
"""
