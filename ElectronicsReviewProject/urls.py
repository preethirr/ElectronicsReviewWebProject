"""
URL configuration for ElectronicsReviewProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin #type: ignore
from django.urls import path,include #type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ElectronicsReviewApp.urls')),
]

from django.conf import settings #type: ignore
from django.conf.urls.static import static #type: ignore

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)