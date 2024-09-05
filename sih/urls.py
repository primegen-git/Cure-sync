"""
URL configuration for sih project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from hospital import urls as hospital_urls
from user import urls as user_urls
from home import urls as home_urls
from opd import urls as opd_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(home_urls, namespace="home")),
    path("hospital/", include(hospital_urls, namespace="hospital")),
    path("user/", include(user_urls, namespace="user")),
    path("opd/", include(opd_urls, namespace="opd")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
