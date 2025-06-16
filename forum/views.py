from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Category, Vote
from .forms import UserRegistrationForm, PostForm, CommentForm

@login_required
def vote_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    direction = request.POST.get("direction")
    if direction not in ['up', 'down']:
        return JsonResponse({'error': 'Invalid vote direction'}, status=400)

    user = request.user

    existing_vote = Vote.objects.filter(user=user, post=post).first()
    if existing_vote:
        existing_vote.value = 1 if direction == 'up' else -1
        existing_vote.save()
    else:
        vote_value = 1 if direction == 'up' else -1
        Vote.objects.create(user=user, post=post, value=vote_value)

    score = post.vote_score()

    return JsonResponse({"score": score})

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'forum/index.html', {'posts': posts, 'categories': categories})

def posts_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'forum/index.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': category
    })

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'forum/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'forum/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'forum/create_post.html', {'form': form})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') 
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'forum/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })
