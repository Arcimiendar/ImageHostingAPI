from django.urls import path

from api.views import ExpirableLinkModelView, ImageModelView


urlpatterns = [
    path('experiable_link/', ExpirableLinkModelView.as_view({
        'get': 'list', 'post': 'create'
    }), name='expirable-link'),
    path('image/', ImageModelView.as_view({
        'get': 'list', 'post': 'create'
    }), name='image')
]