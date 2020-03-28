from django.contrib import admin

from .models import Customer, Store


admin.site.register(Customer, admin.ModelAdmin)
admin.site.register(Store, admin.ModelAdmin)
