from pytz import country_timezones

from django.db import models
from django.contrib.auth.models import AbstractUser

from timezone_field import TimeZoneField
from phone_field import PhoneField


class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Store(TimeStampedModel):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    state = models.CharField(max_length=5)
    contact_name = models.CharField(max_length=200)
    contact_phone_number = PhoneField(E164_only=True)
    timezone = TimeZoneField(choices=[(tz, tz) for tz in country_timezones('us')])
    business_open = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.state = self.state.upper().strip()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name}, {self.address}'


class MyUser(AbstractUser, TimeStampedModel):
    pass


class Customer(TimeStampedModel):
    phone_number = PhoneField(E164_only=True)
    store_line = models.ForeignKey(Store, on_delete=models.CASCADE)
    up_next_text_sent = models.BooleanField(default=False)
    entered_store = models.BooleanField(default=False)
    no_show = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    time_up = models.BooleanField(default=False)
    image = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.phone_number}'

