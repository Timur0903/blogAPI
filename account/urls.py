from django.urls import path,include
# from .views import UserRegistration
from rest_framework.authtoken.views import ObtainAuthToken
from . import views
from dj_rest_auth.views import LoginView,LogoutView
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register('',views.UserViewSet)

urlpatterns  = [
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('register/', views.UserRegistration.as_view()),
    path('',include(router.urls)),
    path('post/',include(router.urls))
    # path('listing/', views.UserListView.as_view()),
    # path('<int:id>/', views.UserDetailView.as_view()),
    # path('login/', ObtainAuthToken.as_view())
    # path('login/', views.LoginView.as_view()),
    # path('logout/', views.LogoutView.as_view())

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)