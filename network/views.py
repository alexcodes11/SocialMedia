from distutils.log import error
import json
import re
from turtle import pos
from urllib import response
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import NullBooleanField
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Count



from .models import  User, Posts, Following


def index(request):
    # TO DO THis will generate all the posts the current user can edit.
    get = Posts.objects.all().order_by('-id')
    paginator = Paginator(get, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"page_obj": page_obj})


@login_required
def following(request, user_id):
    #Here I had only let the specific user accesses their own following page. Because if I do not do this then a hacker can access any following page.
    if request.user == User.objects.get(pk = user_id):
        get = Posts.objects.filter(person__following__person= user_id).order_by('-id')
        paginator = Paginator(get, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        return render(request, "network/following.html", {
                "message": "You cannot access this page"
            })
    return render(request, "network/following.html", {"page_obj": page_obj})

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
            if User.objects.filter(email=email).exists():
                return render(request, "network/register.html", {
                    "message": "Email is already taken."
                    })
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
# fix the following section
def username(request, person_url):
    if request.method == "GET":
        person = User.objects.filter(username = person_url)
        posts = Posts.objects.filter(person__username = person_url).order_by('-id')
        if Following.objects.filter(person__username = person_url).exists():
            # fixed this at first I just counted the person which was one. My bug was I need to count the following field which i fixed below.
            following = Following.objects.filter(person__username = person_url ).values_list("following").count()
        else:
            following = 0
        if Following.objects.filter(following__username = person_url).exists():
            followers = Following.objects.filter(following__username = person_url).count()
        else:
            followers = 0
        userisfollowing = False 
        if Following.objects.filter(person = request.user.id).exists():
            if Following.objects.filter(person = request.user.id, following__username = person_url).exists():
                userisfollowing = True
        return render(request, "network/userprofile.html", {"persons": person, "posts": posts, "followers": followers, "following":following, "userisfollowing": userisfollowing})

# come back to this later and make sure the user cannot follow themselves. Already removed the button though templates but gotta make sure.
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
            return render(request, "network/error.html", {"message": "You do not follow this user, therefore you cannot unfollow them"})
        return redirect('username', person_url) 

# Need to change this so you can like via javascript API
@login_required
def updatelike(request, post_id):
    user = User.objects.get(pk = request.user.id)
    # if like already exists remove it
    if Posts.objects.filter(pk = post_id, likes = user).exists():
        remove_like = Posts.objects.get(pk = post_id)
        remove_like.likes.remove(user)
    # if Like post model exists  just add the user
    else:
        new_like = Posts.objects.get(pk = post_id)
        new_like.likes.add(user)
        new_like.save()
    response_data = {}
    if Posts.objects.filter(pk = post_id, likes__isnull = False).exists():
        response_data["count"] = Posts.objects.filter(pk = post_id).values_list("likes").count()
    else:
        response_data["count"] = 0
    if Posts.objects.filter(pk = post_id, likes = request.user.id):
        response_data["liked"] = "liked"
    else:
        response_data["liked"] = "unlike"
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def editpost(request, post_id):
    #check if user is the creator of the post
    if request.method == "GET":
        if Posts.objects.filter(pk = post_id , person = request.user.id ).exists():
            api = Posts.objects.get(pk = post_id , person = request.user.id )
            return JsonResponse([api.serialize()], safe=False)
    else:
        return JsonResponse({"error": "You cannot edit this post."}, status=400)


@login_required
def edit(request, post_id, editedpost):
    if editedpost == [""]:
        return JsonResponse({
            "error": "At least character needed for your post."
        })
    if Posts.objects.filter(pk = post_id , person = request.user.id ).exists():
        new = Posts.objects.filter(pk = post_id , person = request.user.id ).update(post = editedpost)
        new.save()
        post = 0
        return HttpResponse(json.dumps(post), content_type = "application/json")
    else:
        return JsonResponse({"error": "You cannot edit this post."}, status=400)
