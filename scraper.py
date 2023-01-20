import aiohttp
import asyncio
import time
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor
from bs4 import BeautifulSoup

URL = 'https://www.10000recipe.com/recipe'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Whale/3.18.154.7 Safari/537.36'}


def parse_list(html):
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('a', class_='common_sp_link')
    urls = [
        f"{URL}/{result.attrs['href'].split('/')[-1]}" for result in results]
    return urls


def parse_recipe(html):
    soup = BeautifulSoup(html, "html.parser")
    try:
        title = soup.find('div', class_='view2_summary').find('h3').text
        ingredients = soup.find(
            'div', class_='ready_ingre3').find_all('li')
        res = []
        for ingredient in ingredients:
            res.append(ingredient.get_text().replace(
                '\n', '').replace(' ', '').replace('구매', ','))
        return {title: res}
    except AttributeError:
        pass


async def fetch(session, url):
    async with session.get(url, headers=headers) as response:
        html = await response.text()
        urls = parse_list(html)
        return urls


async def fetch_recipe(session, url):
    async with session.get(url, headers=headers) as response:
        html = await response.text()
        return html


async def search(keyword, page_number):
    urls = [
        f"{URL}/list.html?q={keyword}&order=reco&page={page}" for page in range(1, page_number+1)]
    pool = Pool(cpu_count())
    async with aiohttp.ClientSession() as session:
        recipe_urls = await asyncio.gather(*[fetch(session, url) for url in urls])
        recipe_urls = sum(recipe_urls, [])
        recipe_pages = await asyncio.gather(*[fetch_recipe(session, url) for url in recipe_urls])
        recipe = pool.starmap(parse_recipe, [(page,) for page in recipe_pages])
        print(recipe)


if __name__ == '__main__':
    start = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(search("김치찌개", 5))
    end = time.time()
    print("시간", end-start)  # 20초
