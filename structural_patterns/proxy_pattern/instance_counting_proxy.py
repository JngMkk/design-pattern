from typing_extensions import Self

from creational_patterns.factory_pattern.factory import (
    Accountant,
    Admin,
    Employee,
    EmployeeType,
    Engineer,
)


class EmployeeProxy:
    count = 0

    def __new__(cls, *args) -> Self:
        instance = super().__new__(cls)
        cls.incr_count()

        return instance

    def __init__(self, employee: Employee) -> None:
        self.employee = employee

    @classmethod
    def incr_count(cls) -> None:
        cls.count += 1

    @classmethod
    def decr_count(cls) -> None:
        cls.count -= 1

    @classmethod
    def get_count(cls) -> int:
        return cls.count

    def __str__(self) -> str:
        return str(self.employee)

    def __getattr__(self, name):
        return getattr(self.employee, name)

    def __del__(self) -> None:
        self.decr_count()


class EmployeeProxyFactory:
    @classmethod
    def create(cls, name: EmployeeType, *args) -> EmployeeProxy:
        if name == EmployeeType.ENGINEER:
            return EmployeeProxy(Engineer(*args))
        elif name == EmployeeType.ACCOUNTANT:
            return EmployeeProxy(Accountant(*args))
        elif name == EmployeeType.ADMIN:
            return EmployeeProxy(Admin(*args))


"""
EmployeeProxy와 Employee 대신 EmployeeProxy의 인스턴스를 반환하기 위해 수정된 Factory 클래스를 갖고 있음.
수정된 Factory 클래스를 사용하면 인스턴스를 직접 생성하는 대신 프록시 인스턴스를 생성할 수 있음.

여기에 구현된 프록시는 대상 객체에 액세스하는 속성의 리다이렉션을 위해 대상 객체를 래핑하고 __getattr__을 오버로딩하기 때문에 합성 프록시나 객체 프록시가 됨.
인스턴스의 생성과 삭제를 위해 각각 __new__와 __del__ 메서드를 오버라이딩해 인스턴스의 개수를 추적함.
"""

if __name__ == "__main__":
    factory = EmployeeProxyFactory()
    engineer = factory.create(EmployeeType.ENGINEER, "Kang", 25, "M")
    print(engineer)  # Engineer - Kang, 25 years old M

    admin = factory.create(EmployeeType.ADMIN, "Kim", 30, "F")
    print(admin)  # Admin - Kim, 30 years old F

    print(admin.get_count())  # 2
    print(EmployeeProxy.get_count())  # 2

    del engineer
    print(EmployeeProxy.get_count())  # 1

    del admin
    print(EmployeeProxy.count)  # 0
