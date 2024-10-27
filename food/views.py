from django.shortcuts import render

from food.models import FoodItem

# Create your views here.
def menu(request):
  food_items = FoodItem.objects.all()

  context = {
      "food_items" : food_items
  }
  return render(request , "food/menu.html" , context)