from django.urls import path

from api.views import ExpirableLinkModelView, ImageModelView, ThumbnailModelView, expirable_link_content_view


urlpatterns = [
    path('experiable_links/', ExpirableLinkModelView.as_view(
        {'get': 'list', 'post': 'create'}
    ), name='expirable-link'),
    path('images/', ImageModelView.as_view({'get': 'list', 'post': 'create'}), name='image'),
    path('thumbnails/', ThumbnailModelView.as_view({'get': 'list'}), name='thumbnails'),
    path('temporary_link/<slug:expirable_link>', expirable_link_content_view, name='temporary-link')
]
