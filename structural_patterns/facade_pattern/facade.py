class Engine:
    def __init__(self, name, bhp, rpm, volume, cylinders=4, type="petrol") -> None:
        self.name = name
        self.bhp = bhp
        self.rpm = rpm
        self.volume = volume
        self.cylinders = cylinders
        self.type = type

    def start(self) -> None:
        print("Eninge Started.")

    def stop(self) -> None:
        print("Engine Stopped.")


class Transmission:
    def __init__(self, gears, torque) -> None:
        self.gears = gears
        self.torque = torque

        self.gear_pos = 0

    def shift_up(self) -> None:
        if self.gear_pos == self.gears:
            print("Can't shift up anymore.")

        else:
            self.gear_pos += 1
            print(f"Shifted up to gear {self.gear_pos}")

    def shift_down(self) -> None:
        if self.gear_pos == 0:
            print("Can't shift down.")
        else:
            self.gear_pos -= 1
            print(f"Shifted down to gear {self.gear_pos}")

    def shift_to(self, gear) -> None:
        self.gear_pos = gear
        print(f"Shifted to gear {self.gear_pos}")


class Brake:
    def __init__(self, number, type="disc") -> None:
        self.type = type
        self.number = number

    def engage(self) -> None:
        print(f"{self.__class__.__name__} {self.number} engaged.")

    def release(self) -> None:
        print(f"{self.__class__.__name__} {self.number} released.")


class ParkingBrake(Brake):
    def __init__(self, type="drum") -> None:
        super().__init__(1, type)


class Suspension:
    def __init__(self, load, type="mcpherson") -> None:
        self.load = load
        self.type = type


class Wheel:
    def __init__(self, material, diameter, pitch) -> None:
        self.material = material
        self.diameter = diameter
        self.pitch = pitch


class WheelAssembly:
    def __init__(self, brake: Brake, suspension: Suspension) -> None:
        self.brake = brake
        self.suspension = suspension

        self.wheels = Wheel("alloy", "M12", 1.25)

    def apply_brakes(self) -> None:
        print("Applying brakes.")
        self.brake.engage()


class Frame:
    def __init__(self, length, width) -> None:
        self.length = length
        self.width = width


class Car:
    def __init__(self, model, manufacturer) -> None:
        self.model = model
        self.manufacturer = manufacturer

        self.engine = Engine("K-series", 85, 5000, 1.3)
        self.frame = Frame(385, 170)
        self.transmission = Transmission(5, 115)
        self.parking_brake = ParkingBrake()

        self.ignition = False
        self.wheel_assemblies: list[WheelAssembly] = []
        for i in range(4):
            self.wheel_assemblies.append(WheelAssembly(Brake(i + 1), Suspension(1000)))

    def start(self) -> None:
        print("Starting the car.")

        self.ignition = True
        self.parking_brake.release()
        self.engine.start()
        self.transmission.shift_up()

        print("Car started.")

    def stop(self) -> None:
        print("Stopping the car.")

        for wheel in self.wheel_assemblies:
            wheel.apply_brakes()

        self.transmission.shift_to(1)
        self.engine.stop()
        self.transmission.shift_to(0)

        self.parking_brake.engage()
        self.ignition = False
        print("Car stopped.")


if __name__ == "__main__":
    car = Car("Swift", "Maruti Suzuki")
    print(car)  # <__main__.Car object at 0x101082230>

    car.start()
    """
    Starting the car.
    ParkingBrake 1 released.
    Eninge Started.
    Shifted up to gear 1
    Car started.
    """

    car.stop()
    """
    Stopping the car.
    Applying brakes.
    Brake 1 engaged.
    Applying brakes.
    Brake 2 engaged.
    Applying brakes.
    Brake 3 engaged.
    Applying brakes.
    Brake 4 engaged.
    Shifted to gear 1
    Engine Stopped.
    Shifted to gear 0
    ParkingBrake 1 engaged.
    Car stopped.
    """


"""
파사드는 시스템의 복잡성을 제거하는 데 유용함. 따라서 시스템의 작업 수행을 쉽게 만듦.
앞의 예에서 볼 수 있듯 예제에서 수행한 방법으로 start와 stop 메서드를 만들지 않았다면 작업은 매우 어려웠을 것임.
메서드들은 Car를 출발시키고 멈추는 서브시스템의 배경 작업에 있는 복잡성을 숨김.
"""
