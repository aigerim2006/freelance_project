from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == "GET":
        return render(request, "users/register.html", {"form": RegisterForm()})
    elif request.method == "POST":
        forms_obj = RegisterForm(request.POST)
        if forms_obj.is_valid():
            forms_obj.cleaned_data.pop("confirm_password")
            User.objects.create_user(**forms_obj.cleaned_data)
            return HttpResponse("User created")
        return HttpResponse("Invalid form")


def login_view(request):
    if request.method == "GET":
        return render(request, "users/login.html", {"form": LoginForm()})
    elif request.method == "POST":
        forms_obj = LoginForm(request.POST)
        if forms_obj.is_valid():
            user = authenticate(
                username=forms_obj.cleaned_data["username"],
                password=forms_obj.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return HttpResponse("User logged in")
            return HttpResponse("Invalid login or password")
        return HttpResponse("Invalid form")
    

@login_required(login_url="/login/")
def logout_view(request):
    if request.method == "GET":
        logout(request)
        return HttpResponse("User logged out")

