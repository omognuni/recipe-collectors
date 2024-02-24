from recipe.models import Recipe
from recipe.run_task import run_celery_task


def get_recipe_list(page_size, filters=None):
    filters = filters or {}
    search = filters.get("search", None)
    page = int(filters.get("page", 1))

    queryset = Recipe.objects.all()
    if search is None:
        return queryset

    return get_additional_recipes(
        search=search, page=page, queryset=queryset, page_size=page_size
    )


def get_recipe(id):
    recipe = Recipe.objects.get(id=id)
    return recipe


def get_additional_recipes(search, page, queryset, page_size):
    """queryset 크기가 page*page_size보다 작을 경우 부족한 만큼의 페이지 가져오기"""
    filtered_queryset = queryset.filter(tags__name=search)
    offset = len(queryset) // page_size
    if offset >= page:
        return filtered_queryset

    run_celery_task(search, offset, page)
    filtered_queryset = queryset.filter(tags__name=search)
    return filtered_queryset
