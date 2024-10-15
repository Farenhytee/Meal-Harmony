import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv("Food survey.csv")

# Set UserID as index and extract dish ratings
df.set_index('UserID', inplace=True)
dishes = df.copy()
dish_names = dishes.columns.values

# Simulate user IDs from the CSV file
users = {user_id: str(user_id) for user_id in df.index}

# Calculate dish similarity
dish_similarity = cosine_similarity(dishes.T)

inventory_df = pd.read_csv('temp_dish_inventory.csv')

ingredient_columns = inventory_df.columns[2:-4].tolist() 
meal_time_columns = inventory_df.columns[-4:].tolist()

ingredients = inventory_df[ingredient_columns].values
meal_times = inventory_df[meal_time_columns].values

# Dictionary to track recently selected dishes for each user
recently_selected = {}

user_selected_ingredients = []  
user_meal_time = []


def display_ingredients(): 
    print("\nSelect available ingredients from the list below by entering their index values:")
    for i, ingredient in enumerate(ingredient_columns, start=1):
        print(f"{i}: {ingredient}")
    
    selected_indices = input("\nEnter the indices of the available ingredients (comma-separated): ").split(",")
    selected_indices = [int(i) - 1 for i in selected_indices]
    selected_ingredients = [1 if i in selected_indices else 0 for i in range(len(ingredient_columns))]
    
    return selected_ingredients


def ask_meal_time():
    meal_time_map = {
        1: 'Breakfast',
        2: 'Lunch',
        3: 'Dinner',
        4: 'Snacks'
    }

    print("\nFor which meal time would you like recommendations?")
    
    # Display meal time options using meal_time_map
    for num, time in meal_time_map.items():
        print(f"{num}: {time}")
    
    selected_time = int(input("\nEnter the number corresponding to your meal time: "))
    
    # Map the selected number to the corresponding meal time string (e.g., 'Lunch')
    if selected_time in meal_time_map:
        selected_meal_time = meal_time_map[selected_time]
        print(f"You have selected: {selected_meal_time}")  # Debugging to show selected meal time
    else:
        print("Invalid selection, defaulting to Lunch")
        selected_meal_time = 'Lunch'
    
    return {selected_meal_time}  # Return the actual meal time string


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
            adjustment = 0.1  
        else:
            adjustment = -0.2 if current_rating > 1.2 else 0
        dish_similarity[selected_dish][i] += adjustment

        dish_name = dish_names[i]

        new_rating = np.clip(dishes.loc[user_id, dish_name] + adjustment, 1, 5)
        new_rating = round(new_rating, 1)
        dishes.loc[user_id, dish_name] = new_rating

    # Track the recently selected dish
    if user_id not in recently_selected:
        recently_selected[user_id] = []
    recently_selected[user_id].append(selected_dish)

    # Limit the number of tracked recent dishes (e.g., 3)
    if len(recently_selected[user_id]) > 3:
        recently_selected[user_id].pop(0)


def get_recommendations(user_id, num_recommendations=5):
    global user_selected_ingredients, user_meal_time

    user_ratings = dishes.loc[user_id].values
    unrated_dishes = [(i, user_ratings[i]) for i in range(len(user_ratings)) if user_ratings[i] < 3]
    sorted_unrated = sorted(unrated_dishes, key=lambda x: x[1], reverse=True)

    # Exclude recently selected dishes from recommendations
    recommendations = [(i, score) for i, score in sorted_unrated if i not in recently_selected.get(user_id, [])]
    
    # print(f"Recommendations before filtering: {recommendations}")
    
    filtered_recommendations = filter_recommendations_by_ingredients_and_time(recommendations, user_selected_ingredients, user_meal_time)
    
    if not filtered_recommendations:
        print("\nNo dishes fully match your available ingredients and selected meal time.")
        print("Recommending top 3 dishes that can be made with your available ingredients...\n")
        
        fallback_recommendations = get_ingredient_match(user_selected_ingredients, user_meal_time)
        return fallback_recommendations

    return filtered_recommendations[:num_recommendations]


