from django.urls import path  # Importing the path function for URL routing
from .views import TodoListView  # Importing the TodoListView class-based view

urlpatterns = [
    # Route for listing and creating todos
    path('', TodoListView.as_view(), name='todo-list'),  # Routes to the TodoListView
    path('<int:todo_id>/', TodoListView.as_view(), name='todo-detail'),  # URL for retrieving, updating, and deleting a specific todo

]
