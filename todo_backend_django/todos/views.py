from rest_framework.views import APIView  # Importing APIView for creating class-based views
from rest_framework.permissions import IsAuthenticated  # Importing permission to enforce authentication
from rest_framework.response import Response  # Importing Response to send API responses
from rest_framework import status  # Importing status codes for API responses
from .models import Todo  # Importing the Todo model
from .serializers import TodoSerializer  # Importing the Todo serializer
from rest_framework import viewsets
import re
from django.core.paginator import Paginator
from datetime import datetime  # Import datetime for date conversion

import jwt
from django.conf import settings



# Class-based view for managing todos
class TodoListView(APIView):  
    """
    Handles listing and creating todos for the authenticated user.
    """
    permission_classes = [IsAuthenticated]  # Enforce authentication for this view

    def pagination(self,todos, page_number, page_size=10):

        """
        To get todo with page number===>http://127.0.0.1:8000/api/todos?page=1&page_size=10
        """


        """
        Paginate the todos queryset.

        Args:
            todos (QuerySet): The queryset of todos to paginate.
            page_number (int): The current page number.
            page_size (int): The number of items per page (default is 10).

        Returns:
            dict: Paginated data with items and metadata.
        """
        paginator = Paginator(todos, page_size)  # Create a Paginator object
        page = paginator.get_page(page_number)  # Get the requested page
        return {
            "items": list(page.object_list),  # Items in the current page
            "total_pages": paginator.num_pages,  # Total number of pages
            "current_page": page.number,  # Current page number
            "has_next": page.has_next(),  # Whether there is a next page
            "has_previous": page.has_previous(),  # Whether there is a previous page
        }

    def get(self, request):
        """
        Fetches all todos for the authenticated user.
        """

        user_email = request.user.email  # Extract the email of the authenticated user
        page_number = request.query_params.get('page', 1)  # Get the page number from query parameters
        page_size = request.query_params.get('page_size', 10)  # Get the page size from query parameters

        # role = request.auth.get('role', None)  # 'role' is embedded in the JWT during token generation

         # Decode the JWT token to access the role
        try:
            # Get the token from the request headers (assuming 'Authorization: Bearer <token>')
            token = request.headers.get("Authorization").split(" ")[1]
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            role = decoded_token.get("role", None)  # Extract the role from the token payload
        except (IndexError, jwt.ExpiredSignatureError, jwt.DecodeError, AttributeError):
            return Response({"error": "Invalid or missing token."}, status=status.HTTP_401_UNAUTHORIZED)



         # Fetch todos based on the user's role
        if role == 'admin':
            print("The user has the 'admin' role.")  # Debug log for admin user
            todos = Todo.objects.all()  # Fetch all todos for admin users
        else:
            print(f"The user has the role: {role}.")  # Debug log for non-admin user
            todos = Todo.objects.filter(user=request.user)  # Fetch todos owned by the current user

          # Extract filter parameters from the request
        completed = request.query_params.get('completed', None)  # Filter by status
        created_at = request.query_params.get('created_at', None)  # Filter by due_date

        # Apply filters if provided
        if completed:
            todos = todos.filter(completed=completed)  # Assuming Todo model has a 'status' field
        if created_at:
            try:
                created_at = datetime.strptime(created_at, '%Y-%m-%d').date()  # Convert string to date object
                todos = todos.filter(created_at__date=created_at)  # Use __date to match only the date portion
            except ValueError:
                return Response({"error": "Invalid date format. Please use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)


        # Paginate the todos
        paginated_data = self.pagination(todos, page_number,page_size)
        serializer = TodoSerializer(paginated_data["items"], many=True)  # Serialize the paginated todos
        return Response({
            "todos": serializer.data,  # Serialized todos
            "pagination": {
                "total_pages": paginated_data["total_pages"],
                "current_page": paginated_data["current_page"],
                "has_next": paginated_data["has_next"],
                "has_previous": paginated_data["has_previous"],
            }
        })  # Respond with serialized data and pagination metadata
            


        
    def post(self, request):
        """
        Creates a new todo for the authenticated user.
        """
        data = request.data  # Extract the input data from the request
        data['user'] = request.user.id  # Set the user field to the current user's ID
        serializer = TodoSerializer(data=data)  # Deserialize the input data
        if serializer.is_valid():  # Check if the input data is valid
            serializer.save()  # Save the todo to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Respond with the created todo data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Respond with validation errors

    def delete(self, request, todo_id):
        """
        Deletes a specific todo item for the authenticated user.
        """
        try:
            todo = Todo.objects.get(id=todo_id, user=request.user)  # Find the Todo by ID and ensure it belongs to the authenticated user
            todo.delete()  # Delete the todo
            return Response({"message": "Todo successfully deleted."}, status=status.HTTP_204_NO_CONTENT)  # Respond with success message
        except Todo.DoesNotExist:
            return Response({"message": "Todo not found or you don't have access to it."}, status=status.HTTP_404_NOT_FOUND)  # Handle case where todo does not exist or user doesn't own it

    def put(self, request, todo_id):
        """
        Updates a specific todo for the authenticated user.
        """
        try:
            todo = Todo.objects.get(id=todo_id, user=request.user)  # Get the todo item for the current user
            print(todo_id)
            serializer = TodoSerializer(todo, data=request.data)  # Deserialize the input data
            if serializer.is_valid():  # Check if the input data is valid
                serializer.save()  # Save the updates to the database
                return Response(serializer.data, status=status.HTTP_200_OK)  # Respond with the updated todo data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Respond with validation errors
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found."}, status=status.HTTP_404_NOT_FOUND)