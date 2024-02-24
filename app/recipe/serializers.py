from recipe.models import Ingredient, Recipe, Tag
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ["name", "number", "unit"]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["name"]


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "index", "title", "process", "tags"]
        read_only_fields = ["id", "index", "title", "process", "tags"]


class RecipeDetailSerializer(RecipeSerializer):
    ingredients = IngredientSerializer(
        source="ingredient_set", many=True, required=False
    )

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["ingredients"]
