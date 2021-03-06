from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('forum.urls')),
    path('forum/', include('forum.urls')),
    path('profiles/', include('profiles.urls')),
    path('profile/', include('profiles.urls')),
    path('payment/', include('payment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "helpers.views.handle_not_found"
