import aiohttp
import asyncio


async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def midTemp(url: str) -> float:
    sum = 0
    for el in url["hourly"]["temperature_2m"]:
        sum+=el
    return sum / len(url["hourly"]["temperature_2m"])

async def main() -> None:
    url_porlamar = "https://api.open-meteo.com/v1/forecast?latitude=10.95&longitude=-63.87&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    url_moroni = "https://api.open-meteo.com/v1/forecast?latitude=-11.70&longitude=43.25&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    url_helsinki = "https://api.open-meteo.com/v1/forecast?latitude=60.16&longitude=24.94&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    sites = await asyncio.gather(fetch(url_porlamar), fetch(url_moroni), fetch(url_helsinki))

    cities = {
        "Helsinki": sites[0]["current"],
        "Moroni": sites[1]["current"],
        "Porlamar": sites[2]["current"]
    }

    cities_copy = cities.copy()

    cities_sorted = dict(sorted(cities_copy.items(), key=lambda item: item[1]["temperature_2m"], reverse=True))

    print(cities_sorted)

if __name__ == "__main__":
    asyncio.run(main())
