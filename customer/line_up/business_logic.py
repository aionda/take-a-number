from django.conf import settings
from django.http import HttpResponse

from twilio.rest import Client


def send_text(recipient, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(to=recipient.base_number,
                           from_=settings.TWILIO_NUMBER,
                           body=message)
    return HttpResponse("initial message sent!", 200)
