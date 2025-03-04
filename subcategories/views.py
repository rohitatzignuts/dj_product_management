from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from subcategories.serializers import SubCategorySerializer
from subcategories.models import SubCategory
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SubCategoriesList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    @swagger_auto_schema(
        operation_summary="List all subcategories",
        operation_description="Returns a list of all subcategories available in the database.",
        responses={200: openapi.Response("Successful response")},
    )
    def get(self, request):
        subcategories = SubCategory.objects.all().order_by("created_at")
        serializer = SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Add a new subcategory",
        operation_description="Creates a new subcategory in the database.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "category": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={200: openapi.Response("Successful response")},
    )
    def post(self, request):
        serializer = SubCategorySerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryDetail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def get_object(self, pk):
        try:
            return SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get a subcategory",
        operation_description="Returns a subcategory by its ID.",
        responses={200: openapi.Response("Successful response")},
    )
    def get(self, request, pk):
        subcategory = self.get_object(pk)
        serializer = SubCategorySerializer(subcategory)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a subcategory",
        operation_description="Updates a subcategory in the database.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "category": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={200: openapi.Response("Successful response")},
    )
    def put(self, request, pk):
        subcategory = self.get_object(pk)
        serializer = SubCategorySerializer(subcategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a subcategory",
        operation_description="Deletes a subcategory by its ID.",
        responses={204: openapi.Response("Successful response")},
    )
    def delete(self, request, pk):
        subcategory = self.get_object(pk)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
