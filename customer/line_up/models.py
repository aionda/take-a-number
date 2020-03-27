from django.db import models
from django.contrib.auth.models import AbstractUser

from address.models import AddressField
from phone_field import PhoneField


class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MyUser(AbstractUser, TimeStampedModel):
	pass


class Store(models.Model):
	name = models.CharField(max_length=200)
	address = AddressField()
	contact_name = models.CharField(max_length=200)
	contact_phone_number = PhoneField()


class Customer(models.Model):
	phone_number = models.PhoneField()
	store_line = models.ForeignKey(Store, on_delete=models.CASCADE)
	up_next_text_sent = models.BooleanField()
	entered_store = models.BooleanField()
	canceled = models.BooleanField()
	image = models.CharField(max_length=500)

