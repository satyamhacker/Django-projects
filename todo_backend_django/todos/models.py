from django.db import models  # Importing the models module to define database models
from users.models import User  # Importing the User model to establish a relationship with Todo

# Todo model to store task details
class Todo(models.Model):
    # Foreign key to associate the todo item with a user
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="todos"
    )  
    # Title of the task
    title = models.CharField(max_length=100)  
    # Optional detailed description of the task
    description = models.TextField(blank=True, null=True)  
    # Boolean field to track task completion status
    completed = models.BooleanField(default=False)  
    # Timestamp when the task was created
    created_at = models.DateTimeField(auto_now_add=True)  
    # Timestamp when the task was last updated
    updated_at = models.DateTimeField(auto_now=True)  
