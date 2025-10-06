import asyncio


async def fetch(delay: int) -> int:
    await asyncio.sleep(delay)
    print(delay)
    return delay

async def main() -> None:
    await asyncio.gather(fetch(3), fetch(2), fetch(5))

if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(main())