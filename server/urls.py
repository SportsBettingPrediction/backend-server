from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jet_api/', include('jet_django.urls')),
    path("auth/", include("authenticator.urls")),
    path("", include("game_provider.urls")),
    path("", include("user_interface.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
