from django.urls import path
from .views import UserRegistration
from . import views

urlpatterns = [
    path('register/',views.UserRegistration.as_view()),
    path('listing/',views.UserListView.as_view())
]
