import asyncio

import aiohttp

urls = ['https://news.sina.com.cn/w/2022-02-08/doc-ikyakumy4746398.shtml',
        'https://news.sina.com.cn/c/2022-02-08/doc-ikyamrmz9575177.shtml',
        'https://news.sina.com.cn/c/2022-02-08/doc-ikyamrmz9565897.shtml',
        'https://video.sina.com.cn/p/news/2022-02-08/detail-ikyamrmz9562171.d.html',
        'https://news.sina.com.cn/c/2022-02-08/doc-ikyakumy4751058.shtml',
        'https://news.sina.com.cn/c/2022-02-08/doc-ikyamrmz9562195.shtml',
        'https://video.sina.com.cn/p/news/2022-02-08/detail-ikyamrmz9565319.d.html',
        'https://news.sina.com.cn/o/2022-02-08/doc-ikyamrmz9563673.shtml',
        'https://news.sina.cn/zt_d/springtransportation',
        'https://news.sina.com.cn/w/2022-02-08/doc-ikyakumy4722823.shtml',
        'https://news.sina.com.cn/w/2022-02-08/doc-ikyakumy4735050.shtml',
        'https://news.sina.com.cn/c/2022-02-07/doc-ikyakumy4701160.shtml',
        'https://video.sina.com.cn/p/news/2022-02-07/detail-ikyamrmz9515046.d.html',
        'https://news.sina.com.cn/c/2022-02-07/doc-ikyamrmz9532965.shtml',
        'https://news.sina.com.cn/c/2022-02-08/doc-ikyamrmz9535092.shtml',
        'https://finance.sina.com.cn/roll/2022-02-08/doc-ikyamrmz9544365.shtml',
        'https://finance.sina.com.cn/chanjing/cyxw/2022-02-08/doc-ikyakumy4706578.shtml',
        'https://video.sina.com.cn/p/news/2022-02-06/detail-ikyamrmz9326557.d.html']


async def main(pool):
    sem = asyncio.Semaphore(pool)
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(control_sem(sem, uri, session)) for uri in urls]
        await asyncio.wait(tasks)


async def control_sem(sem, url, session):
    async with sem:
        await fetch(url, session)


async def fetch(url, session):
    async with session.get(url) as resp:
        result = resp.status
        print(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(pool=10))
