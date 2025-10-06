import asyncio


async def korutyna1() -> None:
    await asyncio.sleep(3)
    print("korutyna 1")

async def korutyna2() -> None:
    await asyncio.sleep(1)
    print("korutyna 2")

async def main() -> None:
    await asyncio.gather(korutyna1(), korutyna2())


if __name__ == "__main__":
    with asyncio.Runner() as runner: 
        runner.run(main()) 
