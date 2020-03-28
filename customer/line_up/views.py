from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Customer, Store


def index(request):
    return render(request, 'index.html')


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
        self.object.save()
        return HttpResponseRedirect(reverse('lineup', args=[store_id]))
