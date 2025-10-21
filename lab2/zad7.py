import aiohttp
import asyncio


async def fetch(url: str) -> bin:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            return content

async def main(path: str) -> None:
    url = "https://media.istockphoto.com/id/1322104312/photo/freedom-chains-that-transform-into-birds-charge-concept.jpg?s=612x612&w=0&k=20&c=e2XUx498GotTLJn_62tPmsqj6vU48ZEkf0auXi6Ywh0="
    download = await fetch(url)
    with open(path, 'wb') as f:
        f.write(download)


if __name__ == "__main__":
    path = "D:/studia/rok 3/PSI_/lab2/plik.jpg"
    asyncio.run(main(path))