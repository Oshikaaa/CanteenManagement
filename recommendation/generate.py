
from django.utils.text import slugify
import sys
import os
import django

# Set up Django environment
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CanteenManagement.settings")
django.setup()


import random
from account.models import User
from food.models import Category, FoodItem, Rating
from faker import Faker
# Initialize Faker
fake = Faker()

# Create Categories
categories = ["Breakfast", "Lunch", "Snacks"]
created_categories = {}

# Create Categories in Database
for category_name in categories:
    category, _ = Category.objects.get_or_create(category_name=category_name)
    created_categories[category_name] = category

# Create Food Items
# Create Food Items
food_items = {
    "Breakfast": ["Pancakes", "Egg Sandwich", "Aloo Paratha", "Muesli", "French Toast"],
    "Lunch": ["Chicken Curry", "Fried Rice", "Grilled Chicken", "Tuna Salad", "Beef Stew"],
    "Snacks": ["Nachos", "Spring Rolls", "Hot Dog", "Garlic Bread", "Cheese Balls"],
}
# Create Admin User
admin_user, _ = User.objects.get_or_create(
    email="admin@canteen.com",
    username="admin",
    first_name="Admin",
    last_name="User",
    role=User.ADMIN,
    is_active=True,
    is_staff=True,
    is_superadmin=True
)
admin_user.set_password("admin123")
admin_user.save()

# Generate Unique Food Items
food_item_count = FoodItem.objects.count()
while food_item_count < 100:
    category_name = random.choice(categories)
    food_name = fake.unique.word().capitalize() + " " + fake.unique.word().capitalize()
    FoodItem.objects.get_or_create(
        user=admin_user,
        food_name=food_name,
        category=created_categories[category_name],
        description=fake.text(max_nb_chars=200),
        slug=slugify(food_name),
        total_cost=round(random.uniform(5, 50), 2),
        is_available=True,
        is_soldout=False,
    )
    food_item_count += 1

# Create Dummy Users
users = list(User.objects.filter(role=User.CUSTOMER))
while len(users) < 100:
    user, _ = User.objects.get_or_create(
        email=f"user{len(users)+1}@canteen.com",
        username=f"user{len(users)+1}",
        first_name=f"User{len(users)+1}",
        last_name="Test",
        role=User.CUSTOMER,
        is_active=True,
    )
    user.set_password(f"user{len(users)+1}123")
    user.save()
    users.append(user)

# Generate Unique Ratings
food_items_in_db = list(FoodItem.objects.all())
existing_ratings = set(Rating.objects.values_list('user_id', 'food_item_id'))

for user in users:
    sampled_foods = random.sample(food_items_in_db, 15)
    for food_item in sampled_foods:
        if (user.id, food_item.id) not in existing_ratings:
            Rating.objects.create(
                user=user,
                food_item=food_item,
                rating=round(random.uniform(1.0, 5.0), 1)
            )
            existing_ratings.add((user.id, food_item.id))

print("Custom dataset with 100 unique users and 100 unique food items created successfully!")
