
# from django.utils.text import slugify
# import sys
# import os
# import django

# # Set up Django environment
# PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# if PROJECT_DIR not in sys.path:
#     sys.path.insert(0, PROJECT_DIR)

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CanteenManagement.settings")
# django.setup()


# import random
# from account.models import User
# from food.models import Category, FoodItem, Rating
# from faker import Faker
# # Initialize Faker
# fake = Faker()



# food_data = {
#     "Breakfast": [
#         ("Pancakes", "Fluffy pancakes served with syrup and butter."),
#         ("Egg Sandwich", "Toasted sandwich with egg, cheese, and bacon."),
#         ("Aloo Paratha", "Indian flatbread stuffed with spiced potatoes."),
#         ("Muesli", "A healthy mix of oats, nuts, and dried fruits."),
#         ("French Toast", "Bread soaked in egg and milk, then fried until golden."),
#         ("Bagel", "A dense bread roll, often served with cream cheese."),
#         ("Smoothie Bowl", "A blend of fruits topped with granola and seeds."),
#         ("Omelet", "Egg-based dish with vegetables and cheese."),
#         ("Waffles", "Crispy waffles served with syrup and fruits."),
#         ("Breakfast Burrito", "A tortilla filled with eggs, bacon, and veggies.")
#     ],
#     "Lunch": [
#         ("Chicken Curry", "Tender chicken simmered in a rich, spiced curry sauce."),
#         ("Fried Rice", "Stir-fried rice with vegetables, eggs, and choice of meat."),
#         ("Grilled Chicken", "Marinated chicken grilled to perfection."),
#         ("Tuna Salad", "A fresh salad with tuna, lettuce, tomatoes, and dressing."),
#         ("Beef Stew", "Slow-cooked beef with vegetables in a hearty broth."),
#         ("Spaghetti Bolognese", "Pasta served with a rich meat sauce."),
#         ("Vegetable Stir Fry", "A mix of stir-fried vegetables in a savory sauce."),
#         ("Lamb Kebabs", "Grilled lamb skewers with spices and herbs."),
#         ("Caesar Salad", "Crispy lettuce with Caesar dressing and croutons."),
#         ("Veggie Burger", "Grilled vegetable patty served in a bun.")
#     ],
#     "Snacks": [
#         ("Nachos", "Crispy tortilla chips topped with melted cheese and salsa."),
#         ("Spring Rolls", "Vegetable-filled crispy rolls with dipping sauce."),
#         ("Hot Dog", "Grilled sausage served in a bun with condiments."),
#         ("Garlic Bread", "Bread topped with garlic and butter, baked until crispy."),
#         ("Cheese Balls", "Fried balls of cheese with a crispy coating."),
#         ("Samosa", "Crispy pastry filled with spiced potatoes and peas."),
#         ("Chicken Wings", "Spicy wings served with dipping sauce."),
#         ("Popcorn", "Lightly salted or buttered popcorn."),
#         ("Fruit Salad", "Fresh seasonal fruits mixed together."),
#         ("Pretzels", "Baked twisted bread with salt.")


#     ],
# }

# # Create Categories in Database
# created_categories = {}
# for category_name in food_data.keys():
#     category, _ = Category.objects.get_or_create(category_name=category_name)
#     created_categories[category_name] = category

# # Create Admin User
# admin_user, _ = User.objects.get_or_create(
#     email="admin@canteen.com",
#     username="admin",
#     first_name="Admin",
#     last_name="User",
#     role=User.ADMIN,
#     is_active=True,
#     is_staff=True,
#     is_superadmin=True
# )
# admin_user.set_password("admin123")
# admin_user.save()

# # Populate Food Items
# for category_name, items in food_data.items():
#     for food_name, description in items:
#         FoodItem.objects.get_or_create(
#             user=admin_user,
#             food_name=food_name,
#             category=created_categories[category_name],
#             description=description,
#             slug=slugify(food_name),
#             total_cost=round(random.uniform(5, 50), 2),
#             is_available=True,
#             is_soldout=False,
#         )

# # Create Dummy Users
# users = list(User.objects.filter(role=User.CUSTOMER))
# while len(users) < 100:
#     user, _ = User.objects.get_or_create(
#         email=f"user{len(users)+1}@canteen.com",
#         username=f"user{len(users)+1}",
#         first_name=f"User{len(users)+1}",
#         last_name="Test",
#         role=User.CUSTOMER,
#         is_active=True,
#     )
#     user.set_password(f"user{len(users)+1}123")
#     user.save()
#     users.append(user)

# # Generate Unique Ratings
# food_items_in_db = list(FoodItem.objects.all())
# existing_ratings = set(Rating.objects.values_list('user_id', 'food_item_id'))

# for user in users:
#     sampled_foods = random.sample(food_items_in_db, 15)
#     for food_item in sampled_foods:
#         if (user.id, food_item.id) not in existing_ratings:
#             Rating.objects.create(
#                 user=user,
#                 food_item=food_item,
#                 rating=round(random.uniform(1.0, 5.0), 1)
#             )
#             existing_ratings.add((user.id, food_item.id))

# print("Custom dataset with 100 unique users and 50+ real food items created successfully!")
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
    'user_id', 'food_item_id', 'rating'
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