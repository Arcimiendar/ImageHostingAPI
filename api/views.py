from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Image


class ImageModelView(viewsets.ModelViewSet):
    queryset = Image.objects
    serializer_class = None
    permission_classes = [IsAuthenticated]

# Create your views here.
