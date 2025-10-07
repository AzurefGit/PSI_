import asyncio


async def maszyna_a() -> None:
    licznik = 0
    while licznik < 15:
        await asyncio.sleep(2)
        print("A pracuje")
        licznik += 2

async def maszyna_b() -> None:
    licznik = 0
    while licznik < 15:
        await asyncio.sleep(3)
        print("B pracuje")
        licznik += 3

async def maszyna_c() -> None:
    licznik = 0
    while licznik < 15:
        await asyncio.sleep(5)
        print("C pracuje")
        licznik += 5

async def main() -> None:
    await asyncio.gather(maszyna_a(), maszyna_b(), maszyna_c())

if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(main())