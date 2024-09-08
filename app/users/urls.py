from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.user_registration_view, name="register"),
    # path("", include("django.contrib.auth.urls")),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
