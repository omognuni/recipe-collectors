from rest_framework import viewsets, status
from rest_framework.response import Response
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

    def _url(self, tag, start, page):
        url = 'https://www.10000recipe.com/recipe'
        return [f"{url}/list.html?q={tag}&order=reco&page={p}" for p in range(start, page+3)]

    def _run_celery_task(self, tag, start, page):
        '''Celery task 실행'''
        urls = self._url(tag, start, page)
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
        # 페이지 없이 검색할 시 기본값으로 1
        page = self.request.query_params.get('page', '1')
        if not page.isdigit():
            return
        page = int(page)
        if not keyword:
            return self.queryset
        queryset = self.queryset.filter(tags__name=keyword)
        # queryset 크기가 page*page_size보다 작을 경우 부족한 만큼의 페이지 가져오기
        start = len(queryset) // self.pagination_class.page_size
        if start >= page:
            return queryset
        self._run_celery_task(keyword, start, page)

        return self.queryset.filter(tags__name=keyword)
