from django.conf.urls import url, include
from omok_backend_rest import views

urlpatterns = [
    url(r'^rooms/$', views.room_list),
    url(r'^rooms/(?P<pk>[0-9]+)/$', views.room_detail),
    url(r'^rooms/(?P<pk>[0-9]+)/players/$', views.room_players_list),
    url(r'^rooms/(?P<pk>[0-9]+)/history/$', views.room_history_list),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]
