from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load data
df = pd.read_csv("Food survey.csv")
df.set_index('UserID', inplace=True)
dishes = df.copy()
dish_names = dishes.columns.values

inventory_df = pd.read_csv('temp_dish_inventory.csv')
ingredient_columns = inventory_df.columns[2:-4].tolist()
meal_time_columns = inventory_df.columns[-4:].tolist()

ingredients = inventory_df[ingredient_columns].values
meal_times = inventory_df[meal_time_columns].values

# Calculate dish similarity
dish_similarity = cosine_similarity(dishes.T)

# Dictionary to track recently selected dishes for each user
recently_selected = {}

# Linear Regression Model
x = np.array(df)
y = np.arange(len(df)).reshape(-1, 1)
linear_model = LinearRegression().fit(y, x)

users = {user_id: str(user_id) for user_id in df.index}


# Helper Functions
def validate_user(user_id):
    return user_id in dishes.index


def check_ingredients(dish_id, available_ingredients):
    dish_row = inventory_df[inventory_df['Item_id'] == dish_id]
    if dish_row.empty:
        return False

    dish_ingredients = set(
        ingredient_columns[j]
        for j in range(len(ingredient_columns))
        if dish_row[ingredient_columns[j]].values[0] == 1
    )
    available_ingredients_set = set(available_ingredients)
    return dish_ingredients.issubset(available_ingredients_set)


def select_neighborhood(similarity_matrix, item_id, neighborhood_size):
    item_similarity_scores = similarity_matrix[item_id]
    sorted_indices = np.argsort(item_similarity_scores)[::-1]
    neighborhood = sorted_indices[1:neighborhood_size + 1]  # Exclude the item itself
    return neighborhood


def retry_cosine_similarity(user_id, recommendations, num_recommendations=5):
    filtered_recommendations = []

    for i, _ in recommendations:
        # Check if the ingredients match
        if check_ingredients(i, recently_selected.get(user_id, [])):
            filtered_recommendations.append((i, _))

    # If still no recommendations, fall back to cosine similarity
    if not filtered_recommendations:
        dish_indices = [i for i, _ in recommendations]
        dish_scores = [similarity for _, similarity in recommendations]

        # Sort by highest cosine similarity scores
        sorted_indices = np.argsort(dish_scores)[::-1]
        for idx in sorted_indices:
            if len(filtered_recommendations) < num_recommendations:
                filtered_recommendations.append((dish_indices[idx], dish_scores[idx]))
            else:
                break

    return filtered_recommendations


def get_recommendations(user_id, selected_ingredients, meal_time):
    user_ratings = dishes.loc[user_id].values
    unrated_dishes = [(i, user_ratings[i]) for i in range(len(user_ratings)) if user_ratings[i] < 3]
    sorted_unrated = sorted(unrated_dishes, key=lambda x: x[1], reverse=True)

    recommendations = [(i, score) for i, score in sorted_unrated if i not in recently_selected.get(user_id, [])]

    # Filter based on ingredients
    filtered_recommendations = []
    for i, score in recommendations:
        if check_ingredients(i, selected_ingredients):
            filtered_recommendations.append((i, score))

    if not filtered_recommendations:
        flash("No dishes fully match your available ingredients. Trying with similar dishes...")
        filtered_recommendations = retry_cosine_similarity(user_id, recommendations)

    return [(i, dish_names[i]) for i, score in filtered_recommendations[:5]]



def update_data(user_id, selected_dish, neighborhood_size=5):
    hood = select_neighborhood(dish_similarity, selected_dish, neighborhood_size)

    for i in hood:
        current_rating = dishes.loc[user_id, dish_names[i]]
        if dish_similarity[selected_dish][i] < 0.5:
            adjustment = 0.1
        else:
            adjustment = -0.2 if current_rating > 1.2 else 0
        dish_similarity[selected_dish][i] += adjustment

        dish_name = dish_names[i]

        new_rating = np.clip(dishes.loc[user_id, dish_name] + adjustment, 1, 5)
        new_rating = round(new_rating, 1)
        print(f"User {user_id}: Dish '{dish_names[i]}' - Previous Rating: {current_rating}, Updated Rating: {new_rating}")
        dishes.loc[user_id, dish_name] = new_rating

    #? Track the recently selected dish
    if user_id not in recently_selected:
        recently_selected[user_id] = []
    recently_selected[user_id].append(selected_dish)

    #? Limit the number of tracked recent dishes (e.g., 3)
    if len(recently_selected[user_id]) > 3:
        recently_selected[user_id].pop(0)

    #? Save the updated data to CSV
    df.loc[user_id] = dishes.loc[user_id]
    df.to_csv("Food survey.csv")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        if validate_user(user_id):
            return redirect(url_for('interact', user_id=user_id))
        else:
            flash("User does not exist. Please create a new account.")
            return redirect(url_for('create_account'))
    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        name = request.form['username']
        new_data = linear_model.predict([[user_id]])
        new_ratings = np.clip(new_data[0], 1, 5)
        new_ratings = np.round(new_ratings, 1)

        new_user_data = pd.Series(new_ratings, index=dishes.columns, name=user_id)
        dishes.loc[user_id] = new_ratings
        df.loc[user_id] = new_ratings
        df.to_csv("Food survey.csv", index_label='UserID')
        return redirect(url_for('interact', user_id=user_id))
    return render_template('create.html')


@app.route('/interact/<int:user_id>', methods=['GET', 'POST'])
def interact(user_id):
    if request.method == 'POST':
        meal_time = request.form['meal_time']
        selected_ingredients = request.form.getlist('ingredients')
        recommendations = get_recommendations(user_id, selected_ingredients, meal_time)
        return render_template('recommendations.html', user_id=user_id, recommendations=recommendations)
    return render_template('interact.html', user_id=user_id, ingredients=ingredient_columns)


@app.route('/select_dish/<int:user_id>/<int:dish_id>')
def select_dish(user_id, dish_id):
    update_data(user_id, dish_id)
    flash(f"You have selected {dish_names[dish_id]}")
    return redirect(url_for('interact', user_id=user_id))


if __name__ == "__main__":
    app.run(debug=True)
