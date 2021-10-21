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
from django.contrib import admin
from django.views.defaults import page_not_found
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/auth/', include('djoser.urls')),
    url(r'^api/v1/auth/', include('djoser.urls.authtoken')),
    url(r'^api/v1/', include('src.apps.search.urls')),
    url(r'^api/v1/', include('src.apps.otp.urls')),
    url(r'^api/v1/', include('src.apps.document_user.urls')),
    url(r'^api/v1/', include('src.apps.otp.urls')),
    url(r'^api/v1/', page_not_found, kwargs={'exception': Exception(
        'Page not Found')}),
    url(r'^health-check', views.health_check, name="health_check"),
    url(r'^$', page_not_found, kwargs={'exception': Exception(
        'Page not Found')})
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

