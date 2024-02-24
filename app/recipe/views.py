from recipe.pagination import RecipePagination
from recipe.selectors import get_recipe, get_recipe_list
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


class RecipeView(APIView):
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination

    class FilterSerializer(serializers.Serializer):
        search = serializers.CharField(required=False)
        page = serializers.IntegerField(required=False)

    def get(self, request, *args, **kwargs):
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        paginator = self.pagination_class()

        recipes = get_recipe_list(
            page_size=paginator.page_size, filters=filter_serializer.validated_data
        )
        recipes = paginator.paginate_queryset(recipes, request)

        output_serializer = self.serializer_class(recipes, many=True)

        return Response(output_serializer.data, status=status.HTTP_200_OK)


class RecipeDetailView(APIView):
    serializer_class = RecipeDetailSerializer

    def get(self, request, id, *args, **kwargs):

        recipe = get_recipe(id)

        output_serializer = self.serializer_class(recipe)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


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
