from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from core.tasks import *
from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers


class RecipePagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    max_page_size = 40


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all().prefetch_related('tags', 'ingredient_set')
    pagination_class = RecipePagination

    def _url(self, tag, page):
        page = int(page)
        url = 'https://www.10000recipe.com/recipe'
        return [f"{url}/list.html?q={tag}&order=reco&page={p}" for p in range(page, page+2)]

    def _run_celery_task(self, tag, page):
        urls = self._url(tag, page)
        recipe_urls = get_recipe_url.delay(urls)
        indexes = recipe_urls.get()
        group_res = group([get_recipe.s(index)
                           for index in indexes['result']])()
        recipes = group_res.join()
        save_result = save_recipe.delay(recipes, tag)
        return save_result

    def get_queryset(self):
        keyword = self.request.query_params.get('search')
        page = self.request.query_params.get('page')
        if not keyword:
            return self.queryset
        queryset = self.queryset.filter(tags__name=keyword)
        if len(queryset) >= RecipePagination.page_size * int(page):
            return queryset
        self._run_celery_task(keyword, page)

        return self.queryset.filter(tags__name=keyword)
