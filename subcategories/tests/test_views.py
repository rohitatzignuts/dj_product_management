from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from subcategories.models import SubCategory
from subcategories.models import Category
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class SubCategoryAPITestCase(APITestCase):
    # Test suite for SubCategory API endpoints

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

        self.subcategory = SubCategory.objects.create(
            name="Test Sub Category",
            parent_category=self.category,
            description="SubCategory Description",
            created_by=self.user,
            updated_by=self.user,
        )

        self.valid_payload = {
            "name": "New SubCategory",
            "parent_category": self.category.id,
            "description": "SubCategory Description",
            "created_by": self.user.id,
            "updated_by": self.user.id,
        }

        self.invalid_payload = {
            "name": "",
        }

    def test_get_all_subcategories(self):
        # get all sub categories

        url = reverse("subcategories")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Sub Category")

    def test_create_valid_subcategory(self):
        # Test creating a valid subcategory

        url = reverse("subcategories")
        response = self.client.post(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New SubCategory")

    def test_create_invalid_subcategory(self):
        # Test creating an invalid subcategory

        url = reverse("subcategories")
        response = self.client.post(url, self.invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_get_single_subcategory(self):
        # get a single subcategory

        url = reverse("subcategory", kwargs={"pk": self.subcategory.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.subcategory.name)

    def test_update_subcategory(self):
        # update a subcategory

        url = reverse("subcategory", kwargs={"pk": self.subcategory.pk})
        response = self.client.put(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "New SubCategory")

    def test_delete_subcategory(self):
        # delete a subcategory

        url = reverse("subcategory", kwargs={"pk": self.subcategory.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SubCategory.objects.count(), 0)

    def test_partial_update_subcategory(self):
        # partial update a subcategory

        partial_payload = {"name": "Partially Updated SubCategory"}
        url = reverse("subcategory", kwargs={"pk": self.subcategory.pk})
        response = self.client.put(url, partial_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Partially Updated SubCategory")

    def test_get_nonexistent_subcategory(self):
        # get a subcategory that does not exist

        url = reverse("subcategory", kwargs={"pk": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
