from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.http import HttpResponse
from .forms import PostForm, SearchForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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
    print(request.method)
    if request.method == "GET":
        post = Post.objects.filter(id=post_id).first()
        post.views += 1
        post.save()
        form = CommentForm()
        comments = Comment.objects.filter(post_id=post_id)
        comment_count = comments.count()
        average = 0
        if comment_count > 0:
            average = sum([comment.rate for comment in comments]) / comment_count
        return render(
            request,
            "post_detail.html",
            context={
                "post": post,
                "form": form,
                "comments": comments,
                "average": int(average),
            },
        )
    elif request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                text=form.cleaned_data["text"],
                post_id=post_id,
                author=request.user,
                rate=form.cleaned_data["rate"],
            )
        return redirect(f"/posts/{post_id}/")

    elif request.method == "DELETE":
        Post.objects.filter(id=post_id).delete()
        return redirect("/posts/")




@login_required(login_url="/login/")
def post_create_view(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "post_create.html", {"form": form})

    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                price=form.cleaned_data["price"],
                photo=form.cleaned_data["photo"],
                category=form.cleaned_data["category"],
            )
            return HttpResponse("Заказ создан")

        return HttpResponse("Ошибка валидации формы")

@login_required(login_url="/login/")
def post_update(request, post_id):
    if request.method == "GET":
        post = Post.objects.filter(id=post_id).first()
        form = PostForm(initial=post.__dict__)
        return render(request, "post_update.html", context={"form": form})

    elif request.method == "PUT":
        form = PostForm(request.PUT, request.FILES)
        if form.is_valid():
            post = Post.objects.filter(id=post_id).first()
            if request.user == post.user:
                post.title = form.cleaned_data["title"]
                post.description = form.cleaned_data["description"]
                post.price = form.cleaned_data["price"]
                post.photo = form.cleaned_data["photo"]
                post.category = form.cleaned_data["category"]
                post.save()

        return redirect(f"/posts/{post_id}/")
