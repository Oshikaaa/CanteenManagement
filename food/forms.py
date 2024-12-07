from django import forms
from .models import FoodItem, Category  # Import FoodItem and Category models

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['food_name', 'category', 'description', 'total_cost', 'food_image', 'is_available']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

