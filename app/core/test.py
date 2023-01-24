from core.tasks import *
import time
from celery import chain, group

URL = 'https://www.10000recipe.com/recipe'

page_urls = [
    f"{URL}/list.html?q=김치찌개&order=reco&page={page}" for page in range(1, 3)]

recipe_urls = get_recipe_url.delay(page_urls)

start = time.time()
indexes = recipe_urls.get()
group_res = group([get_recipe.s(index) for index in indexes['result']])()
recipes = group_res.join()
save_result = save_recipe.delay(recipes)
end = time.time()
print("group:", end-start)
