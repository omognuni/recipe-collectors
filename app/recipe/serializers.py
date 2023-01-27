from rest_framework import serializers

from core.models import Recipe, Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['index', 'title', 'process', 'tags']
        read_only_fields = ['index', 'title', 'process', 'tags']
