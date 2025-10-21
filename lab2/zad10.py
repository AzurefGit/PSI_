# wtf is potok zadań
import aiohttp
import asyncio


async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main(path: str) -> None:
    url = "https://api.open-meteo.com/v1/forecast?latitude=10.95&longitude=-63.87&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    data = await fetch(url)
    data = str(data)
    with open(path, 'w', encoding="utf-8") as f:
        f.write(data)

if __name__ == "__main__":
    path = "D:/studia/rok 3/PSI_/lab2/plik.txt"
    asyncio.run(main(path))