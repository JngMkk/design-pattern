from abc import ABCMeta, abstractmethod
from enum import Enum


class Employee(metaclass=ABCMeta):
    def __init__(self, name, age, gender) -> None:
        self.name = name
        self.age = age
        self.gender = gender

    @abstractmethod
    def get_role(self):
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__} - {self.name}, {self.age} years old {self.gender}"


class Engineer(Employee):
    def get_role(self):
        return "engineering"


class Accountant(Employee):
    def get_role(self):
        return "accountant"


class Admin(Employee):
    def get_role(self):
        return "administration"


class EmployeeType(str, Enum):
    ENGINEER = "engineer"
    ACCOUNTANT = "accountant"
    ADMIN = "admin"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class EmployeeFactory:
    @classmethod
    def create(cls, name, *args):
        """Factory method for creating Employee instance"""

        if not isinstance(name, EmployeeType):
            raise ValueError(f"EmployeeType {name} is not valid")

        if name == EmployeeType.ENGINEER:
            return Engineer(*args)
        elif name == EmployeeType.ACCOUNTANT:
            return Accountant(*args)
        elif name == EmployeeType.ADMIN:
            return Admin(*args)


if __name__ == "__main__":
    factory = EmployeeFactory()
    print(factory.create(EmployeeType.ENGINEER, "Kang", 25, "M"))  # Engineer - Kang, 25 years old M
    print(factory.create(EmployeeType.ENGINEER, "Choi", 25, "M"))  # Engineer - Choi, 25 years old M

    accountant = factory.create(EmployeeType.ACCOUNTANT, "Kim", 25, "F")
    print(accountant)  # Accountant - Kim, 25 years old F
    print(accountant.get_role())  # accountant

    admin = factory.create(EmployeeType.ADMIN, "Lee", 25, "F")
    print(admin)  # Admin - Lee, 25 years old F
    print(admin.get_role())  # administration

    print(EmployeeFactory.create(EmployeeType.ENGINEER, "Park", 25, "F"))
    # Engineer - Park, 25 years old F

"""
- 단일 팩토리 클래스는 Employee 계층의 모든 클래스에 대한 인스턴스를 생성할 수 있음.

- 팩토리 패턴에서는 클래스 패밀리(클래스와 해당 클래스의 하위 클래스 계층)에 관련된 하나의 Factory 클래스를 사용함.
  예를 들어, Person 클래스는 PersonFactory를 사용할 수 있으며, Automobile 클래스는 AutomobileFactory를 사용할 수 있음.

- 팩토리 메서드는 파이썬의 classmethod로 데코레이션됨. 이렇게 하면, 메서드를 클래스 네임스페이스를 통해 직접 호출될 수 있음.
  즉, 팩토리 클래스의 인스턴스는 이 패턴에서는 실제로 필요하지 않음.
"""
