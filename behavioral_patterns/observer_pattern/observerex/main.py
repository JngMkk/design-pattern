from behavioral_patterns.observer_pattern.observerex.dice import Dice
from behavioral_patterns.observer_pattern.observerex.zonk import (
    SaveZonkHand,
    ThreePairZonkHand,
    ZonkHandHistory,
)

if __name__ == "__main__":
    d = Dice.from_text("6d6")
    player = ZonkHandHistory("Bo", d)

    save = SaveZonkHand(player)
    is_3pair = ThreePairZonkHand(player)
    player.attach(save)
    player.attach(is_3pair)

    r1 = player.start()
    # SaveZonkHand: {'player': 'Bo', 'count': 1, 'hands': '[[1, 1, 2, 3, 5, 6]]', 'time': 1721921350.3771122}

    print(r1)
    # [1, 1, 2, 3, 5, 6]

    r2 = player.roll()
    # SaveZonkHand: {'player': 'Bo', 'count': 2, 'hands': '[[1, 2, 2, 2, 5, 6], [1, 1, 2, 2, 3, 3]]', 'time': 1721921700.8632}
    # 3 Pair Zonk!
