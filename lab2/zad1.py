import aiohttp
import asyncio


async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text(encoding="utf-8")


async def main() -> None:
    url = "https://www.gov.pl/"
    users = await fetch(url)
    print(users)


if __name__ == "__main__":
    asyncio.run(main())
