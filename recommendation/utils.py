import os
import django
import pandas as pd

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CanteenManagement.settings')
django.setup()

# Import models after Django setup
from food.models import FoodItem, Rating

# Fetch food data
food_queryset = FoodItem.objects.all().values(
    'id', 'food_name', 'category', 'description'
)

# Convert to DataFrame
food_df = pd.DataFrame(list(food_queryset))
food_df.columns = ['Food_ID', 'Name', 'C_Type', 'Describe']

# Fetch ratings data
rating_queryset = Rating.objects.all().values(
    'user__id', 'food_item__id', 'rating'
)

# Convert to DataFrame
rating_df = pd.DataFrame(list(rating_queryset))
rating_df.columns = ['User_ID', 'Food_ID', 'Rating']

# Export to CSV
food_file_path = 'food_processing_dataset.csv'
rating_file_path = 'food_ratings.csv'

food_df.to_csv(food_file_path, index=False)
rating_df.to_csv(rating_file_path, index=False)

print(f"Datasets exported: {food_file_path}, {rating_file_path}")
