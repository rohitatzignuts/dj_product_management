from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.serializers import ProductSerializer
from products.models import Product
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProductsList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    @swagger_auto_schema(
        tags=["Products"],
        operation_summary="List all products",
        operation_description="Returns a list of all products available in the database.",
        responses={200: openapi.Response("Successful response")},
    )
    def get(self, request):
        filters = {}

        is_active = request.GET.get("is_active")
        category = request.GET.get("category")

        if is_active is not None:
            filters["is_active"] = is_active.lower() in ["true", "1"]

        if category is not None:
            filters["category"] = category

        products = Product.objects.filter(**filters).order_by("created_at")

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Products"],
        operation_summary="Add a new product",
        operation_description="Creates a new product in the database.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "price": openapi.Schema(type=openapi.TYPE_NUMBER),
                "category": openapi.Schema(type=openapi.TYPE_INTEGER),
                "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
        responses={200: openapi.Response("Successful response")},
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        tags=["Products"],
        operation_summary="Get a product",
        operation_description="Returns a product by its ID.",
        responses={200: openapi.Response("Successful response")},
    )
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Products"],
        operation_summary="Update a product",
        operation_description="Updates a product by its ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "price": openapi.Schema(type=openapi.TYPE_NUMBER),
                "category": openapi.Schema(type=openapi.TYPE_INTEGER),
                "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
    )
    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["Products"],
        operation_summary="Delete a product",
        operation_description="Deletes a product by its ID.",
        responses={204: openapi.Response("No content")},
    )
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
