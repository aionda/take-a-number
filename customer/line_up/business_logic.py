import datetime
import pytz

from redis import Redis
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

import django_rq

from twilio.rest import Client

from .models import Customer, Store


def send_text(recipient, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(to=recipient.base_number,
                           from_=settings.TWILIO_NUMBER,
                           body=message)
    return HttpResponse("initial message sent!", 200)

def remove_from_line(customer):
    # function called after 5 mins will remove it from pubnub, remove color letter combo from redis
    print("Your time is up! If you couldn't make it to the store, please line up again.")
    # send_text(customer, "Your time is up! If you couldn't make it to the store, please line up again.")
    customer.time_up = True
    customer.save()

def dequeue_customer(store_id):
    next_customer = Customer.objects.filter(store_line=store_id,
                                            up_next_text_sent=False,
                                            entered_store=False,
                                            no_show=False,
                                            canceled=False).order_by('created_on')
    if not next_customer:
        print("no customer in line")
        return

    next_customer = next_customer[0]
    store = Store.objects.get(pk=store_id)
    store_timezone = store.timezone
    calculated_time_utc = datetime.datetime.now(pytz.timezone('UTC')) + datetime.timedelta(minutes=5)
    calculated_time_timezone = calculated_time_utc.astimezone(store.timezone)
    formatted_time = calculated_time_timezone.strftime('%I:%M %p')
    # send_text(next_customer,    f'It\'s your turn. '
    #                             'You have until {formatted_time} to enter the store. '
    #                             'If you can\'t make it by that time, you\'ll have to line up again at {reverse('lineup', args=[store_id])}.')

    # generate image url
    # 26*4(red,white,blue,yellow)
    # check redis that color letter combo is not in the db
    # add color letter combo to db
    print("text",   f'It\'s your turn. You have until {formatted_time} to enter the store. '
                    'If you can\'t make it by that time, '
                    'you\'ll have to line up again.')

    scheduler = django_rq.get_scheduler('default')
    next_customer.up_next_text_sent = True
    next_customer.save()

    scheduler.enqueue_in(datetime.timedelta(minutes=1), remove_from_line, next_customer)

