from django.db import models
from categories.models import Category
from django.contrib.auth.models import User


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


# Create your models here.
class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    all_objects = models.Manager()
    objects = SubCategoryManager()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subcategories_created"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subcategories_updated"
    )

    def delete(self, *args, **kwargs):
        """Soft delete instead of actual deletion."""
        self.is_deleted = True
        self.save()
