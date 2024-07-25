"""
GUI 외부에서 옵저버 패턴은 객체의 중간 상태를 저장하는 데 유용함.
옵저버 객체를 사용하면 변경에 대해 엄격한 감사가 요구되는 시스템에서 편리할 수 있음.

복잡한 클라우드 기반 애플리케이션은 불안정한 연결로 인해 혼돈 문제를 겪을 수 있음.
옵저버를 사용하면 상태 변경을 기록해 복구 및 재시작을 더 쉽게 할 수 있음.

이 예제에서는 중요한 값들의 컬렉션을 유지 관리하는 코어 객체를 정의한 다음 하나 이상의 옵저버가 해당 객체의 직렬화된 복사본을 만들도록 함.
이 복사본은 데이터베이스, 원격 호스트, 또는 로컬 파일에 저장될 수 있음.
많은 옵저버를 가질 수 있기 때문에 서로 다른 데이터 캐시를 사용하도록 디자인을 수정하는 것은 쉬움.

이 예제에서는 Zonk, Zilch 또는 Ten Thousand라고 불리는 주사위 게임에 대해 생각할 것임.
이 게임에서 플레이어는 6개의 주사위를 굴리고, 트리플과 런 등에 대해 점수를 얻고, 아마도 특정 시퀀스를 얻기 위해 주사위의 일부 또는 전체를 다시 굴릴 것임.
"""

from __future__ import annotations

from typing import Protocol


class Observer(Protocol):
    """
    Observer 클래스는 프로토콜로서 옵저버를 위한 추상 상위 클래스임. 이것을 abc.ABC 추상클래스로 공식화하지 않음.
    이는 abc 모듈이 제공하는 런타임 오류에 의존하지 않기 위함.
    Protocol을 정의할 때 모든 옵저버가 실제로 요구되는 메서드를 구현했는지 확인하기 위해 mypy에 의존함.
    """

    def __call__(self) -> None: ...  # noqa


class Observable:
    """
    Observable 클래스는 _observers 인스턴스 변수와 이 프로토콜 정의의 pure 부분인 세 가지 메서드를 정의함.
    관찰 가능한 객체는 옵저버를 추가 및 제거할 수 잇으며, 가장 중요한 것으로 모든 옵저버에 상태 변경을 알릴 수 있음.
    코어 클래스가 특별히 다르게 수행해야 하는 유일한 것은 상태 변경이 있을 때 _notify_observers() 메서드를 호출하는 것.
    적절한 알림은 관찰 가능한 객체에 대한 디자인에서 중요한 부분.
    """

    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer()
