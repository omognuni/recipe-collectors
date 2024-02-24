from django.db import transaction
from django.db.utils import DatabaseError
from recipe.models import Ingredient, Recipe, Tag


def save_recipes(results, tag):
    """크롤링한 레시피 데이터 저장"""
    for res in results:
        try:
            with transaction.atomic():
                recipe, _ = Recipe.objects.update_or_create(
                    index=res["index"], title=res["title"], process=res["process"]
                )
                tag_obj, _ = Tag.objects.get_or_create(name=tag)
                recipe.tags.add(tag_obj)
                recipe.save()
                ingredients = res["ingredients"]
                for ing in ingredients:
                    ingredient, _ = Ingredient.objects.update_or_create(
                        recipe=recipe, **ing
                    )
                    ingredient.save()
        except (DatabaseError, TypeError, Exception):
            pass
    return
