import itertools
import random


class ComputerState:
    name = "state"
    next_states = []
    random_states = []

    def __init__(self) -> None:
        self.index = 0

    def __str__(self) -> str:
        return self.__class__.__name__

    def __iter__(self):
        return self

    def change(self):
        return self.__next__()

    def set(self, state):
        if self.index < len(self.next_states):
            if state in self.next_states:
                self.index = self.next_states.index(state)
                self.__class__ = eval(state)
                return self.__class__
            else:
                current = self.__class__
                new = eval(state)
                raise Exception(f"Illegal transition from {current} to {new}")

        else:
            self.index = 0
            if state in self.random_states:
                self.__class__ = eval(state)
                return self.__class__

    def __next__(self):
        if self.index < len(self.next_states):
            self.__class__ = eval(self.next_states[self.index])
            self.index += 1
            return self.__class__

        else:
            self.index = 0
            if len(self.random_states):
                state = random.choice(self.random_states)
                self.__class__ = eval(state)
                return self.__class__

            else:
                raise StopIteration


class ComputerOff(ComputerState):
    next_states = ["ComputerOn"]
    random_states = ["ComputerSuspend", "ComputerHibernate", "ComputerOff"]


class ComputerOn(ComputerState):
    random_states = ["ComputerSuspend", "ComputerHibernate", "ComputerOff"]


class ComputerWakeUp(ComputerState):
    random_states = ["ComputerSuspend", "ComputerHibernate", "ComputerOff"]


class ComputerSuspend(ComputerState):
    next_states = ["ComputerWakeUp"]
    random_states = ["ComputerSuspend", "ComputerHibernate", "ComputerOff"]


class ComputerHibernate(ComputerState):
    next_states = ["ComputerOn"]
    random_states = ["ComputerSuspend", "ComputerHibernate", "ComputerOff"]


class Computer:
    def __init__(self, model) -> None:
        self.model = model
        self.state = ComputerOff()

    def change(self, state=None):
        if state is None:
            return self.state.change()
        else:
            return self.state.set(state)

    def __str__(self) -> str:
        return str(self.state)


"""
이터레이터로서의 상태
- 이터레이터로 ComputerStatus 클래스를 구현함. 이것은 한 상태가 자연스럽게 상태 전환할 수 있는 매우 가까운 미래의 상태 목록을 가지고 있기 때문.
  예를 들어, Off 상태의 컴퓨터는 다음에는 On 상태로만 이동할 수 있음. 이터레이터로 정의하면 이터레이터가 한 상태에서 다음 상태로 자연스럽게 진행할 수 있는 이점이 있음.

무작위 상태
- 예제에서는 무작위 상태의 개념을 구현함. 컴퓨터가 한 상태에서 필수적인 다음 상태로 이동하면, 다음 이동할 수 있는 임의의 상태 목록을 가짐.
  On 상태의 컴퓨터는 항상 Off 상태로 전환될 필요가 없음. 또한 On 상태에서 Sleep 또는 Hibernate 상태로 갈 수 있음.

수동 변경
- 컴퓨터는 change 메서드의 선택적 두 번째 인수를 통해서 특정 상태로 이동할 수 있음. 그러나 이것은 상태 변경이 유효한 경우만 가능하며 그렇지 않을 때는 예외가 발생함.
"""

if __name__ == "__main__":
    c = Computer("ASUS")
    print(c)  # ComputerOff

    print(c.change())  # <class '__main__.ComputerOn'>
    print(c.change())  # <class '__main__.ComputerOff'>
    print(c.change())  # <class '__main__.ComputerOn'>
    print(c.change())  # <class '__main__.ComputerSuspend'>
    print(c.change())  # <class '__main__.ComputerWakeUp'>

    print(c.change())  # <class '__main__.ComputerHibernate'>
    print(c.change())  # <class '__main__.ComputerOn'>
    print(c.change())  # <class '__main__.ComputerOff'>

    for state in itertools.islice(c.state, 10):
        print(state)
        """
        <class '__main__.ComputerOn'>
        <class '__main__.ComputerOff'>
        <class '__main__.ComputerOn'>
        <class '__main__.ComputerOff'>
        <class '__main__.ComputerOn'>
        <class '__main__.ComputerHibernate'>
        <class '__main__.ComputerOn'>
        <class '__main__.ComputerHibernate'>
        <class '__main__.ComputerOn'>
        <class '__main__.ComputerSuspend'>
        """

    c.change("ComputerHibernate")
    # Suspend에서 Hibernate로 바로 갈 수 없음(next state가 아님)
    # Exception: Illegal transition from <class '__main__.ComputerSuspend'> to <class '__main__.ComputerHibernate'>
