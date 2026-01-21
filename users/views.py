from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from users.models import Profile
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == "GET":
        return render(request, "users/register.html", {"form": RegisterForm()})
    elif request.method == "POST":
        forms_obj = RegisterForm(request.POST, request.FILES)
        if forms_obj.is_valid():
            forms_obj.cleaned_data.__delitem__("confirm_password")
            age = forms_obj.cleaned_data.pop("age")
            photo = forms_obj.cleaned_data.pop("photo")
            user = User.objects.create_user(**forms_obj.cleaned_data)
            if user:
                Profile.objects.create(user=user, age=age, photo=photo)
            return redirect("/login/")
        return HttpResponse("Invalid form")


def login_view(request):
    if request.method == "GET":
        return render(request, "users/login.html", {"form": LoginForm()})
    elif request.method == "POST":
        forms_obj = LoginForm(request.POST)
        if forms_obj.is_valid():
            user = authenticate(**forms_obj.cleaned_data)
            if user is not None:
                login(request, user)
            return redirect("/")
        
    

@login_required(login_url="/login/")
def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect("/")

@login_required(login_url="/login/")
def profile_view(request):
    if request.method == "GET":
        user = request.user
        products = user.posts.all()
        return render(
            request,
            "users/profile.html",
            {
                "user": user,
                "products" : products
            }
        )
