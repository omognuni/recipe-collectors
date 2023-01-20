from core.tasks import *

URL = 'https://www.10000recipe.com/recipe'

urls = [
    f"{URL}/list.html?q=김치찌개&order=reco&page={page}" for page in range(1, 3)]

recipe_indexes = get_recipe_url.delay(urls)
result = get_recipe.delay(recipe_indexes.get()['result'])
result = save_recipe.delay(result.get())
