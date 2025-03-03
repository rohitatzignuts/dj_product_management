from django.db import models
from django.contrib.auth.models import User


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    all_objects = models.Manager()
    objects = CategoryManager()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="categories_created"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="categories_updated"
    )

    def delete(self, *args, **kwargs):
        """Soft delete instead of actual deletion."""
        self.is_deleted = True
        self.save()
