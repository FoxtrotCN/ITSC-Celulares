from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from .models import Technician


def technician_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='technician')
        instance.groups.add(group)
        Technician.objects.create(username=instance, first_name=instance.first_name, last_name=instance.last_name)


post_save.connect(technician_profile, sender=User)
