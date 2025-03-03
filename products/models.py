from django.db import models
from django.contrib.auth.models import User
from categories.models import Category


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    stock = models.IntegerField(default=10)
    price = models.FloatField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = ProductManager()
    all_objects = models.Manager()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products_created"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products_updated"
    )

    def delete(self, *args, **kwargs):
        """Soft delete instead of actual deletion."""
        self.is_deleted = True
        self.save()
