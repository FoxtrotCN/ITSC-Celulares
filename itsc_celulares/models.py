from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Technician(models.Model):
    username = models.OneToOneField(User, null=False, blank=False, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=20, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name


class Customer(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    primary_phone_number = models.CharField(max_length=20, null=False, blank=False)
    secondary_phone_number = models.CharField(max_length=20, null=False, blank=True)
    email = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class CellPhone(models.Model):
    brand = models.CharField(max_length=100, null=False, blank=False)
    model = models.CharField(max_length=100, null=False, blank=False)
    serial_number = models.CharField(max_length=100, null=False, blank=False)
    problem_description = models.TextField(null=False, blank=False)
    diagnosis = models.TextField(null=False, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

    def device_brand_model_str_rep(self):
        return f"{self.brand} {self.model}"

    def __str__(self):
        return self.brand


class RepairOrder(models.Model):
    RECEIVED = "RECEIVED"
    IN_DIAGNOSIS = "IN DIAGNOSIS"
    IN_REPAIR = "IN REPAIR"
    READY_FOR_DELIVERY = "READY FOR DELIVERY"
    DELIVERED = "DELIVERED"

    REPAIR_ORDER_STATUS = [
        (RECEIVED, "Recibido"),
        (IN_DIAGNOSIS, "En Diagnostico"),
        (IN_REPAIR, "En Reparacion"),
        (READY_FOR_DELIVERY, "Listo para entrega"),
        (DELIVERED, "Entregado")
    ]

    technician = models.ForeignKey(Technician, on_delete=models.DO_NOTHING)
    device = models.ForeignKey(CellPhone, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100, choices=REPAIR_ORDER_STATUS, default=RECEIVED)

    def __str__(self):
        return f"{self.device.brand} - {self.device.customer}"


