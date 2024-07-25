import json
import time

from .dice import Dice
from .observer import Observable, Observer

Hand = list[int]


class ZonkHandHistory(Observable):
    """
    플레이어가 매 턴마다 실행한 결과를 hand 리스트에 유지함.

    중요한 상태 변경이 있을 때 self.notify_observers()를 호출함. 이것은 모든 옵저버 인스턴스에 알림을 보냄.
    옵저버는 각 터의 복사본을 캐시하고, 네트워크를 통해 상세정보를 보내고, GUI에서 위젯을 업데이트할 것임.
    Observable에서 상속받은 notify_observers() 메서드는 등록된 모든 옵저버에게 Hand의 상태가 변경됐음을 각각 알림.
    """

    def __init__(self, player: str, dice_set: Dice) -> None:
        super().__init__()
        self.player = player
        self.dice_set = dice_set
        self.rolls: list[Hand]

    def start(self) -> Hand:
        self.dice_set.roll()
        self.rolls = [self.dice_set.dice]
        self.notify_observers()  # 상태 변경

        return self.dice_set.dice

    def roll(self) -> Hand:
        self.dice_set.roll()
        self.rolls.append(self.dice_set.dice)
        self.notify_observers()  # 상태 변경

        return self.dice_set.dice


class SaveZonkHand(Observer):
    def __init__(self, hand: ZonkHandHistory) -> None:
        self.hand = hand
        self.count = 0

    def __call__(self) -> None:
        self.count += 1
        message = {
            "player": self.hand.player,
            "count": self.count,
            "hands": json.dumps(self.hand.rolls),
            "time": time.time(),
        }

        print(f"SaveZonkHand: {message}")


class ThreePairZonkHand:
    """ZonkHandHistory의 옵저버"""

    def __init__(self, hand: ZonkHandHistory) -> None:
        self.hand = hand
        self.zonked = False

    def __call__(self) -> None:
        last_roll = self.hand.rolls[-1]
        distinct_values = set(last_roll)
        self.zonked = len(distinct_values) == 3 and all(
            last_roll.count(v) == 2 for v in distinct_values
        )
        if self.zonked:
            print("3 Pair Zonk!")
