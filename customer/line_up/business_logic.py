import datetime
import pytz
import requests

from redis import Redis
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

import django_rq

from twilio.rest import Client
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from .models import Customer, Store


pnconfig = PNConfiguration()
pnconfig.subscribe_key = settings.PUBNUB_SUBSCRIBE_KEY
pnconfig.publish_key = settings.PUBNUB_PUBLISH_KEY

pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    pass

def send_text(recipient, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(to=recipient.base_number,
                           from_=settings.TWILIO_NUMBER,
                           body=message)
    return HttpResponse("initial message sent!", 200)

def remove_from_line(customer, pubnub_sub_key, pubnub_pub_key):

    send_text(customer, "Your time is up! If you couldn't make it to the store by now, please line up again. Otherwise, ignore this text and have a great day!")

    data = f'{{"number": "{customer.phone_number.base_number}", "operation": "remove"}}'
    response = requests.post(f'https://ps.pndsn.com/publish/{settings.PUBNUB_PUBLISH_KEY}/{settings.PUBNUB_SUBSCRIBE_KEY}/0/pubnub_onboarding_channel/myCallback', data=data)
    customer.time_up = True
    customer.save()

def dequeue_customer(store_id):
    next_customer = Customer.objects.filter(store_line=store_id,
                                            up_next_text_sent=False,
                                            entered_store=False,
                                            no_show=False,
                                            canceled=False,
                                            time_up=False).order_by('created_on')
    if not next_customer:
        return None

    next_customer = next_customer[0]
    store = Store.objects.get(pk=store_id)
    store_timezone = store.timezone
    calculated_time_utc = datetime.datetime.now(pytz.timezone('UTC')) + datetime.timedelta(seconds=20)
    calculated_time_timezone = calculated_time_utc.astimezone(store.timezone)
    formatted_time = calculated_time_timezone.strftime('%I:%M %p')
    send_text(next_customer,    f'It\'s your turn. '
                                'You have until {formatted_time} to enter the store. '
                                'If you can\'t make it by that time, you\'ll have to line up again.')

    pubnub.publish().channel("pubnub_onboarding_channel").message({"number": next_customer.phone_number.base_number, "time": formatted_time, "operation": "add"}).pn_async(my_publish_callback)

    scheduler = django_rq.get_scheduler('default')
    next_customer.up_next_text_sent = True
    next_customer.save()

    scheduler.enqueue_in(datetime.timedelta(seconds=20), remove_from_line, next_customer, settings.PUBNUB_SUBSCRIBE_KEY, settings.PUBNUB_PUBLISH_KEY)
    return next_customer
