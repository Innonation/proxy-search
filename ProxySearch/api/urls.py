from django.conf.urls import url
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# SCHEMA
from ProxySearch.utils.utils_api import FieldViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Proxy_search",
        default_version='0.0.0',
        description="Applicativo per effettuare ricerche su architetture dati complessi, richiamando opportunamente le api di metabase.",
    ),
    public=True,
)

# URLS
urlpatterns = [
    path('metadata/', FieldViewSet.as_view({'post': 'doMetadata'})),
    path('research/', FieldViewSet.as_view({'post': 'doQuery'})),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
