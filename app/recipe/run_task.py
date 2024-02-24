from celery import group
from core.tasks import (
    get_recipe,
    get_recipe_url,
    get_url_by_tag_and_page,
    save_recipes_concurrent,
)


def run_celery_task(tag, start, page):
    """Celery task 실행"""
    urls = get_url_by_tag_and_page(tag, start, page)
    recipe_urls = get_recipe_url.delay(urls)
    indexes = recipe_urls.get()
    group_res = group([get_recipe.s(index) for index in indexes["result"]])()
    recipes = group_res.join()
    end = save_recipes_concurrent.delay(recipes, tag)
    end.get()
