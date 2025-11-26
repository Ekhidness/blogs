from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm

def home(request):
    posts_list = Post.objects.all().order_by('-created_at')[:50]
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'app/home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    paginator = Paginator(user_posts, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'app/profile.html', {'profile_user': profile_user, 'posts': posts})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Ваш профиль обновлен!')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'app/edit_profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Ваш профиль был удален.')
        return redirect('home')
    return render(request, 'app/delete_profile.html')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'app/post_form.html', {'form': form, 'title': 'Создать пост'})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('created_at')
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'app/post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'app/post_form.html', {'form': form, 'title': 'Редактировать пост'})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('home')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return redirect('post_detail', pk=comment.post.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'app/comment_form.html', {'form': form})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if request.user == comment.author:
        comment.delete()
    return redirect('post_detail', pk=post_pk)