from rest_framework import serializers  # Importing serializers for API input/output handling
from .models import Todo  # Importing the Todo model

# Serializer for Todo model
class TodoSerializer(serializers.ModelSerializer):  
    """
    Converts Todo model instances into JSON format and validates input data for creating/updating todos.
    """

    class Meta:
        model = Todo  # Specify the model the serializer is based on
        fields = '__all__'  # Include all fields of the model in the API response
