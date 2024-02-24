import requests
from celery import shared_task
from recipe.parser import parse_list, parse_recipe
from recipe.services import save_recipes
from requests.exceptions import ConnectionError

URL = "https://www.10000recipe.com/recipe"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Whale/3.18.154.7 Safari/537.36"
}


def get_url_by_tag_and_page(tag, start, page):
    return [
        f"{URL}/list.html?q={tag}&order=reco&page={p}" for p in range(start, page + 3)
    ]


@shared_task
def get_recipe_url(urls):
    """레시피 목록에서 각 레시피 url 가져오기"""
    result = []
    for url in urls:
        try:
            response = requests.get(url)
            res = parse_list(response.text)
            result += res
        except ConnectionError:
            pass
    return {"result": result}


@shared_task
def save_recipes_concurrent(results, tag):
    save_recipes(results, tag)


@shared_task
def get_recipe(index):
    """레시피 url에서 레시피 크롤링"""
    try:
        response = requests.get(f"{URL}/{index}", headers=headers)
        res = parse_recipe(response.text)
        if not res:
            return
        res.update({"index": index})
        return res
    except ConnectionError:
        return


@shared_task
def get_recipes(indexes):
    results = []

    for index in indexes:
        try:
            response = requests.get(f"{URL}/{index}", headers=headers)
            res = parse_recipe(response.text)
            if not res:
                continue
            res.update({"index": index})
            results.append(res)
        except ConnectionError:
            pass
    return {"results": results}
