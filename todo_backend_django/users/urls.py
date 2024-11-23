from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView, 
    PasswordResetRequestView, 
    PasswordResetConfirmView
)

urlpatterns = [
    # User registration
    path('register/', RegisterView.as_view(), name='register'),
    
    # User login
    path('login/', LoginView.as_view(), name='login'),
    
    # User logout
    path('logout/', LogoutView.as_view(), name='logout'),

    # Password reset request (send reset link)
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),

    # Password reset confirmation (reset password using link)
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
