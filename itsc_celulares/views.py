from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import UserRegistrationForm


# Create your views here.

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Credenciales invalidas. Intente nuevamente!")
            return redirect('login')
    return render(request, "itsc_celulares/login.html")


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, "itsc_celulares/dashboard.html")


@login_required(login_url='login')
def users(request):
    technicians = Technician.objects.all()
    context = {'technicians': technicians}
    return render(request, "itsc_celulares/users.html", context)


def register_new_user(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            return redirect('users')

    context = {'form': form}
    return render(request, "itsc_celulares/register_new_user.html", context)
