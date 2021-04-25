"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.views.defaults import page_not_found
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/auth/', include('rest_auth.urls')),
    url(r'^api/v1/auth/register/', include('rest_auth.registration.urls')),
    url(r'^api/v1/auth/token/', obtain_jwt_token),
    url(r'^api/v1/auth/token-refresh/', refresh_jwt_token),
    url(r'^api/v1/', include('src.apps.search.urls')),
    url(r'^$', page_not_found, kwargs={'exception': Exception(
        'Page not Found')}),
    url(r'^api/v1/', page_not_found, kwargs={'exception': Exception(
        'Page not Found')}),
    url(r'^health-check', views.health_check, name="health_check")
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)