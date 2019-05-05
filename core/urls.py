from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken

from . import views

router = routers.SimpleRouter()
router.register(r'users', views.UsersView, 'users')
router.register(r'sets', views.SetViewSet, 'sets')

urlpatterns = [
    path('login', ObtainAuthToken.as_view(), name='user_login'),
    path('sets/<int:set_id>/words', views.WordCreateView.as_view()),
    path('', include(router.urls))
]
