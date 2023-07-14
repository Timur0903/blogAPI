from rest_framework import  generics,permissions

from post.permissions import IsAuthor
from .models import Like
from .serializers import LikeSerializer

# Create your views here.
class LikeCreateView(generics.CreateAPIView):
    permissions_classes = permissions.IsAuthenticated,
    serializer_class = LikeSerializer

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class LikeDeleteView(generics.DestroyAPIView):
    lookup_field = 'id'
    queryset = Like.objects.all()
    permission_classes = permissions.IsAuthenticated,IsAuthor