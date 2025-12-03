from django.urls import path
from . import views

urlpatterns = [
    path('todo/', views.TodoListView.as_view(), name='todo-list-all'),
    path('todo/<int:pk>/', views.GetTodoView.as_view(), name='get-todo'),
    path('todo_crud/', views.TodoCRUDView.as_view(), name='update-delete-retrive-todo'),
    path('todo_create/', views.TodoCreateView.as_view(), name='todo-create')
]