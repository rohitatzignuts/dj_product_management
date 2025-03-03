from djoser.serializers import UserCreateSerializer
from django.contrib.auth.models import User
from tasks.models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        extra_kwargs = {
            "is_deleted": {"read_only": True},
        }
