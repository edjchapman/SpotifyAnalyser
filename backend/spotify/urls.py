from django.urls import path

from .views import spotify_login, spotify_callback, spotify_disconnect

urlpatterns = [
    path("callback/", spotify_callback, name="spotify-callback"),
    path("login/", spotify_login, name="spotify-login"),
    path("disconnect/", spotify_disconnect, name="spotify-disconnect"),
]
