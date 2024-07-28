from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from accounts.forms import CustomUserCreationForm
from spotify.models import SpotifyToken


class RegisterView(CreateView):
    """
    User registration view
    """

    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    """
    User login view
    """

    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("profile")
    redirect_authenticated_user = True

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    User profile view
    """

    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            spotify_token = SpotifyToken.objects.get(user=self.request.user)
            context["spotify_connected"] = True
            context["spotify_token"] = spotify_token
        except SpotifyToken.DoesNotExist:
            context["spotify_connected"] = False
        return context
