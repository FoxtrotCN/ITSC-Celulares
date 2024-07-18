from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .decorators import *


# Create your views here.

@unauthenticated_user
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
@admin_only
def home(request):
    repair_orders = RepairOrder.objects.all()
    repair_orders_received = repair_orders.filter(order_status="RECEIVED").count()
    repair_orders_in_diagnosis = repair_orders.filter(order_status="IN DIAGNOSIS").count()
    print(repair_orders_in_diagnosis)
    repair_orders_in_repair = repair_orders.filter(order_status="IN REPAIR").count()
    repair_orders_ready_for_delivery = repair_orders.filter(order_status="READY FOR DELIVERY").count()
    repair_orders_delivered = repair_orders.filter(order_status="DELIVERED").count()
    context = {
        'repair_orders': repair_orders,
        'repair_orders_received': repair_orders_received,
        'repair_orders_in_diagnosis': repair_orders_in_diagnosis,
        'repair_orders_in_repair': repair_orders_in_repair,
        'repair_orders_ready_for_delivery': repair_orders_ready_for_delivery,
        'repair_orders_delivered': repair_orders_delivered,
    }

    return render(request, "itsc_celulares/dashboard.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def users(request):
    technicians = Technician.objects.all()
    context = {'technicians': technicians}
    return render(request, "itsc_celulares/users.html", context)


@login_required(login_url='login')
@admin_only
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


def customer(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, "itsc_celulares/customers.html", context)


def new_customer_entry(request):
    customer_form = CustomerEntryForm()
    if request.method == "POST":
        customer_form = CustomerEntryForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('new-cellphone')
    context = {'form': customer_form}
    return render(request, "itsc_celulares/new_customer_entry.html", context)


def cell_phone(request):
    cellphones = CellPhone.objects.all()
    context = {'cellphones': cellphones}
    return render(request, "itsc_celulares/cell_phones.html", context)


def new_cellphone_entry(request):
    cellphone_form = CellPhoneEntryForm()
    if request.method == "POST":
        cellphone_form = CellPhoneEntryForm(request.POST)
        if cellphone_form.is_valid():
            cellphone_form.save()
            return redirect('new-entry')
    context = {'form': cellphone_form}
    return render(request, "itsc_celulares/new_cell_phone_entry.html", context)


def new_entry(request):
    form = NewEntryForm()
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, "itsc_celulares/new_entry.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['technician'])
def technician_page(request):
    is_technician = request.user.groups.filter(name='technician').exists()
    technician_id = request.user.technician.id
    repair_orders = RepairOrder.objects.all()
    technician_repair_orders = repair_orders.filter(technician_id=technician_id)

    context = {
        'is_technician': is_technician,
        'repair_orders': repair_orders,
        'technician_repair_orders': technician_repair_orders,
    }
    return render(request, "itsc_celulares/technican_page.html", context)


def diagnose_repair_order(request, pk):
    repair_order = RepairOrder.objects.get(id=pk)
    device = CellPhone.objects.get(id=repair_order.device.id)
    print(device)
    form = CellPhoneEntryForm(instance=device)
    if request.method == "POST":
        form = CellPhoneEntryForm(request.POST, instance=device)
        if form.is_valid():
            repair_order.order_status = "IN DIAGNOSIS"
            repair_order.save()
            form.save()

            return redirect('technician-page')

    context = {'form': form}
    form.fields['brand'].widget.attrs['readonly'] = True
    form.fields['model'].widget.attrs['readonly'] = True
    form.fields['serial_number'].widget.attrs['readonly'] = True
    form.fields['problem_description'].widget.attrs['readonly'] = True
    form.fields['customer'].widget.attrs['readonly'] = True

    return render(request, "itsc_celulares/diagnose_repair_order.html", context)


def mark_as_fixed(request, pk):
    repair_order = RepairOrder.objects.get(id=pk)
    if request.method == "POST":
        repair_order.order_status = "READY FOR DELIVERY"
        repair_order.save()
        return redirect('technician-page')

    return render(request, "itsc_celulares/technican_page.html")

