import asyncio


async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got id')


async def main():
    event = asyncio.Event()

    waiter_task = asyncio.create_task(waiter(event))

    await asyncio.sleep(1)
    event.set()

    await waiter_task


asyncio.run(main())
