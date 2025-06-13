from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  
    path('api/songs/', include('songs.urls')),
    path('api/albums/', include('albums.urls')),
    path('api/playlists/', include('playlists.urls')),
    path('api/follows/', include('follows.urls')),
    path('api/streams/', include('streams.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # OpenAPI schema JSON
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # ReDoc UI
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)