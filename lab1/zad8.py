import asyncio


async def wczytanie() -> None:
    await asyncio.sleep(2)
    print("Wczytywanie pliku zakończone")

async def analiza() -> None:
    await asyncio.sleep(4)
    print("Analiza pliku zakończona")

async def zapis() -> None:
    await asyncio.sleep(1)
    print("Zapis pliku zakończony")


async def main() -> None:
    await asyncio.gather(wczytanie(), analiza(), zapis())

if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(main())