class Room:
    def __init__(self, n_windows, n_doors, direction) -> None:
        self.n_windows = n_windows
        self.n_doors = n_doors
        self.direction = direction

    def __str__(self) -> str:
        return f"Room<facing: {self.direction}, windows: #{self.n_windows}, doors: #{self.n_doors}>"


class Porch:
    def __init__(self, n_doors, direction) -> None:
        self.n_doors = n_doors
        self.direction = direction

    def __str__(self) -> str:
        return f"Porch<facing: {self.direction}, doors: #{self.n_doors}>"


class House:
    def __init__(
        self,
        n_rooms=2,
        n_porches=1,
        n_room_windows=1,
        n_room_doors=1,
        n_porch_doors=1,
        room_direction="S",
        porch_direction="W",
    ) -> None:
        self.n_rooms = n_rooms
        self.n_porches = n_porches
        self.n_room_windows = n_room_windows
        self.n_room_doors = n_room_doors
        self.n_porch_doors = n_porch_doors
        self.room_direction = room_direction
        self.porch_direction = porch_direction

        self.rooms = []
        self.porches = []

    def __str__(self) -> str:
        msg = f"House<rooms: #{self.n_rooms}, porches: #{self.n_porches}>"

        for room in self.rooms:
            msg += f"\n...{str(room)}"

        for porch in self.porches:
            msg += f"\n...{str(porch)}"

        return msg

    def add_room(self, room: Room) -> None:
        self.rooms.append(room)
        return

    def add_porch(self, porch: Porch) -> None:
        self.porches.append(porch)
        return


if __name__ == "__main__":
    house = House(n_rooms=1, n_porches=1, n_room_windows=3)
    print(house)
    # House<rooms: #1, porches: #1>

    room = Room(house.n_room_windows, house.n_room_doors, house.room_direction)
    house.add_room(room)

    porch = Porch(house.n_porch_doors, house.porch_direction)
    house.add_porch(porch)

    print(house)
    """
    House<rooms: #1, porches: #1>
    ...Room<facing: S, windows: #3, doors: #1>
    ...Porch<facing: W, doors: #1>
    """


"""
- Room과 Porch 클래스는 각각 집의 방과 현관을 나타냄. 방은 창문과 문을 갖고 있으며 현관은 문을 갖고 있음.
- House 클래스는 실제 집에 대한 예제를 나타냄. 집은 여러 개의 방과 현관을 구성됨.

서로 다른 100개 집에 대한 인스턴스를 만들 필요가 있다고 가정하면, 각 집은 방과 현관 구성이 다르므로 위의 코드 작성으로 문제가 해결되지 않음.
빌더 패턴을 사용하면 이러한 문제를 해결할 수 있음.
"""
