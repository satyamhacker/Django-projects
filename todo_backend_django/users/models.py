from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Automatically hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

# Custom User model for authentication
class User(AbstractBaseUser, PermissionsMixin):
    # A unique username for the user (used for authentication)
    username = models.CharField(max_length=100, unique=True)
    # A unique email for the user (optional)
    email = models.EmailField(unique=True)
    # A field to store the hashed password of the user (automatically managed by AbstractBaseUser)
    password = models.CharField(max_length=255)
    # Other fields for user profile can go here, such as name, profile picture, etc.
    is_active = models.BooleanField(default=True)  # Active flag
    is_staff = models.BooleanField(default=False)  # Staff flag for admin privileges

    # Using the custom user manager
    objects = CustomUserManager()

    # The field used for authentication
    USERNAME_FIELD = 'username'

    # Define required fields for superuser creation
    REQUIRED_FIELDS = ['email']  # Only email is needed for superuser creation

    # Method to return the string representation of the User object (email)
    def __str__(self):
        return self.email  # Display the user's email when the object is printed

 
# UserSettings model to store user settings such as roles
class UserSettings(models.Model):
    user = models.OneToOneField(User, related_name='usersettings', on_delete=models.CASCADE)
    #related_name: This is an optional argument that defines the name of the reverse relation from the User model back to the UserSettings model.

    role = models.CharField(max_length=50, default='user')  # Default role is 'user'
    # You can add more fields for other settings, for example:
    # preferred_language = models.CharField(max_length=20, default='en')
    # notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s settings"  # String representation of UserSettings
