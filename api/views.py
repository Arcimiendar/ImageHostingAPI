from django.db.models import F, ExpressionWrapper, DateTimeField
from django.db.models.functions import Now
from django.views.decorators.http import require_GET
from django.http import Http404, HttpResponse

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Image, ExpirableLink, Thumbnail
from api.serializers import ExpirableLinkSerializer, ImageSerializer, ThumbnailSerializer
from api.permissions import IsCreationOfExpirableLinkAllowedOrReadOnly


class ImageModelView(viewsets.ModelViewSet):
    queryset = Image.objects
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super(ImageModelView, self).get_queryset()
        return queryset.filter(uploader=self.request.user)


class ExpirableLinkModelView(viewsets.ModelViewSet):
    serializer_class = ExpirableLinkSerializer
    queryset = ExpirableLink.objects.annotate(
        expiration_time=ExpressionWrapper(
            F('time_created') + F('experation_period'), output_field=DateTimeField())
    ).filter(expiration_time__gt=Now())
    permission_classes = [IsCreationOfExpirableLinkAllowedOrReadOnly]


class ThumbnailModelView(viewsets.ModelViewSet):
    serializer_class = ThumbnailSerializer
    queryset = Thumbnail.objects
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super(ThumbnailModelView, self).get_queryset()
        if self.request.query_params.get('image'):
            queryset = queryset.filter(original_image__pk=int(self.request.query_params.get('image')))
        return queryset.filter(original_image__uploader=self.request.user)


@require_GET
def expirable_link_content_view(request, expirable_link):
    link = ExpirableLink.filter_by_temporary_link(expirable_link).annotate(
        expiration_time=ExpressionWrapper(
            F('time_created') + F('experation_period'), output_field=DateTimeField())
    ).filter(expiration_time__gt=Now()).first()

    if not link:
        raise Http404
    return HttpResponse(content=link.image.image_file, content_type='image/jpg')
