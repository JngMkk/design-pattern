import itertools


class Polygon:
    def __init__(self, *sides) -> None:
        self.sides = sides

    def perimeter(self) -> int | float:
        return sum(self.sides)

    def is_valid(self) -> bool:
        raise NotImplementedError

    def is_regular(self) -> bool:
        side = self.sides[0]
        return all([x == side for x in self.sides[1:]])

    def area(self) -> int | float:
        raise NotImplementedError


"""
위 클래스는 기하학에서 일반적인 닫혀진 모양의 다각형을 기술함.

삼각형이나 사각형과 같은 일반적인 기하학 모양의 구체적인 클래스를 구현하낟고 가정해 보자.
물론, 처음부터 구현할 수 있지만 Polygon 클래스를 사용할 수 있으므로 클래스를 재사용해 필요에 따라 적용할 수 있음.

Triangle 클래스는 다음과 같은 메서드가 필요하다고 가정.
- is_equilateral: 삼각형이 정삼각형인지 확인
- is_isosceles: 삼각형이 이등변 삼각형인지 확인
- is_valid: 삼각형의 is_valid 메서드를 구현
- area: 삼각형의 area 메서드를 구현

Rectangle 클래스는 다음과 같은 메서드가 필요하다고 가정.
- is_square: 사각형이 정사각형인지 확인
- is_valid: 사각형의 is_valid 메서드를 구현
- area: 사각형의 area 메서드를 구현
"""


class InvalidPolygonError(Exception):
    pass


class Triangle(Polygon):
    def is_equilateral(self) -> bool:
        if self.is_valid():
            return self.is_regular()

    def is_isosceles(self) -> bool:
        if self.is_valid():
            for a, b in itertools.combinations(self.sides, 2):
                if a == b:
                    return True
        return False

    def area(self) -> float:
        p = self.perimeter() / 2.0
        total = p
        for side in self.sides:
            total *= abs(p - side)

        return pow(total, 0.5)

    def is_valid(self) -> bool:
        perimeter = self.perimeter()
        for side in self.sides:
            sum_two = perimeter - side
            if sum_two <= side:
                raise InvalidPolygonError(f"{self.__class__} is invalid.")

        return True


class Rectangle(Polygon):
    def is_square(self) -> bool:
        if self.is_valid():
            return self.is_regular()

    def is_valid(self) -> bool:
        if len(self.sides) != 4:
            return False

        for a, b in [(0, 2), (1, 3)]:
            if self.sides[a] != self.sides[b]:
                return False

        return True

    def area(self) -> int | float:
        if self.is_valid():
            return self.sides[0] * self.sides[1]


if __name__ == "__main__":
    t1 = Triangle(20, 20, 20)
    print(t1.is_valid())
    # True
    print(t1.is_equilateral())
    # True
    print(t1.is_isosceles())
    # True
    print(t1.perimeter())
    # 60
    print(t1.area())
    # 173.20508075688772

    # t2 = Triangle(10, 20, 30)
    # print(t2.is_valid())
    # __main__.InvalidPolygonError: <class '__main__.Triangle'> is invalid.

    r1 = Rectangle(10, 20, 10, 20)
    print(r1.is_valid())
    # True
    print(r1.is_square())
    # False
    print(r1.area())
    # 200
    print(r1.perimeter())
    # 60

    r2 = Rectangle(10, 10, 10, 10)
    print(r2.is_square())
    # True


"""
여기서 Rectangle/Triangle 클래스는 class adapter의 예임.
이들은 적용하기 원하는 클래스를 상속받고 클라이언트가 기대하는 메서드를 제공하며, 때때로 기본 클래스의 메서드에 계산을 위임하기 때문.
Triangle과 Rectangle 클래스의 is_equilateral과 is_square 메서드에서 확인할 수 있음.
"""
