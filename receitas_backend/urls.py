from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from configs.views import Config

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('recipes/', include('recipes.urls')),
    path('config/', Config.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)