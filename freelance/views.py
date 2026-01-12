from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import HttpResponse
from .forms import PostForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    if request.method == "GET":
        return render(request, "index.html")
    
@login_required(login_url="/login/")
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        return render(request, "posts.html", {"posts": posts})


@login_required(login_url="/login/")
def post_detail(request, post_id):
    if request.method == "GET":
        post = get_object_or_404(Post, id=post_id)
        return render(request, "post_detail.html", {"post": post})

@login_required(login_url="/login/")
def post_create_view(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "post_create.html", {"form": form})

    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(**form.cleaned_data)
            return HttpResponse("Заказ создан")

        return HttpResponse("Ошибка валидации формы")
