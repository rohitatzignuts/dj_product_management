from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class TaskManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("inprogress", "In Progress"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tasks")
    assigned_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks_assigned"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)
    all_objects = models.Manager()
    objects = TaskManager()

    def delete(self, *args, **kwargs):
        """Soft delete instead of actual deletion."""
        self.is_deleted = True
        self.save()
