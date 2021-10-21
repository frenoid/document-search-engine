from django.conf.urls import re_path
from django.urls import path
from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views
from .views import DocUserView, DocUserLogoutAllView, DocUserDeleteView, CurrentUserView

urlpatterns = [
    re_path(r'^user/view/$', DocUserView.as_view({'get': 'detail'}), name='user-view'),
    re_path(r'^user/delete/$', DocUserDeleteView.as_view({'get': 'delete'}), name='user-delete'),
    re_path(r'^user/logout/all/$', DocUserLogoutAllView.as_view(), name='user-logout-all'),

    # Views are defined in Djoser, but we're assigning custom paths.
    re_path(r'^user/create/$', djoser_views.UserViewSet.as_view({'get': 'create'}), name='user-create'),
    path('current-user/<int:pk>', CurrentUserView.as_view(), name='current-user'),
    # Views are defined in Rest Framework JWT, but we're assigning custom paths.
    re_path(r'^user/login/$', jwt_views.ObtainJSONWebToken.as_view(), name='user-login'),
    re_path(r'^user/login/refresh/$', jwt_views.RefreshJSONWebToken.as_view(), name='user-login-refresh'),
]
