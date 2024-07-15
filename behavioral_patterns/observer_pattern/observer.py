import asyncio
import weakref
from collections import defaultdict, deque

import aiohttp


class NewsPublisher:
    def __init__(self) -> None:
        self.channels = defaultdict(deque)
        self.subscribers: dict[str, list["NewsSubscriber"]] = defaultdict(list)
        self.flag = True

    def add_news(self, channel: str, url: str) -> None:
        self.channels[channel].append(url)

    def register(self, subscriber: "NewsSubscriber", channel: str) -> None:
        self.subscribers[channel].append(weakref.proxy(subscriber))

    def stop(self) -> None:
        self.flag = False

    async def notify(self) -> None:
        self.data_null_cnt = 0

        while self.flag:
            subs = []
            for channel in self.channels:
                try:
                    data = self.channels[channel].popleft()
                except IndexError:
                    self.data_null_cnt += 1
                    continue

                subscribers = self.subscribers[channel]
                for sub in subscribers:
                    print("Notifying", sub, "on channel", channel, "with data =>", data)
                    response = await sub.callback(data)
                    print("Response from", sub, "for channel", channel, "=>", response)
                    subs.append(sub)

            await asyncio.sleep(2)


class NewsSubscriber:
    def __init__(self) -> None:
        self.stories = {}
        self.futures = []
        self.future_status = {}
        self.flag = True

    async def callback(self, data: str):
        url = data
        print("Fetching URL", url, "...")
        future = aiohttp.request("GET", url)
        self.futures.append(future)

        return future

    async def fetch_urls(self):
        while self.flag:
            for future in self.futures:
                if self.future_status.get(future):
                    continue

                response: aiohttp.ClientResponse = await future
                data = await response.read()
                print("\t", self, "Got data for URL", response.url, "length:", len(data))
                self.stories[response.url] = data
                self.future_status[future] = 1

            await asyncio.sleep(2)


"""
뉴스 구독자는 자신의 관심 뉴스 채널을 등록하고 URL을 뉴스 기사로 소비함.
구독자들은 URL을 얻으면 비동기적으로 URL의 데이터를 가져옴.
게시자의 구독자 통보 역시 비동기적으로 발생함.

게시자의 notify 메서드는 비동기적임.
채널 목록을 통해 각 채널의 구독자를 찾아 callback 메서드를 사용해, 구독자를 다시 호출해 채널의 가장 최신 데이터를 제공함.

callback 메서드는 자체가 비동기적이며 future 객체를 반환하고 최종 결과를 반환하지 않음.
future의 추가적인 처리는 구독자의 fetch_urls 메서드 내부에서 비동기적으로 발생함.

callback과 fetch_urls 메서드 모두 비동기식으로 선언됨.
callback 메서드는 단순히 게시자에서 future를 반환하는 aiohttp 모듈의 GET 메서드로 URL을 전달함.
future는 fetch_urls 메서드를 통해 URL 데이터를 얻기 위해, 다시 비동기적으로 처리되는 futures의 로컬 목록에 추가됨.
그 다음 URL을 키로 갖는 로컬 기사 딕셔너리에 추가됨.
"""

if __name__ == "__main__":
    publisher = NewsPublisher()
    publisher.add_news("sports", "https://m.sports.naver.com/kfootball/article/022/0003950904")
    publisher.add_news("sports", "https://m.sports.naver.com/wfootball/article/001/0014808259")
    publisher.add_news("korea", "https://www.hankyung.com/article/2024071552407")

    subscriber1 = NewsSubscriber()
    subscriber2 = NewsSubscriber()
    publisher.register(subscriber1, "sports")
    publisher.register(subscriber2, "korea")

    loop = asyncio.get_event_loop()

    tasks = map(lambda x: x.fetch_urls(), (subscriber1, subscriber2))
    loop.run_until_complete(asyncio.wait([publisher.notify(), *tasks], timeout=30))

    print("Ending loop")
    loop.close()

    """
    Notifying <__main__.NewsSubscriber object at 0x1030026e0> on channel sports with data => https://m.sports.naver.com/kfootball/article/022/0003950904
    Fetching URL https://m.sports.naver.com/kfootball/article/022/0003950904 ...
    Response from <__main__.NewsSubscriber object at 0x1030026e0> for channel sports => <aiohttp.client._SessionRequestContextManager object at 0x103cce640>

    Notifying <__main__.NewsSubscriber object at 0x103ab5f60> on channel korea with data => https://www.hankyung.com/article/2024071552407
    Fetching URL https://www.hankyung.com/article/2024071552407 ...
    Response from <__main__.NewsSubscriber object at 0x103ab5f60> for channel korea => <aiohttp.client._SessionRequestContextManager object at 0x1045d8300>

    Notifying <__main__.NewsSubscriber object at 0x1030026e0> on channel sports with data => https://m.sports.naver.com/wfootball/article/001/0014808259
    Fetching URL https://m.sports.naver.com/wfootball/article/001/0014808259 ...
    Response from <__main__.NewsSubscriber object at 0x1030026e0> for channel sports => <aiohttp.client._SessionRequestContextManager object at 0x1045d8780>

    Ending loop
    Task was destroyed but it is pending!
    task: <Task pending name='Task-3' coro=<NewsPublisher.notify() done, defined at /Users/eddiek/workspace/github/design-pattern/behavioral_patterns/observer_pattern/observer.py:24> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    sys:1: RuntimeWarning: coroutine 'ClientSession._request' was never awaited
    Unclosed client session
    client_session: <aiohttp.client.ClientSession object at 0x1045d4550>
    Unclosed client session
    client_session: <aiohttp.client.ClientSession object at 0x1045d41c0>
    Unclosed client session
    client_session: <aiohttp.client.ClientSession object at 0x1045d4370>
    """
