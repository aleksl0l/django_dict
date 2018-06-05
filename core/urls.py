from django.conf.urls import url
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UsersView)

urlpatterns = [
    url(r'sets', views.SetsByUserView.as_view()),
    path('', include(router.urls))
]