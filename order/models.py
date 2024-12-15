import json
from django.db import models
from account.models import User

from decimal import Decimal

# Create your models here.
import logging

from food.models import FoodItem
class Payment(models.Model):
    pidx = models.CharField(max_length=255, unique=True)
    
    payment_status = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.pidx or "Payment"
    

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(null=True , blank=True)

    order_number = models.CharField(max_length=20)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=25, blank=True)
    city = models.CharField(max_length=50)

    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text = "Data format: {'tax_type':{'tax_percentage':'tax_amount'}}" , null=True)
    total_tax = models.FloatField(blank=True, null=True)
    total_data = models.JSONField(blank=True, null=True)

    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return f"Order {self.order_number} - Placed to: {self.order_placed_to()}"

    def get_total_by_vendor(self, vendor):
        subtotal = 0
        tax = 0
        tax_dict = {}

        if self.total_data:
            tax_data = json.loads(self.tax_data)
            data = tax_data.get(str(vendor.id))

            for key, val in data.items():
                val_float = float(val)  # Convert val to float
                subtotal += val_float
                val = val.replace("'", '"')
                val = json.loads(val)
                tax_dict.update(val)

                # Calculate tax
                # {'CGST': {'9.00': '6.03'}, 'SGST': {'7.00': '4.69'}}
                for i in val:
                    for j in val[i]:
                        tax += float(val[i][j])

        grand_total = subtotal + tax  # No need to convert to float again
        context = {
            'subtotal': subtotal,
            'tax_dict': tax_dict,
            'grand_total': grand_total,
        }


        return context

    def __str__(self):
      return f"Order {self.order_number} - Placed by: {self.user.first_name} "

 
class FoodOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_item.food_name


    