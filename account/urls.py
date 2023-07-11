from django.urls import path
# from .views import UserRegistration
from rest_framework.authtoken.views import ObtainAuthToken
from . import views

urlpatterns  = [
    path('register/', views.UserRegistration.as_view()),
    path('listing/', views.UserListView.as_view()),
    path('<int:id>/', views.UserDetailView.as_view()),
    # path('login/', ObtainAuthToken.as_view())
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view())
]