
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import PostViewSet

router = DefaultRouter()
router.register('', PostViewSet)


urlpatterns = [
    # path('',views.PostListCreateView.as_view()),
    # path('<int:id>',views.PostDetailsView.as_view()),
    path('', include(router.urls))
]