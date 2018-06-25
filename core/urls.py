from django.conf.urls import url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UsersListView)
# router.register('sets', views.SetsByUserView, base_name='sets')
urlpatterns = [
    url(r'^sets/$', views.SetsByUserView.as_view()),
    url(r'^users/$', views.UsersListView.as_view()),
    url(r'^words/(?P<pk>[0-9]+)/$', views.WordsListView.as_view())
    # path('', include(router.urls))
]
