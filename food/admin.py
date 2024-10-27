from django.contrib import admin

from .models import Category, FoodItem, Tax
from .models import Cart
from decimal import Decimal





class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'quantity', 'updated_at')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Category)
admin.site.register(FoodItem )