from djoser.serializers import UserCreateSerializer
from django.contrib.auth.models import User
from products.models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
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
