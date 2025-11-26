from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),

    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),

    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]