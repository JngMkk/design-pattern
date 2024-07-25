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


"""
옵저버 패턴은 관찰을 수행하는 코드와 관찰의 대상이 되는 코드를 분리함.
이 패턴을 사용하지 않았다면 콘솔에 로깅하고, 데이터베이스 또는 파일을 업데이트하고, 특별한 경우를 확인하는 등 발생할 수 있는 다양한 경우를 처리하기 위해 ZonkHandHistory 클래스에 코드를 넣어야 함.
그러면 이런 각 작업에 대한 코드는 모두 코어 클래스 정의와 섞이게 됨.
그것을 유지하는 것은 악몽이 될 것이고 나중에 새로운 모니터링 기능을 추가하는 것은 힘들 것.
"""
