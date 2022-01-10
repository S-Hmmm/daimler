import asyncio
import concurrent.futures
from time import sleep


def blocking_io():
    sleep(1)
    return 'blocking_io'


def cup_bound():
    return sum(i * i for i in range(10 ** 7))


async def main():
    loop = asyncio.get_running_loop()

    result = await loop.run_in_executor(None, blocking_io)
    print('default thread pool', result)

    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_io)
        print('custom thread pool', result)

    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cup_bound)
        print('custom process pool', result)


if __name__ == '__main__':
    asyncio.run(main())
