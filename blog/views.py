from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms  import SignupForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import Post
# Create your views here.

# Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})

# About
def about(request):
    return render(request, 'blog/about.html')

# Contact
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all() #One person can be in many groups
        return render(request, 'blog/dashboard.html', {'posts':posts, 'fullName':full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup
def sign_up(request):
    if request.method == 'POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            user = fm.save()
            group = Group.objects.get(name = "Author")
            user.groups.add(group)
            messages.success(request, 'Congratulations!!, You are an Author now')
            fm = SignupForm()
    else:        
        fm = SignupForm()
    return render(request, 'blog/signup.html', {'forms':fm})

# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = LoginForm(request=request, data = request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username = uname, password = upass)
                
                if user!=None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!!')
                    return HttpResponseRedirect('/dashboard/')
        else:        
            fm = LoginForm()
        return render(request, 'blog/login.html', {'forms':fm})
    else:
        return HttpResponseRedirect('/dashboard/')
    
# Add new Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PostForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Your post has been added successfully!!')
                fm = PostForm()
        else:
            fm = PostForm()        
        return render(request, 'blog/addPost.html', {'forms':fm})
    else:
        return HttpResponseRedirect('/login/')    
    
    
# Update Post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk = id)
            fm = PostForm(request.POST, instance=pi)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Your post has been updated successfully!!')
                fm = PostForm()
        else:
            pi = Post.objects.get(pk = id)
            fm = PostForm(instance=pi)        
        return render(request, 'blog/updatePost.html', {'forms':fm})
    else:
        return HttpResponseRedirect('/login/')    
    
    
# Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
       if request.method == 'POST':
            pi = Post.objects.get(pk = id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')  