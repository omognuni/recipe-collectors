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
