from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("tmcapp.urls")),
    path("admin/", admin.site.urls),
]

# Append static and media URLs correctly
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)