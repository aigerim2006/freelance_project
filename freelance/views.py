from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import HttpResponse
from .forms import PostForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.

def home(request):
    if request.method == "GET":
        return render(request, "index.html")
    
@login_required(login_url="/login/")
def post_list(request):
    posts = Post.objects.all()
    limit = 3

    form = SearchForm()

    search = request.GET.get("search")
    category = request.GET.get("category")
    tags = request.GET.getlist("tags")
    ordering = request.GET.get("ordering")
    page = int(request.GET.get("page", 1))
    if category:
        posts = posts.filter(category=category)

    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    if tags:
        posts = posts.filter(tags__in=tags)

    if ordering:
        posts = posts.order_by(ordering)

    total = posts.count()
    num_pages = total // limit + (1 if total % limit else 0)
    page = max(1, min(page, num_pages))  # чтобы страница не вышла за границы
    max_page = range(1, num_pages + 1)
    posts = posts[limit * (int(page) - 1) : limit * int(page)]
    return render(
        request,
        "posts.html",
        {
            "posts": posts,
            "form": form,
            "max_page": max_page, 
            "current_page": int(page),
            "selected_tags": tags,
        },
    )




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
