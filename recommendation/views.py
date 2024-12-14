from django.shortcuts import render
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.decorators import login_required

from food.models import FoodItem

@login_required
def recommend_view(request):
    user_id = request.user.id

    # Load datasets
    food_df = pd.read_csv('food_processing_dataset.csv')
    rating_df = pd.read_csv('food_ratings.csv')

    # Build user-item matrix
    user_item_matrix = rating_df.pivot_table(
        index='User_ID', columns='Food_ID', values='Rating', fill_value=0
    )

    # Calculate item similarity
    item_similarity = cosine_similarity(user_item_matrix.T)
    item_similarity_df = pd.DataFrame(
        item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns
    )

    # Recommendation logic
    if user_id not in user_item_matrix.index:
        recommended_food_ids = []
    else:
        user_ratings = user_item_matrix.loc[user_id]
        user_unrated_items = user_ratings[user_ratings == 0].index.tolist()

        # Predict ratings for unrated items
        item_scores = {}
        for item in user_unrated_items:
            similar_items = item_similarity_df[item]
            user_scores = user_ratings[user_ratings > 0]
            item_scores[item] = sum(user_scores * similar_items[user_scores.index]) / (
                sum(similar_items[user_scores.index]) + 1e-9
            )

        recommended_items_ids = sorted(
            item_scores.items(), key=lambda x: x[1], reverse=True
        )[:5]
        recommended_food_ids = [item for item, _ in recommended_items_ids]

    # Fetch matching food items from the database
    recommended_food = FoodItem.objects.filter(id__in=recommended_food_ids)

    print("recommended foods ===>" , recommended_food)

    context = {'recommended_food': recommended_food}
    return render(request, 'food/recommendation.html', context)