def filter_recommendations_by_ingredients_and_time(recommendations, available_ingredients, meal_time):
    filtered_recommendations = []
    
    # Convert available_ingredients and meal_time to sets for faster lookup
    available_ingredients_set = set(available_ingredients)
    meal_time_set = set(meal_time)

    # print(f"Available Ingredients Set: {available_ingredients_set}")
    # print(f"Meal Time Set: {meal_time_set}")
    
    for i, score in recommendations:
        # Get dish ingredients and meal times from the inventory
        dish_row = inventory_df[inventory_df['Item_id'] == i]
        
        if dish_row.empty:
            continue
        
        # Get dish ingredients
        dish_ingredients = set(
            ingredient_columns[j] 
            for j in range(len(ingredient_columns)) 
            if dish_row[ingredient_columns[j]].values[0] == 1
        )
        
        # Get dish meal times
        dish_meal_times = set(
            meal_time_columns[j] 
            for j in range(len(meal_time_columns)) 
            if dish_row[meal_time_columns[j]].values[0] == 1
        )
        
        # print(f"Dish {i} Ingredients: {dish_ingredients}")
        # print(f"Dish {i} Meal Times: {dish_meal_times}")

        # Check if all required dish ingredients are available
        if not dish_ingredients.issubset(available_ingredients_set):
            # If the user does not have all the required ingredients, skip the dish
            continue
        
        # Check if the dish meal times overlap with the selected meal time
        meal_time_matches = not meal_time_set.isdisjoint(dish_meal_times)
        
        if not meal_time_matches:
            continue

        # Add to filtered recommendations if it meets the criteria
        filtered_recommendations.append((i, score))
    
    return filtered_recommendations


def get_ingredient_match(available_ingredients, meal_time):
    available_ingredients_set = set(available_ingredients)
    meal_time_set = set(meal_time)

    matching_dishes = []
    
    for idx, row in inventory_df.iterrows():
        dish_ingredients = set(
            ingredient_columns[j] 
            for j in range(len(ingredient_columns)) 
            if row[ingredient_columns[j]] == 1
        )
        dish_meal_times = set(
            meal_time_columns[j] 
            for j in range(len(meal_time_columns)) 
            if row[meal_time_columns[j]] == 1
        )
        
        if dish_ingredients.issubset(available_ingredients_set):
            meal_time_matches = not set(meal_time).isdisjoint(dish_meal_times)
            
            # Even if the meal time doesn't match fully, suggest the dish if ingredients match
            matching_dishes.append((row['Item_id'], meal_time_matches))

    # Sort fallback dishes to show full meal time matches first
    matching_dishes = sorted(matching_dishes, key=lambda x: x[1], reverse=True)
    
    return matching_dishes[:3]


def interact(user_id):
    global user_selected_ingredients, user_meal_time  
    print(f"Welcome, {users[user_id]}")

    if not user_selected_ingredients:  
        print("Please select the ingredients you have available:")
        
        for i in range(0, len(ingredient_columns), 6):
            row = ingredient_columns[i:i+6]
            print("\t\t".join([f"{i+j+1}: {ingredient}" for j, ingredient in enumerate(row)]))
        
        selected_indices = input("\nEnter the numbers of ingredients you have (comma separated): ")
        selected_indices = [int(i) - 1 for i in selected_indices.split(",")]  # convert input to indices
        
        user_selected_ingredients = [ingredient_columns[i] for i in selected_indices]  # Store user selection
        print(f"\nYou have selected: {', '.join(user_selected_ingredients)}")

    while True:
        print("\nWhat would you like to do?")
        print("1: Get Recommendations")
        print("2: Select a Dish")
        print("3: View Recently Selected Dishes")
        print("99: Exit\n")

        choice = input("Enter your choice: ")

        if choice == "99":
            print("Thank you for using the Food Recommendation System. Goodbye!")
            break
        elif choice == "1":
            user_meal_time = ask_meal_time()
            recommendations = get_recommendations(user_id)

            print("We recommend the following dishes:")
            for i, _ in recommendations:
                print(f"{i}: {dish_names[i]}")

            selection = int(input("\nEnter the number of your selected dish: "))
            update_data(user_id, selection)
            
            print("Your selection has been saved. Enjoy your meal!")
        elif choice == "2":
            print("Please enter the number of the dish you want to select:")
            for i, dish in enumerate(dish_names):
                print(f"{i}: {dish}")

            selection = int(input("\nEnter the number of your selected dish: "))
            update_data(user_id, selection)

            print("Your selection has been saved. Enjoy your meal!")
        elif choice == "3":
            print("Your recently selected dishes are:")
            for dish_id in recently_selected.get(user_id, []):
                print(dish_names[dish_id])
        else:
            print("Invalid choice. Please try again.")