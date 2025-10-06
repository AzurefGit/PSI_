import asyncio


async def main(n) -> None:
    i1 = 0
    i2 = 1

    for _ in range(n):
        temp = i1
        i1 = i2
        i2 += temp
        print(i1)
        await asyncio.sleep(1)

if __name__ == "__main__":
    with asyncio.Runner() as runner: 
        runner.run(main(10))