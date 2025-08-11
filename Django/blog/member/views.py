from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse


def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    context = {
        "form": form,
    }
    return render(request, "registration/signup.html", context)


def login(request):
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
        django_login(request, form.get_user())

        next = request.GET.get("next")
        if next:
            return redirect(next)

        return redirect(reverse("blog:list"))
    context = {
        "form": form,
    }
    return render(request, "registration/login.html", context)
