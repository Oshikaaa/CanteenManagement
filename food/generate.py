import pandas as pd
from faker import Faker
import random
from sqlalchemy import create_engine


engine = create_engine('postgresql://postgres:bicky@localhost:5432/CM')

# Define categories
categories = ["Breakfast", "Lunch", "Dessert", "Snacks"]
fake = Faker()
# Generate fake food data
fake_food_items = []
for _ in range(100):  # Create 100 fake entries
    food_name = fake.word().capitalize() + " " + fake.word().capitalize()
    description = fake.text(max_nb_chars=200)
    total_cost = round(random.uniform(5, 50), 2)
    food_image = fake.image_url()
    is_available = random.choice([True, False])
    is_soldout = not is_available
    category_id = random.randint(1, len(categories))
    user_id = random.randint(1, 10)  # Assuming 10 users exist

    fake_food_items.append(
        {
            "food_name": food_name,
            "description": description,
            "total_cost": total_cost,
            "food_image": food_image,
            "is_available": is_available,
            "is_soldout": is_soldout,
            "category_id": category_id,
            "user_id": user_id,
        }
    )

# Insert data into the database
import pandas as pd

df = pd.DataFrame(fake_food_items)
df.to_sql("food_fooditem", engine, if_exists="append", index=False)

print("Fake food items inserted successfully!")