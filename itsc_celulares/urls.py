from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('users/', views.users, name="users"),
    path('users/new', views.register_new_user, name="new"),
]
