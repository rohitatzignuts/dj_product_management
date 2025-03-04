from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from categories.serializers import CategorySerializer
from categories.models import Category
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import Http404
from rest_framework.throttling import UserRateThrottle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=205)
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=400)


class CategoriesList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    @swagger_auto_schema(
        tags=["Categories"],
        operation_summary="List all categories",
        operation_description="Returns a list of all categories available in the database.",
        responses={200: openapi.Response("Successful response")},
    )
    def get(self, request):
        categories = Category.objects.all().order_by("created_at")
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Categories"],
        operation_summary="Add a new category",
        operation_description="Creates a new category in the database.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
        responses={200: openapi.Response("Successful response")},
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        tags=["Categories"],
        operation_summary="Get a category",
        operation_description="Returns a category by its ID.",
        responses={200: openapi.Response("Successful response")},
    )
    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Categories"],
        operation_summary="Update a category",
        operation_description="Updates a category by its ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
        responses={200: openapi.Response("Successful response")},
    )
    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["Categories"],
        operation_summary="Delete a category",
        operation_description="Deletes a category by its ID.",
        responses={204: openapi.Response("Successful response")},
    )
    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
