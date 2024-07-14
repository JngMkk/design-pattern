import gc
import weakref

from creational_patterns.factory_pattern.factory import Engineer

"""
파이썬에서 약한 참조(weak reference) 모듈은 클래스 인스턴스에 관한 접근을 프록시 처리해 구현한 기능과 매우 유사한 기능을 수행하는 프록시 객체를 제공함.
"""


if __name__ == "__main__":
    engineer = Engineer("Kang", 25, "M")
    print(len(gc.get_referrers(engineer)))  # 1

    engineer_proxy = weakref.proxy(engineer)
    print(engineer_proxy)  # Engineer - Kang, 25 years old M
    print(engineer_proxy.get_role())  # engineering

    # weakref 프록시는 프록시되는 객체의 참조 횟수를 증가시키지 않음.
    print(len(gc.get_referrers(engineer)))  # 1
