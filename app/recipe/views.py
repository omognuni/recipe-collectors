from recipe.pagination import RecipePagination
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer
from recipe.services import RecipeService
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


class RecipeView(APIView):
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination

    class FilterSerializer(serializers.Serializer):
        search = serializers.CharField()
        page = serializers.IntegerField()

    def get(self, request, *args, **kwargs):
        filter_serializer = self.FilterSerializer(data=request.data)
        filter_serializer.is_valid(raise_exception=True)

        service = RecipeService()

        recipes = service.get_recipe_list(filters=filter_serializer.validated_data)

        output_serializer = self.serializer_class(recipes, many=True)

        return Response(output_serializer.data, status=status.HTTP_200_OK)


class RecipeDetailView(APIView):
    serializer_class = RecipeDetailSerializer

    def get(self, request, pk, *args, **kwargs):

        service = RecipeService()

        recipe = service.get_recipe()

        return Response()


# class RecipeViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.RecipeDetailSerializer
#     queryset = Recipe.objects.all().prefetch_related(
#         'tags', Prefetch('ingredient_set'))
#     pagination_class = RecipePagination

#     def _url(self, tag, start, page):
#         url = 'https://www.10000recipe.com/recipe'
#         return [f"{url}/list.html?q={tag}&order=reco&page={p}" for p in range(start, page+3)]

#     def _run_celery_task(self, tag, start, page):
#         '''Celery task 실행'''
#         urls = self._url(tag, start, page)
#         recipe_urls = get_recipe_url.delay(urls)
#         indexes = recipe_urls.get()
#         group_res = group([get_recipe.s(index)
#                            for index in indexes['result']])()
#         recipes = group_res.join()
#         end = save_recipe.delay(recipes, tag)
#         end.get()

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return serializers.RecipeSerializer
#         return self.serializer_class

#     def get_queryset(self):
#         keyword = self.request.query_params.get('search')
#         # 페이지 없이 검색할 시 기본값으로 1
#         page = self.request.query_params.get('page', '1')
#         if not page.isdigit():
#             return
#         page = int(page)
#         if not keyword:
#             return self.queryset
#         queryset = self.queryset.filter(tags__name=keyword)
#         # queryset 크기가 page*page_size보다 작을 경우 부족한 만큼의 페이지 가져오기
#         start = len(queryset) // self.pagination_class.page_size
#         if start >= page:
#             return queryset
#         self._run_celery_task(keyword, start, page)

#         return self.queryset.filter(tags__name=keyword)
