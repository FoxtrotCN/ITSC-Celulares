from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_page, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('users/', views.users, name="users"),
    path('users/new', views.register_new_user, name="new"),
    path('customers/', views.customer, name="customer"),
    path('customers/new', views.new_customer_entry, name="new-customer"),
    path('cell-phones/', views.cell_phone, name="cell-phone"),
    path('cell-phones/new', views.new_cellphone_entry, name="new-cellphone"),
    path('new-entry/', views.new_entry, name="new-entry"),
    path('technician/', views.technician_page, name="technician-page")
]
