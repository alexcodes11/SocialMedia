from distutils.log import error
import re
from tkinter.messagebox import RETRY
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import FieldDoesNotExist


from .models import  User, Posts, Following


def index(request):
    get = Posts.objects.all()
    paginator = Paginator(get, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"page_obj": page_obj})

def following(request):
    pass


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def posts(request):
    if request.method == "POST":
        text = request.POST["text"]
        post = Posts.objects.create(person = request.user, post = text)
        post.save()
        return redirect('index')

def username(request, person_url):
    if request.method == "GET":
        person = User.objects.filter(username = person_url)
        posts = Posts.objects.filter(person__username = person_url)
        return render(request, "network/userprofile.html", {"persons": person, "posts": posts})

@login_required
def follow(request, person_url):
    if request.method == "POST":
        user = User.objects.get(pk = request.user.id)
        follow = User.objects.get(username = person_url)
        if Following.objects.filter(person = user ).exists():
            test = Following.objects.get(person = user )
            test.following.add(follow.id)
            test.save()
        else: 
            new = Following.objects.create(person = user)
            new.following.add(follow.id)
            new.save()
        return redirect('username', person_url)
        

@login_required
def unfollow(request, person_url):
    if request.method == "POST":
        user = User.objects.get(pk = request.user.id)
        follow = User.objects.get(username = person_url)
        if Following.objects.filter(person = user, following = follow ).exists():
            test = Following.objects.get(person = user )
            test.following.remove(follow.id)
        else:
            # print error message
            pass
        return redirect('username', person_url) 

