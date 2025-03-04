from djoser.serializers import UserCreateSerializer
from django.contrib.auth.models import User
from categories.models import Category
from rest_framework import serializers
from subcategories.serializers import SubCategorySerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username", "password", "first_name", "last_name")


class CategorySerializer(serializers.ModelSerializer):

    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"required": False},
            "updated_by": {"required": False},
            "is_deleted": {"read_only": True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user:
            validated_data["created_by"] = request.user
            validated_data["updated_by"] = request.user
        return super().create(validated_data)
