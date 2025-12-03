from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions

from .models import Todo
from .serializers import TodoSerializer



class TodoListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.order_by('-id')
    serializer_class = TodoSerializer



class GetTodoView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.order_by('-id')
    serializer_class = TodoSerializer

    def get(self, pk):
        todo = Todo.objects.get(id=pk)
        serializer = TodoSerializer(todo)

        return Response(serializer.data, status=status.HTTP_200_OK)



class TodoCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.order_by('-id')
    serializer_class = TodoSerializer



class TodoCRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.order_by('-id')
    serializer_class = TodoSerializer