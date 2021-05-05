from django.urls import path
from .views import get_users, get_user, update_user, register_user, validate_user_registration, generate_user_registration_token

urlpatterns = [
    path('get_users/', get_users),
    path('update_user/<user_id>', update_user),
    path('get_user/<user_id>', get_user),
    path('register_user/', register_user),
    path('validate_registration/<user_id>', validate_user_registration),
    path('generate_user_registration_token/<user_id>', generate_user_registration_token),
]