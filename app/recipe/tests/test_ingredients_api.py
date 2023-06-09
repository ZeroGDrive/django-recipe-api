"""
Test the ingredients API
"""


from core.models import Ingredient
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import IngredientSerializer
from rest_framework import status
from rest_framework.test import APIClient

INGREDIENTS_URL = reverse("recipe:ingredient-list")


def create_user(email="user@example.com", password="testpass"):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(ingredient_id):
    """Helper function to return ingredient detail URL"""
    return reverse("recipe:ingredient-detail", args=[ingredient_id])


class PublicIngredientsApiTests(TestCase):
    """Tests the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required"""

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """Test retrieving a list of ingredients"""

        Ingredient.objects.create(user=self.user, name="Kale")
        Ingredient.objects.create(user=self.user, name="Salt")

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user are returned"""

        user2 = create_user(email="user2@example.com", password="testpass")

        Ingredient.objects.create(user=user2, name="Vinegar")
        ingredient = Ingredient.objects.create(user=self.user, name="Tumeric")

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)

    def test_update_ingredient(self):
        """Test updating an ingredient"""

        ingredient = Ingredient.objects.create(user=self.user, name="Vinegar")

        payload = {"name": "Apple Cider Vinegar"}

        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(res.data["name"], payload["name"])

    def test_delete_ingredient(self):
        """Test deleting an ingredient"""
        ingredient = Ingredient.objects.create(user=self.user, name="Vinegar")
        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(id=ingredient.id))
