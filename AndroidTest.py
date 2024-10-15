import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Simulate data for user 35
user_id = 35
dishes_data = {
    "Patta Gobi": 2.8,
    "Phool Gobi": 2.4,
    "Bhindi": 3.4,
    "Aloo Sabzi": 3.6,
    "Rajma": 3.4,
    "Paneer": 3.8,
    "Chole": 3.6,
    "Baingan": 3.2,
    "Shimla Mirch": 2.9,
    "Sev Tamatar": 1.8,
    "Malai Pyaaz": 2.4,
    "Mix Veg": 2.4,
    "Any Dal": 3.6,
    "Aloo Paratha": 3.4,
    "Pyaaz Paratha": 3.6,
    "Paneer Paratha": 2.4
}
dish_names = list(dishes_data.keys())
dishes = pd.DataFrame([dishes_data], index=[user_id])

# Precomputed similarity matrix for simplicity
dish_similarity = cosine_similarity(dishes.T)

# Dictionary to track recently selected dishes for the user
recently_selected = {}

def select_neighborhood(similarity_matrix, item_id, neighborhood_size):
    item_similarity_scores = similarity_matrix[item_id]
    sorted_indices = np.argsort(item_similarity_scores)[::-1]
    neighborhood = sorted_indices[1:neighborhood_size+1]  # Exclude the item itself
    return neighborhood

def update_data(user_id, selected_dish, neighborhood_size=5):
    hood = select_neighborhood(dish_similarity, selected_dish, neighborhood_size)

    for i in hood:
        current_rating = dishes.loc[user_id, dish_names[i]]
        if dish_similarity[selected_dish][i] < 0.5:
            adjustment = 0.1  # smaller positive adjustment
        else:
            # Only apply negative adjustment if the current rating is well above 1.0
            adjustment = -0.2 if current_rating > 1.2 else 0
        dish_similarity[selected_dish][i] += adjustment

        new_rating = np.clip(dishes.loc[user_id, dish_names[i]] + adjustment, 1, 5)
        new_rating = round(new_rating, 1)
        dishes.loc[user_id, dish_names[i]] = new_rating

    if user_id not in recently_selected:
        recently_selected[user_id] = []
    recently_selected[user_id].append(selected_dish)

    if len(recently_selected[user_id]) > 3:
        recently_selected[user_id].pop(0)

def get_recommendations(user_id, num_recommendations=5):
    user_ratings = dishes.loc[user_id].values
    unrated_dishes = [(i, user_ratings[i]) for i in range(len(user_ratings)) if user_ratings[i] < 3]
    sorted_unrated = sorted(unrated_dishes, key=lambda x: x[1], reverse=True)
    
    recommendations = [(i, score) for i, score in sorted_unrated if i not in recently_selected.get(user_id, [])]

    recoms = [(dish_names[i]) for i, _ in recommendations[:num_recommendations]]
    
    return recoms

def get_recs():
    return get_recommendations(35)