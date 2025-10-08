import aiohttp
import asyncio


async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text(encoding="utf-8")


async def main() -> None:
    ## Rozwiązanie 1
    # gov = await fetch("https://www.gov.pl/")
    # wiki = await fetch("https://www.wikipedia.org/")
    # yt = await fetch("https://www.youtube.com/")
    # teams = await fetch("https://www.microsoft.com/pl-pl/microsoft-teams/log-in")
    # ex = await fetch("https://example.com/")
    #
    # print(gov, wiki, yt, teams, ex)

    ## Rozwiązanie 2
    sites = await asyncio.gather(fetch("https://www.gov.pl/"),
                                 fetch("https://www.wikipedia.org/"),
                                 fetch("https://www.youtube.com/"),
                                 fetch("https://www.microsoft.com/pl-pl/microsoft-teams/log-in"),
                                 fetch("https://example.com/"))
    print(sites)


if __name__ == "__main__":
    asyncio.run(main())
