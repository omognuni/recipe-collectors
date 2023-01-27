from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def create_recipe(index='1', title='test', process='test1.test2.test3'):
    return Recipe.objects.create(index=index, title=title, process=process)


class PrivateAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com', password='testpass')
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        create_recipe()
        create_recipe(index='2')

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    @patch('celery.group.apply_async')
    @patch('core.tasks.get_recipe_url.delay')
    @patch('core.tasks.save_recipe.delay')
    def test_search_recipe(self, save_recipe, get_recipe_url, group):
        recipe = create_recipe()
        tag = Tag.objects.create(name='test')
        Ingredient.objects.create(
            name='kimchi', number='1', unit='포기', recipe=recipe)
        recipe.tags.add(tag)

        params = {'search': 'test', 'page': '1'}
        res = self.client.get(RECIPE_URL, params)

        recipe = Recipe.objects.filter(tags__name='test')
        serializer = RecipeSerializer(recipe, many=True)

        group.assert_called()
        get_recipe_url.assert_called()
        save_recipe.assert_called()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
