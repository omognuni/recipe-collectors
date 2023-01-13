import time
import aiohttp
import os
import asyncio
import requests
from multiprocessing import Pool, cpu_count
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


def fetch(session, url):
    with session.get(url, headers=headers) as response:
        html = response.text
        urls = parse_list(html)
        results = [fetch_recipe(session, url) for url in urls]
        return results


def fetch_recipe(session, url):
    with session.get(url, headers=headers) as response:
        html = response.text
        recipe = parse_recipe(html)
        return recipe


def search(keyword, page_number):
    urls = [f"{URL}/list.html?q={keyword}&order=reco&page={page}" for page in range(
        1, page_number+1)]
    pool = Pool(cpu_count())
    with requests.Session() as session:
        results = pool.starmap_async(
            fetch, [(session, url) for url in urls])
        print(len(results.get()))
    pool.close()


if __name__ == '__main__':
    start = time.time()
    search("김치찌개", 10)
    end = time.time()
    print("시간", end-start)  # 초
