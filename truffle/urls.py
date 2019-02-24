from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r: redirect('core:index'), name='root'),
    path('core/', include(('core.urls', 'core'), namespace='core')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('playlists/', include(('playlists.urls', 'playlists'), namespace='playlists')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
