import asyncio


async def krojenie() -> None:
    await asyncio.sleep(2)
    print("Krojenie warzyw zakończone")

async def gotowanie() -> None:
    await asyncio.sleep(5)
    print("Gotowanie makaronu zakończone")

async def smazenie() -> None:
    await asyncio.sleep(3)
    print("Smażenie mięsa zakończone")


async def main() -> None:
    await asyncio.gather(krojenie(), gotowanie(), smazenie())

if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(main())