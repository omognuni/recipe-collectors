from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from django.db.models import Prefetch
from django.db import transaction

from celery import group
from core.tasks import *
from core.models import Recipe
from recipe import serializers


class RecipePagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    max_page_size = 40


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all().prefetch_related(
        'tags', Prefetch('ingredient_set'))
    pagination_class = RecipePagination

    def _url(self, tag, page):
        url = 'https://www.10000recipe.com/recipe'
        return [f"{url}/list.html?q={tag}&order=reco&page={p}" for p in range(page, page+2)]

    def _run_celery_task(self, tag, page):
        urls = self._url(tag, page)
        recipe_urls = get_recipe_url.delay(urls)
        indexes = recipe_urls.get()
        group_res = group([get_recipe.s(index)
                           for index in indexes['result']])()
        recipes = group_res.join()
        end = save_recipe.delay(recipes, tag)
        end.get()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def get_queryset(self):
        keyword = self.request.query_params.get('search')
        page = int(self.request.query_params.get('page', 1))
        if not keyword:
            return self.queryset
        queryset = self.queryset.filter(tags__name=keyword)
        if len(queryset) >= RecipePagination.page_size * page:
            return queryset
        self._run_celery_task(keyword, page)

        return self.queryset.filter(tags__name=keyword)
