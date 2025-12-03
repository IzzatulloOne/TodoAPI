from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema

from .models import Todo
from .serializers import TodoSerializer



class TodoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.order_by('-id')
    serializer_class = TodoSerializer

    @swagger_auto_schema(
        operation_description="Список всех TODO",
        responses={200: TodoSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GetTodoView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.order_by('-id')
    serializer_class = TodoSerializer

    @swagger_auto_schema(
        operation_description="Получение одного TODO по id",
        responses={200: TodoSerializer()}
    )
    def get(self, request, pk, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TodoCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.order_by('-id')
    serializer_class = TodoSerializer

    @swagger_auto_schema(
        operation_description="Создание нового TODO",
        responses={201: TodoSerializer()}
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class TodoCRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.order_by('-id')
    serializer_class = TodoSerializer

    @swagger_auto_schema(
        operation_description="Получение TODO по id",
        responses={200: TodoSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновление TODO по id",
        request_body=TodoSerializer,
        responses={200: TodoSerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное обновление TODO по id",
        request_body=TodoSerializer,
        responses={200: TodoSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удаление TODO по id",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
