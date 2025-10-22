import aiohttp
import asyncio


async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if 200 <= response.status >= 299:
                return await response
            elif 500 <= response.status >= 999:
                fetch(url)


async def main() -> None:
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    i = 0
    while i < 100:
        weather = await fetch(url)
        print(weather["current"])
        i += 1


if __name__ == "__main__":
    asyncio.run(main())
