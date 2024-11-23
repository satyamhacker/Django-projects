from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .models import User, UserSettings  # Import custom User model from your users app
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.db import transaction  # Import transaction for atomic operations
from .serializers import CustomTokenObtainPairSerializer




# Register view (User registration)
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users

    def post(self, request):
        # Expecting username, email, password, and role from the request body
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "user")  # Default to "user" if role is not provided

        # Validate role if provided
        valid_roles = ["user", "admin"]  # Add other roles if needed
        if role not in valid_roles:
            return Response({"error": f"Invalid role. Valid roles are {valid_roles}."}, status=status.HTTP_400_BAD_REQUEST)

        if not username or not email or not password:
            return Response({"error": "Username, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use a single transaction to handle both user and settings creation
            with transaction.atomic():
                # Create new user
                user = User.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password),
                )

                # Create the user's settings with the specified or default role
                UserSettings.objects.create(
                    user=user,  # Link to the user
                    role=role   # Set the role
                )

            # Create a token (using JWT or session, depending on your setup)
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                "message": "User registered successfully",
                "access_token": str(access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    authentication_classes = []  # Disable authentication for this view
    permission_classes = []  # Optionally disable permission check if necessary
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
      
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate token using the custom serializer
        serializer = CustomTokenObtainPairSerializer(data={"username": username, "password": password})
        serializer.is_valid(raise_exception=True)  # This will call validate()
        token_data = serializer.validated_data

        return Response({
            "message": "Login successful",
            "access_token": token_data['access'],
            "refresh_token": token_data['refresh'],
        }, status=status.HTTP_200_OK)

# Logout view (Invalidate the token)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Invalidate the token (simple approach, you can implement blacklist logic)
        try:
            request.user.auth_token.delete()  # If using token authentication
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    # Set permission to allow any user (authenticated or not) to access this view
    permission_classes = [AllowAny]

    # Define the POST method to handle password reset requests
    def post(self, request):
        # Retrieve the email from the incoming request data
        email = request.data.get("email")

        # If the email is not provided in the request, return a 400 Bad Request error
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to get the user with the provided email address from the database
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # If no user exists with the given email, return a 404 Not Found error
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Generate a password reset token for the user using the default token generator
        token = default_token_generator.make_token(user)

        # Create a reset link that includes the user ID (encoded) and the reset token
        uid = urlsafe_base64_encode(str(user.pk).encode())
        reset_link = f"http://localhost:8000/api/reset-password/{uid}/{token}/"

        # Send the reset link via email (optional for testing)
        subject = "Password Reset Request"  # Subject line of the email
        message = f"Click the link below to reset your password:\n\n{reset_link}"  # Body of the email containing the reset link
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])  # Sending the email to the user

        # Return a response confirming that the reset link has been sent to the user's email
        # Include the reset link in the response body (usually for testing purposes)
        return Response({
            "message": "Password reset link has been sent to your email.",
            "reset_link": reset_link  # Return the reset link in the response for testing
        }, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    # Set permission to allow any user (authenticated or not) to access this view
    permission_classes = [AllowAny]

    # Define the POST method to handle password reset confirmation requests
    def post(self, request, uidb64, token):
        try:
            # Decode the user ID from base64 (uidb64) into a readable string
            uid = urlsafe_base64_decode(uidb64).decode()

            # Retrieve the user object with the decoded user ID (primary key)
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            # If the user does not exist or the base64 decoding fails, return a 400 error
            return Response({"error": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the token to ensure it's valid and not expired
        if not default_token_generator.check_token(user, token):
            # If the token is invalid or expired, return a 400 error
            return Response({"error": "Invalid or expired reset link."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the new password from the request data
        new_password = request.data.get("password")

        # If no new password is provided, return a 400 error
        if not new_password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the user's password to the new password, securely hashing it
        user.password = make_password(new_password)

        # Save the user object with the updated password in the database
        user.save()

        # Return a success message indicating that the password has been successfully reset
        return Response({"message": "Password has been successfully reset."}, status=status.HTTP_200_OK)
