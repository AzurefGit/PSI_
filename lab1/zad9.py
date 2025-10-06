import asyncio


async def maszyna_a() -> None:
    await asyncio.sleep(2)
    print("A pracuje")

async def maszyna_b() -> None:
    await asyncio.sleep(3)
    print("B pracuje")

async def maszyna_c() -> None:
    await asyncio.sleep(5)
    print("C pracuje")

async def main() -> None:
    await asyncio.gather(maszyna_a(), maszyna_b(), maszyna_c())
    await asyncio.gather(maszyna_a(), maszyna_b(), maszyna_c())
    await asyncio.gather(maszyna_a(), maszyna_b(), maszyna_c())

if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(main())