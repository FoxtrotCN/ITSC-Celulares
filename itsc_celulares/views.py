from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, "itsc_celulares/login.html")


def home(request):
    return render(request, "itsc_celulares/dashboard.html")


def users(request):
    return render(request, "itsc_celulares/users.html")
