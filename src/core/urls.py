from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from . import views
from django.urls import re_path, include


router = DefaultRouter()
router.register('profile', views.ProfileViewSet)


urlpatterns = [
    re_path(r'^login/?$', views.LoginAPIView.as_view(), name='user_login'),
    url(r'', include(router.urls)),
]
