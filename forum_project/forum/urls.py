from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_post, name='create_post'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
	path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
	path('post/<int:post_id>/', views.post_detail, name='post_detail'),
	path('vote/<int:post_id>/', views.vote_post, name='vote_post'),
]
