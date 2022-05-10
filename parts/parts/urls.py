# Main urls.py

from django.contrib import admin
from django.urls import re_path, path, include

from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', include('catalog.urls')),
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('verification/', include('verify_email.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += [re_path(r'[.]*', views.redirect_url, name="redirect-url")]