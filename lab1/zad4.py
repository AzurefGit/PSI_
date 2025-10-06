import asyncio


async def main() -> None:
    i = 1
    while i < 6:
        print(i)
        i+=1
        await asyncio.sleep(1)


if __name__ == "__main__":
    with asyncio.Runner() as runner: 
        runner.run(main())