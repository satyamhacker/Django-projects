from rest_framework import serializers  # Importing serializers for API input/output handling
from .models import User, UserSettings  # Importing the User model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken



# Serializer for User model
class UserSerializer(serializers.ModelSerializer):  
    """
    Converts User model instances into JSON format and validates input data for creating/updating users.
    """

    class Meta:
        model = User  # Specify the model the serializer is based on
        fields = ['id', 'username', 'email', 'password']  # Fields to include in the API response
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only to avoid exposure

    def create(self, validated_data):
        """
        Overrides the default creation process to hash passwords before saving.
        """
        # Create a new user instance using the validated data
        return User.objects.create(**validated_data)  

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call the parent validate method to get the token and user
        data = super().validate(attrs)

        # Add custom claims
        user = self.user

        
        try:
            role = user.usersettings.role

           
            
        except UserSettings.DoesNotExist:
            role = "Unknown"  # Default role if UserSettings is missing
        
        # Create the refresh token for the user
        refresh = RefreshToken.for_user(user)

        # Add the role to the token payload
        refresh['role'] = role  # Embed role into the payload

        # Add the tokens to the response
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)


        return data
