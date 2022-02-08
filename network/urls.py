
from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("<str:person_url>/", views.username, name="username"),
    path("follow/<str:person_url>/", views.follow, name="follow"), 
    path("unfollow/<str:person_url>/", views.unfollow, name="unfollow")
]
