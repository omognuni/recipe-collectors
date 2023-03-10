from core.tasks import *
from core.models import *
import time
from celery import group

URL = 'https://www.10000recipe.com/recipe'

tag = '김치찌개'
page_urls = [
    f"{URL}/list.html?q={tag}&order=reco&page={page}" for page in range(1, 3)]

Recipe.objects.all().delete()
Ingredient.objects.all().delete()
Tag.objects.all().delete()


start = time.time()
recipe_urls = get_recipe_url.delay(page_urls)
indexes = recipe_urls.get()
group_res = group([get_recipe.s(index) for index in indexes['result']])()
recipes = group_res.join()
save_result = save_recipe.delay(recipes, tag)
save_result.get()
end = time.time()
group_time = end-start

Recipe.objects.all().delete()
Ingredient.objects.all().delete()
Tag.objects.all().delete()


start = time.time()
recipe_urls = get_recipe_url.delay(page_urls)
indexes = recipe_urls.get()
res = get_recipes.delay(indexes['result'])
recipes = res.get()['results']
save_result = save_recipe.delay(recipes, tag)
save_result.get()
end = time.time()
chain_time = end-start

print("group:", group_time)  # 9.7초
print("chain:", chain_time)  # 48.6초
