from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL=reverse('recipe:ingredient-list')

class PublicIngredientsAPIlist(TestCase):
    def setUp(self):
        self.client=APIClient()

    def test_login_required(self):

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatIngredientAPI(TestCase):
    def setUp(self):
        self.user= get_user_model().objects.create_user(
            'mirza@test.com', 'passss'
        )
        self.client=APIClient()
        self.client.force_authenticate(self.user)

    def retrive_ingredient_list(self):

        Ingredient.objects.create(user=self.user, name='brasno')
        Ingredient.objects.create(user = self.user, name = 'kvasac')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')

        serializer = IngredientSerializer(ingredients, many= True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):

        user2 = get_user_model().objects.create_user('test@test.com', 'passsswordd')
        Ingredient.objects.create(user=user2, name='secer')
        ingredient = Ingredient.objects.create(user=self.user, name='luk')
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)


    def test_create_ingredient(self):
        payload = {'name':'test sastojak'}
        self.client.post(INGREDIENT_URL, payload)
        exists = Ingredient.objects.filter(user = self.user, name=payload['name']).exists()
        self.assertTrue(exists)

    def test_ingredient_invalid_name(self):
        payload = {'name':''}

        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)