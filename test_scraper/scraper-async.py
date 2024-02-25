import asyncio
import os
import time

import aiohttp
from bs4 import BeautifulSoup

URL = "https://www.10000recipe.com/recipe"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Whale/3.18.154.7 Safari/537.36"
}


def parse_list(html):
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all("a", class_="common_sp_link")
    urls = [f"{URL}/{result.attrs['href'].split('/')[-1]}" for result in results]
    return urls


def parse_recipe(html):
    soup = BeautifulSoup(html, "html.parser")
    try:
        title = soup.find("div", class_="view2_summary").find("h3").text
        ingredients = soup.find("div", class_="ready_ingre3").find_all("li")
        res = []
        for ingredient in ingredients:
            res.append(
                ingredient.get_text()
                .replace("\n", "")
                .replace(" ", "")
                .replace("구매", ",")
            )

        return {title: res}
    except AttributeError:
        pass


async def fetch(session, url):
    async with session.get(url, headers=headers) as response:
        html = await response.text()
        urls = parse_list(html)
        results = await asyncio.gather(*[fetch_recipe(session, url) for url in urls])
        return results


async def fetch_recipe(session, url):
    async with session.get(url, headers=headers) as response:
        html = await response.text()
        recipe = parse_recipe(html)
        return recipe


async def search(keyword, page_number):
    urls = [
        f"{URL}/list.html?q={keyword}&order=reco&page={page}"
        for page in range(1, page_number + 1)
    ]
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls])
        # print(results)


if __name__ == "__main__":
    start = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(search("김치찌개", 10))
    end = time.time()
    print("시간", end - start)  #
