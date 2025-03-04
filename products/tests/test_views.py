from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from products.models import Product
from products.models import Category
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class ProductAPITestCase(APITestCase):
    # Test suite for Product API endpoints

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

        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=10.99,
            stock=55,
            description="Product Description",
            created_by=self.user,
            updated_by=self.user,
        )

        self.valid_payload = {
            "name": "New Product",
            "price": 10.99,
            "stock": 55,
            "category": self.category.id,
            "description": "Product Description",
            "created_by": self.user.id,
            "updated_by": self.user.id,
        }

        self.invalid_payload = {
            "name": "Test Product",
        }

    def test_get_all_products(self):
        # get all products

        url = reverse("products")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Product")

    def test_create_valid_product(self):
        # Test creating a valid product

        url = reverse("products")
        response = self.client.post(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Product")

    def test_create_invalid_product(self):
        # Test creating an invalid product

        url = reverse("products")
        response = self.client.post(url, self.invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_get_single_product(self):
        # get a single product

        url = reverse("product", kwargs={"pk": self.product.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_update_product(self):
        # update a product

        url = reverse("product", kwargs={"pk": self.product.pk})
        response = self.client.put(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "New Product")

    def test_delete_product(self):
        # delete a product

        url = reverse("product", kwargs={"pk": self.product.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_partial_update_product(self):
        # partial update a product

        partial_payload = {"name": "Partially Updated Product"}
        url = reverse("product", kwargs={"pk": self.product.pk})
        response = self.client.put(url, partial_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Partially Updated Product")

    def test_get_nonexistent_product(self):
        # get a product that does not exist

        url = reverse("product", kwargs={"pk": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
