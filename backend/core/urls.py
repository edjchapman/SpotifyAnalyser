from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("spotify/", include("spotify.urls")),
    path(
        "",
        RedirectView.as_view(url="/accounts/profile/", permanent=False),
        name="root_redirect",
    ),
]
