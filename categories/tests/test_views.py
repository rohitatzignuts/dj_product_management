from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from categories.models import Category
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class CategoryAPITestCase(APITestCase):
    # Test suite for Category API endpoints

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="freeuser", password="password"
        )

        # Obtain the JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + self.access_token)

        self.category = Category.objects.create(
            name="Test Category",
            description="A sample category",
            created_by=self.user,
            updated_by=self.user,
        )

        self.valid_payload = {
            "name": "New Category",
            "description": "A newly created category",
            "created_by": self.user.id,
            "updated_by": self.user.id,
        }

        self.invalid_payload = {
            "name": "",
        }

    def test_get_all_categories(self):
        # get all categories

        url = reverse("categories")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Category")

    def test_create_valid_category(self):
        # Test creating a valid category

        url = reverse("categories")
        response = self.client.post(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Category")

    def test_create_invalid_category(self):
        # Test creating an invalid category

        url = reverse("categories")
        response = self.client.post(url, self.invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_get_single_category(self):
        # get a single category

        url = reverse("category", kwargs={"pk": self.category.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)

    def test_update_category(self):
        # update a category

        url = reverse("category", kwargs={"pk": self.category.pk})
        response = self.client.put(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "New Category")

    def test_delete_category(self):
        # delete a category

        url = reverse("category", kwargs={"pk": self.category.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_partial_update_category(self):
        # partial update a category

        partial_payload = {"name": "Partially Updated Category"}
        url = reverse("category", kwargs={"pk": self.category.pk})
        response = self.client.put(url, partial_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Partially Updated Category")

    def test_get_nonexistent_category(self):
        # get a category that does not exist

        url = reverse("category", kwargs={"pk": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
