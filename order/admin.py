from django.contrib import admin

from order.models import Payment, Order


admin.site.register(Payment)
admin.site.register(Order)