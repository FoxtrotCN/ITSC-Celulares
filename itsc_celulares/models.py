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
        return self.username


class CellPhone(models.Model):
    brand = models.CharField(max_length=100, null=False, blank=False)
    model = models.CharField(max_length=100, null=False, blank=False)
    serial_number = models.CharField(max_length=100, null=False, blank=False)
    problem_description = models.TextField(null=False, blank=False)
    repair_technician = models.ForeignKey(Technician, on_delete=models.DO_NOTHING, related_name="repaired_phones")
    diagnosis = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.brand


