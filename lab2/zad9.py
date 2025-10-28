import aiohttp
import asyncio


async def fetch(url: str, session: aiohttp.ClientSession) -> str:
    a = 0
    limit = 3
    while a <= limit:
        async with session.get(url) as response:
            if 200 <= response.status >= 299:
                return response

            elif 500 <= response.status >= 999:
                a += 1
                if a <= limit:
                    print("Błąd serwera")
                    await asyncio.sleep(0.5)
                    continue
                else:
                    print("Błąd")
                    return None



async def main() -> None:
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(url, session) for _ in range(100)]
        results = await asyncio.gather(*tasks)
        print(results)


if __name__ == "__main__":
    asyncio.run(main())
