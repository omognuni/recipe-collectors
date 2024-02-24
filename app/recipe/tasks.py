from celery import group
from core.tasks import get_recipe, get_recipe_url, save_recipe

URL = "https://www.10000recipe.com/recipe"


def get_url_by_tag_and_page(tag, start, page):
    return [
        f"{URL}/list.html?q={tag}&order=reco&page={p}" for p in range(start, page + 3)
    ]


def run_celery_task(tag, start, page):
    """Celery task 실행"""
    urls = get_url_by_tag_and_page(tag, start, page)
    recipe_urls = get_recipe_url.delay(urls)
    indexes = recipe_urls.get()
    group_res = group([get_recipe.s(index) for index in indexes["result"]])()
    recipes = group_res.join()
    end = save_recipe.delay(recipes, tag)
    end.get()
