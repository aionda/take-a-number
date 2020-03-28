from django.db import models
from django.contrib.auth.models import AbstractUser

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
	address = models.CharField(max_length=500)
	state = models.CharField(max_length=5)
	contact_name = models.CharField(max_length=200)
	contact_phone_number = PhoneField(E164_only=True)

	def __str__(self):
		return f'{self.name}, {self.address}'


class Customer(models.Model):
	phone_number = PhoneField(E164_only=True)
	store_line = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
	up_next_text_sent = models.BooleanField(default=False)
	entered_store = models.BooleanField(default=False)
	canceled = models.BooleanField(default=False)
	image = models.CharField(max_length=500)

	def __str__(self):
		return f'{self.phone_number}'

