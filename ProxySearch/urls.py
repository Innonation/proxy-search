from django.urls import path, include

from ProxySearch.utils.utils_api import FieldViewSet

urlpatterns = [
    path('api/', include('ProxySearch.api.urls')),
]
