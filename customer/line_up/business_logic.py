from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

from twilio.rest import Client

from .models import Customer


def send_text(recipient, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(to=recipient.base_number,
                           from_=settings.TWILIO_NUMBER,
                           body=message)
    return HttpResponse("initial message sent!", 200)

def dequeue_customer(store_id, message):
    next_customer = Customer.objects.filter(store_line=store_id,
                                            up_next_text_sent=False,
                                            entered_store=False,
                                            canceled=False,
                                            image=None).order_by('created_on')[0]
    # send_text(next_customer,    f'It\'s your turn. '
    #                             'You have until {} to enter the store. '
    #                             'If you can\'t make it by that time, you\'ll have to line up again at {reverse('lineup', args=[store_id])}.')
    print("text", f"It\'s your turn. You have until to enter the store. If you can\'t make it by that time, you\'ll have to line up again at {reverse('lineup', args=[store_id])}.")
    next_customer.up_next_text_sent = True
    # generate image

