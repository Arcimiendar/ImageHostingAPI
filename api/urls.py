from django.urls import path

from api.views import ExpirableLinkModelView


urlpatterns = [
    path('experiable_link/', ExpirableLinkModelView.as_view({
        'get': 'list', 'post': 'create'
    }), name='expirable-link'),
]