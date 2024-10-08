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
# @allowed_users(allowed_roles=['admin', 'technician'])
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
            form.save()
            return redirect('users')
        else:
            for error in form.errors.values():
                messages.error(request, error)

    context = {'form': form}
    return render(request, "itsc_celulares/register_new_user.html", context)


@login_required(login_url='login')
@admin_only
def customer(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, "itsc_celulares/customers.html", context)


@login_required(login_url='login')
@admin_only
def new_customer_entry(request):
    customer_form = CustomerEntryForm()
    if request.method == "POST":
        customer_form = CustomerEntryForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('new-cellphone')

        else:
            for error in customer_form.errors.values():
                messages.error(request, error)

    context = {'form': customer_form}
    return render(request, "itsc_celulares/new_customer_entry.html", context)


@login_required(login_url='login')
@admin_only
def cell_phone(request):
    repair_order_cellphones = RepairOrder.objects.select_related('device').all()

    context = {'repair_order_cellphones': repair_order_cellphones}
    return render(request, "itsc_celulares/cell_phones.html", context)


@login_required(login_url='login')
@admin_only
def new_cellphone_entry(request):
    cellphone_form = CellPhoneEntryForm()
    if request.method == "POST":
        cellphone_form = CellPhoneEntryForm(request.POST)
        if cellphone_form.is_valid():
            cellphone_form.save()
            return redirect('new-entry')
    context = {'form': cellphone_form}
    return render(request, "itsc_celulares/new_cell_phone_entry.html", context)


@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['technician'])
def diagnose_repair_order(request, pk):
    repair_order = RepairOrder.objects.get(id=pk)
    device = CellPhone.objects.get(id=repair_order.device.id)
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['technician'])
def mark_as_fixed(request, pk):
    repair_order = RepairOrder.objects.get(id=pk)
    if request.method == "POST":
        repair_order.order_status = "READY FOR DELIVERY"
        repair_order.save()
        return redirect('technician-page')

    return render(request, "itsc_celulares/technican_page.html")


def tickets(request):
    repair_orders = RepairOrder.objects.all()
    context = {'repair_orders': repair_orders}
    return render(request, "itsc_celulares/tickets.html", context)


def remove_user(request, pk):
    user = Technician.objects.get(id=pk)

    if request.method == "POST":
        user.username.is_active = False
        user.username.save()
        user.delete()

        return redirect('users')

    context = {'user': user}

    return render(request, "itsc_celulares/delete_user.html", context)


def mark_as_delivered(request, pk):
    repair_order = RepairOrder.objects.get(id=pk)

    if request.method == "POST":
        repair_order.order_status = "DELIVERED"
        repair_order.save()

        return redirect('cell-phone')

    return render(request, "itsc_celulares/cell_phones.html")


def password_forgotten(request):
    return render(request, "itsc_celulares/password_forgotten.html")
