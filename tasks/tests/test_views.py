from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tasks.models import Task
from categories.models import Category
from products.models import Product
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TaskAPITestCase(APITestCase):
    # Test suite for Task API endpoints

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

        self.task = Task.objects.create(
            title="Test Task",
            description="Task Description",
            product=self.product,
            assigned_user=self.user,
            status="pending",
            due_date="2025-03-31",
        )

        self.valid_payload = {
            "title": "Test Valid Task",
            "description": "Task Valid Description",
            "product": self.product.id,
            "assigned_user": self.user.id,
            "status": "pending",
            "due_date": "2025-03-31",
        }

        self.invalid_payload = {
            "title": "",
        }

    def test_get_all_tasks(self):
        # get all tasks

        url = reverse("tasks")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Task")

    def test_create_valid_task(self):
        # Test creating a valid task

        url = reverse("tasks")
        response = self.client.post(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test Valid Task")

    def test_create_invalid_task(self):
        # Test creating an invalid task
        url = reverse("tasks")
        response = self.client.post(url, self.invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_get_single_task(self):
        # get a single task

        url = reverse("task", kwargs={"pk": self.task.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task.title)

    def test_update_task(self):
        # update a task

        url = reverse("task", kwargs={"pk": self.task.pk})
        response = self.client.put(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Valid Task")

    def test_delete_task(self):
        # delete a task

        url = reverse("task", kwargs={"pk": self.task.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_partial_update_task(self):
        # partial update a task

        partial_payload = {"title": "Partially Updated Task"}
        url = reverse("task", kwargs={"pk": self.task.pk})
        response = self.client.put(url, partial_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Partially Updated Task")

    def test_get_nonexistent_task(self):
        # get a task that does not exist

        url = reverse("task", kwargs={"pk": 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
