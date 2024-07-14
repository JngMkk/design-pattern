from creational_patterns._builder.problem import House, Porch, Room


class HouseBuilder:
    def __init__(self, *args, **kwds) -> None:
        self.house = House(*args, **kwds)

    def build(self) -> House:
        self.build_rooms()
        self.build_porches()
        return self.house

    def build_rooms(self) -> None:
        for _ in range(self.house.n_rooms):
            room = Room(
                self.house.n_room_windows, self.house.n_room_doors, self.house.room_direction
            )
            self.house.add_room(room)

    def build_porches(self) -> None:
        for _ in range(self.house.n_porches):
            porch = Porch(self.house.n_porch_doors, self.house.porch_direction)
            self.house.add_porch(porch)


class SmallHouseBuilder(HouseBuilder):
    def __init__(self, *args, **kwds) -> None:
        super().__init__(n_rooms=1, *args, **kwds)


class NorthFacingHouseBuilder(HouseBuilder):
    def __init__(self, *args, **kwds) -> None:
        super().__init__(room_direction="N", *args, **kwds)


class NorthFacingSmallHouseBuilder(SmallHouseBuilder, NorthFacingHouseBuilder):
    pass


"""
- 대상 클래스와 함께 빌더 클래스를 구성함. 이를 통해 방과 현관의 개수를 설정함.
- 집의 컴포넌트를 생성하고 조립하는 build 메서드를 지공함. 예제에서는 지정된 구성에 따라 Room과 Porch를 생성함.
- build 메서드는 생성되고 조립된 집을 반환함.
"""

if __name__ == "__main__":
    builder = HouseBuilder(n_rooms=3, n_porches=2, n_room_windows=2)
    house = builder.build()
    print(house)
    """
    House<rooms: #3, porches: #2>
    ...Room<facing: S, windows: #2, doors: #1>
    ...Room<facing: S, windows: #2, doors: #1>
    ...Room<facing: S, windows: #2, doors: #1>
    ...Porch<facing: W, doors: #1>
    ...Porch<facing: W, doors: #1>
    """

    small_house = SmallHouseBuilder().build()
    print(small_house)
    """
    House<rooms: #1, porches: #1>
    ...Room<facing: S, windows: #1, doors: #1>
    ...Porch<facing: W, doors: #1>
    """

    houses = list(map(lambda _: SmallHouseBuilder().build(), range(50)))
    print(houses[0])
    """
    House<rooms: #1, porches: #1>
    ...Room<facing: S, windows: #1, doors: #1>
    ...Porch<facing: W, doors: #1>
    """

    print(NorthFacingHouseBuilder(n_rooms=10, n_porches=3, n_room_windows=3).build())
    """
    House<rooms: #10, porches: #3>
    ...Room<facing: N, windows: #3, doors: #1>
    ...Room<facing: N, windows: #3, doors: #1>
    ...Room<facing: N, windows: #3, doors: #1>
    ...Room<facing: N, windows: #3, doors: #1>
    ...Room<facing: N, windows: #3, doors: #1>
    ...Room<facing: N, windows: #3, doors: #1>
    ...Room<facing: N, windows: #3, doors: #1>
    ...Room<facing: N, windows: #3, doors: #1>
    ...Room<facing: N, windows: #3, doors: #1>
    ...Room<facing: N, windows: #3, doors: #1>
    ...Porch<facing: W, doors: #1>
    ...Porch<facing: W, doors: #1>
    ...Porch<facing: W, doors: #1>
    """

    print(NorthFacingSmallHouseBuilder().build())
    """
    House<rooms: #1, porches: #1>
    ...Room<facing: N, windows: #1, doors: #1>
    ...Porch<facing: W, doors: #1>
    """
