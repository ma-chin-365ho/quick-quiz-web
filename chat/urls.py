from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("room-creation/", views.room_creation, name="room_creation"),
    path("room-entering/", views.room_entering, name="room_entering"),
    path("room-questioner/<str:room_id>/", views.room_questioner, name="room_questioner"),
    path("room-answerer/<str:room_id>/", views.room_answerer, name="room_answerer"),
]