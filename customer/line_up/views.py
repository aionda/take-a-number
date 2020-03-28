from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Customer, Store

from .business_logic import send_text


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


class LineupView(CreateView):
    model = Customer
    fields = ['phone_number']
    template_name = 'customer_form.html'

    def get_context_data(self, **kwargs):
        store_obj = Store.objects.get(pk=self.kwargs['store_id'])
        ctx = super().get_context_data(**kwargs)
        ctx['state'] = store_obj.state
        ctx['store'] = store_obj
        return ctx

    def form_valid(self, form):
        self.object = form.save(commit=False)
        store_id = self.kwargs['store_id']

        store_obj = Store.objects.get(pk=store_id)
        self.object.store_line = store_obj
        num_customers_in_line = Customer.objects.filter(store_line=store_obj,
                                                        up_next_text_sent=False,
                                                        entered_store=False,
                                                        canceled=False).count()

        self.object.save()

        # send_text(self.object.phone_number, f'You\'re in line for {store_obj.name} at {store_obj.address}. '
        #                                     'There are {num_customers_in_line} people in front of you.'
        #                                     'You\'ll receive a text once we\'re ready for you to show up. '
        #                                     'You must show up within 5 minutes after that text is sent. '
        #                                     'Otherwise, you\'ll have to line up again. '
        #                                     'Thanks for doing your part in social distancing.')
        return HttpResponseRedirect(reverse('lineup', args=[store_id]))
