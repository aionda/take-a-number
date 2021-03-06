import json
from requests import get

from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings

from .models import Customer, Store

from .business_logic import send_text, dequeue_customer


def index(request):
    return render(request, 'index.html')


class StoresListView(ListView):

    model = Store
    template_name = 'store_list.html'
    queryset = Store.objects.all().order_by('state')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['stores_list_view'] = True
        return ctx


class SingleStoreListView(ListView):

    template_name = 'store_list.html'

    def get_queryset(self):
        return Store.objects.filter(state=self.kwargs['state'].upper())


class LineupView(CreateView):

    model = Customer
    fields = ['phone_number']
    template_name = 'customer_form.html'

    def get_context_data(self, **kwargs):
        store_obj = Store.objects.get(pk=self.kwargs['store_id'])
        ctx = super().get_context_data(**kwargs)
        ctx['state'] = store_obj.state
        ctx['store'] = store_obj
        ctx['gmaps_api_key'] = settings.GOOGLE_MAPS_KEY
        return ctx

    def form_valid(self, form):
        self.object = form.save(commit=False)
        store_id = self.kwargs['store_id']

        store_obj = Store.objects.get(pk=store_id)
        self.object.store_line = store_obj
        num_customers_in_line = Customer.objects.filter(store_line=store_obj,
                                                        up_next_text_sent=False,
                                                        entered_store=False,
                                                        canceled=False,
                                                        no_show=False,
                                                        time_up=False).count()
        self.object.save()

        send_text(self.object.phone_number, f'You\'re in line for {store_obj.name} at {store_obj.address}. '
                                            f'There are {num_customers_in_line} people in front of you. '
                                            'You\'ll receive a text once we\'re ready for you to show up. '
                                            'You must show up by the time sent in that text. '
                                            'Otherwise, you\'ll have to line up again. NO EXCEPTIONS. '
                                            'Make sure you have good reception. '
                                            'Thanks for doing your part in social distancing.')
        return HttpResponseRedirect(reverse('lineup', args=[store_id]))


class LineManagerView(TemplateView):

    template_name = 'line_manager.html'

    def post(self, request, *args, **kwargs):

        next_customer = dequeue_customer(self.kwargs['store_id'])
        if next_customer:
            next_customer = next_customer.id

        return HttpResponse(
            json.dumps({"next_customer": next_customer}),
            content_type="application/json"
        )

    def get_context_data(self, **kwargs):
        store_obj = Store.objects.get(pk=self.kwargs['store_id'])
        ctx = super().get_context_data(**kwargs)
        ctx['state'] = store_obj.state
        ctx['store'] = store_obj
        ctx['pubnub_publish_key'] = settings.PUBNUB_PUBLISH_KEY
        ctx['pubnub_subscribe_key'] = settings.PUBNUB_SUBSCRIBE_KEY
        return ctx

