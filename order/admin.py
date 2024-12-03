from django.contrib import admin

from order.models import FoodOrder, Payment, Order


admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(FoodOrder)