import after_response
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import redirect, render
from users.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from .forms import UserCustomCreationForm
from .tasks import user_registration_email
from .tokens import account_activation_token


def logout_view(request):
    logout(request)
    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("/")
    else:
        return redirect("login")


def user_registration_view(request):
    current_site = Site.objects.get_current()
    domain = current_site.domain
    if request.method == "POST":
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user_registration_email.after_response(
                request, user, form.cleaned_data["email"]
            )
            # user_registration_email(request, user, form.cleaned_data.get("email"))
            return redirect("login")
    else:
        form = UserCustomCreationForm()
    return render(request, "users/register.html", {"form": form})
