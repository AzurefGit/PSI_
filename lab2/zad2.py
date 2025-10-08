import aiohttp
import asyncio


async def add_user(url: str, header: dict, body: dict) -> str:
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.post(url, data=body) as response:
            return await response.json()


async def main() -> None:
    url = "https://68e6851b21dd31f22cc5ffad.mockapi.io/api/v1/user"
    header = {"Token": "Bearer SOME_CHARS"}
    body = {
        "name": "Robert Kubica"
    }

    users = await add_user(url=url, header=header, body=body)
    print(users)


if __name__ == "__main__":
    asyncio.run(main())
