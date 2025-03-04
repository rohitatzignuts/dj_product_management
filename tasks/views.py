from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.serializers import TaskSerializer
from tasks.models import Task
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TaskList(APIView):

    @swagger_auto_schema(
        operation_summary="List all tasks",
        operation_description="Returns a list of all tasks available in the database.",
        responses={200: openapi.Response("Successful response")},
    )
    def get(self, request):
        filters = {}

        tstatus = request.GET.get("status")
        product = request.GET.get("product")

        if tstatus is not None:
            filters["status"] = tstatus

        if product is not None:
            filters["product"] = product

        tasks = Task.objects.filter(**filters).order_by("due_date")
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Add a new task",
        operation_description="Creates a new task in the database.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "due_date": openapi.Schema(type=openapi.TYPE_STRING),
                "status": openapi.Schema(type=openapi.TYPE_STRING),
                "product": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={200: openapi.Response("Successful response")},
    )
    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="Get a task",
        operation_description="Returns a task by its ID.",
        responses={200: openapi.Response("Successful response")},
    )
    def get(self, request, pk):
        Task = self.get_object(pk)
        serializer = TaskSerializer(Task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a task",
        operation_description="Updates a task by its ID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "due_date": openapi.Schema(type=openapi.TYPE_STRING),
                "status": openapi.Schema(type=openapi.TYPE_STRING),
                "product": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={200: openapi.Response("Successful response")},
    )
    def put(self, request, pk):
        Task = self.get_object(pk)
        serializer = TaskSerializer(Task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a task",
        operation_description="Deletes a task by its ID.",
        responses={204: openapi.Response("Successful response")},
    )
    def delete(self, request, pk):
        Task = self.get_object(pk)
        Task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
