import itertools

from structural_patterns.adapter_pattern.ex2.main import InvalidPolygonError, Polygon


class Triangle:
    def __init__(self, *sides) -> None:
        self.polygon = Polygon(*sides)

    def perimeter(self) -> int:
        return self.polygon.perimeter()

    def is_valid(f) -> bool:
        def inner(self, *args):
            perimeter = self.perimeter()

            for side in self.polygon.sides:
                sum_two = perimeter - side
                if sum_two <= side:
                    raise InvalidPolygonError(f"{self.__class__} is invalid.")

            return f(self, *args)

        return inner

    @is_valid
    def is_equilateral(self) -> bool:
        return self.polygon.is_regular()

    @is_valid
    def is_isosceles(self) -> bool:
        for a, b in itertools.combinations(self.polygon.sides, 2):
            if a == b:
                return True
        return False

    @is_valid
    def area(self) -> float:
        p = self.perimeter() / 2.0
        total = p

        for side in self.polygon.sides:
            total *= abs(p - side)

        return pow(total, 0.5)


"""
내부의 세부 사항들이 클래스 상속보단 객체의 합성을 통해 구현되었다.

object adapter와 class adapter 사이의 주된 차이점은 다음과 같음.
    - 객체 어댑터 클래스는 적용을 원하는 클래스에서 상속받지 않는 대신 해당 클래스의 인스턴스를 구성함.
    - 모든 Wrapper 메서드가 구성된 인스턴스로 전달됨. perimeter 메서드가 여기에 해당함.
    - Wrapping된 인스턴스의 모든 속성에 대한 액세스는 구현에서 명시적으로 지정돼야 함.
      클래스를 상속받지 않기 때문에 저절로 되는 것은 없음.(예를 들어, polygon 인스턴스의 sides 속성을 접근하는 방법의 검사)

object adapter의 한 가지 문제점은 어댑터 인스턴스의 모든 속성 참조를 명시적으로 해야 한다는 점임.
예를 들어, Triangle 클래스에 관한 perimeter 메서드 구현을 잊어버린다면 클래스를 상속받지 않았기 때문에 호출하기 위한 메서드가 전혀 없음.

이는 파이썬의 __getattr__ 매직 메서드를 사용해 속성 참조를 단순하게 만드는 대안적인 구현을 사용할 수 있음.
"""


class Rectangle:
    method_mapper = {"is_square": "is_regular"}

    def __init__(self, *sides) -> None:
        self.polygon = Polygon(*sides)

    def is_valid(f) -> bool:
        def inner(self: "Rectangle", *args):
            sides = self.polygon.sides

            if len(sides) != 4:
                return False

            for a, b in [(0, 2), (1, 3)]:
                if sides[a] != sides[b]:
                    return False

            return f(self, *args)

        return inner

    def __getattr__(self, name):
        if name in self.method_mapper:
            wrapped_name = self.method_mapper[name]
            print(f"Forwarding to method {wrapped_name}")

            return getattr(self.polygon, wrapped_name)
        else:
            return getattr(self.polygon, name)

    @is_valid
    def area(self) -> int | float:
        sides = self.polygon.sides
        return sides[0] * sides[1]


if __name__ == "__main__":
    t1 = Triangle(2, 2, 2)
    print(t1.is_equilateral())
    # True

    t2 = Triangle(4, 4, 5)
    print(t2.is_isosceles())
    # True
    print(t2.is_equilateral())
    # False

    r1 = Rectangle(10, 20, 10, 20)
    print(r1.perimeter())
    # 60
    print(r1.is_square())
    """
    Forwarding to method is_regular
    False
    """


"""
실제로 클래스에 메서드가 정의되지 않아도 Rectangle 인스턴스의 is_perimeter 메서드를 호출할 수 있음.
유사하게 is_square 역시 마법처럼 동작함.

일반적인 방법으로 속성을 찾을 수 없으면 파이썬은 객체에 매직 메서드 __getattr__을 호출함.
속성을 찾으려면 먼저 객체의 딕셔너리를 찾고, 그 다음 객체 클래스의 딕셔너리를 찾는 방법이 일반적임.
따라서 라우팅을 통해 다른 객체에서 이들에 관한 조회 메서드를 제공하는 방법을 구현하기 위해 이름을 통해 클래스에 관한 hook을 제공함.

예제에서 __getattr__ 메서드는 다음 사항을 수행함.
    - method_mapper 딕셔너리에서 속성의 이름을 검사함.
      딕셔너리는 클래스에 생성한 것으로, 클래스에서 호출하기 원하는 메서드 이름을 래핑된 인스턴스의 실제 메서드 이름에 매핑함. 항목이 발견되면 반환함.
    - 항목이 method_mapper에 없으면 항목은 같은 이름으로 보이는 래핑된 인스턴스로 전달됨.
    - 두 경우 모두 래핑된 인스턴스에서 속성을 찾아 반환하기 위해 getattr을 사용함. 속성은 데이터 속성이나 메서드가 될 수 있음.
    - 래핑된 인스턴스의 속성이 존재하지 않으면, AttributeError 예외가 발생함.
"""
