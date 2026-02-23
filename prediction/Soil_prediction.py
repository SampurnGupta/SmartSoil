#Final Code is this snippet
from PIL import Image
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def open_and_convert_image(image_path):
    # Open the image and convert it to RGB mode
    img = Image.open(image_path)
    img = img.convert("RGB")
    return img

def extract_rgb_values(img):
    # Extract RGB values from the image
    pixels = list(img.getdata())
    rgb_values = [pixel[:3] for pixel in pixels]
    return rgb_values

def choose_random_rgb_value(rgb_values):
    # Choose a random RGB value from the list
    list_of_sets = rgb_values[:10]
    random_sublist = random.choice(list_of_sets)
    return random_sublist

def load_csv_data(csv_file):
    # Load the dataset from a CSV file
    try:
        df = pd.read_csv(csv_file)
        return df
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None

def train_model(dataset):
    # Train a Random Forest model to predict pH value from RGB values
    X = dataset[['R', 'G', 'B']]
    y = dataset['pH']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    y_pred = rf_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error for Random Forest: {mse}")
    
    return rf_model

def predict_ph_value(model, rgb_values):
    # Predict the pH value using the trained Random Forest model
    rgb_df = pd.DataFrame([rgb_values], columns=['R', 'G', 'B'])
    ph_value = model.predict(rgb_df)[0]
    return ph_value

def get_npk_values(dataset, pH_value):
    # Retrieve N, P, K values based on pH input
    row = dataset[dataset['ph_round'] == round(pH_value)]
    if not row.empty:
        return {
            'Nitrogen (N)': row['Nitrogen'].values[0],
            'Phosphorus (P)': row['phosphorus'].values[0],
            'Potassium (K)': row['potassium'].values[0],
            'Crop(C)': row['label'].values[0]
        }
    else:
        return None

def calculate_distance(x1, y1, z1, x2, y2, z2):
    # Calculate Euclidean distance between two points
    return ((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)**0.5

def find_best_fertilizer(dataset, target_N, target_P, target_K):
    # Find the best fertilizer based on N, P, K values
    min_distance = float('inf')
    best_fertilizer = None
    for index, row in dataset.iterrows():
        fertilizer_N = row['Nitrogen']
        fertilizer_P = row['Potassium']
        fertilizer_K = row['Phosphorous']
        distance = calculate_distance(target_N, target_P, target_K, fertilizer_N, fertilizer_P, fertilizer_K)
        if distance < min_distance:
            min_distance = distance
            best_fertilizer = row['Fertilizer Name']
    return best_fertilizer

def main():
    # Paths to the files
    image_path =  r"C:\DT_Final\captured_images\latest.jpg"
    ph_csv_file = r"C:\DT_Final\prediction\soilpH_rgb1.csv"
    crop_csv_file = r"C:\DT_Final\prediction\Crop_recommendation_edited.csv"
    fertilizer_csv_file = r"C:\DT_Final\prediction\Fertilizer Prediction.csv"
    
    # Step 1: Open and convert the image
    img = open_and_convert_image(image_path)
    
    # Step 2: Extract RGB values from the image
    rgb_values = extract_rgb_values(img)
    
    # Step 3: Choose a random RGB value
    random_sublist = choose_random_rgb_value(rgb_values)
    
    # Step 4: Load pH dataset
    ph_dataset = load_csv_data(ph_csv_file)
    
    if ph_dataset is not None:
        # Step 5: Train Random Forest model
        rf_model = train_model(ph_dataset)
        
        # Step 6: Predict pH value using Random Forest
        ph_value_rf = predict_ph_value(rf_model, random_sublist)
        print("Predicted pH value (Random Forest):", ph_value_rf)
        
        # Step 7: Load crop dataset and get NPK values based on pH value from Random Forest
        crop_dataset = load_csv_data(crop_csv_file)
        if crop_dataset is not None:
            result = get_npk_values(crop_dataset, ph_value_rf)
            if result:
                print(f"At pH {ph_value_rf}:")
                for nutrient, value in result.items():
                    print(f"{nutrient}: {value}")
            else:
                print(f"No data found for pH {ph_value_rf}")
    
    # Step 8: Load fertilizer dataset and find the best fertilizer
    fertilizer_dataset = load_csv_data(fertilizer_csv_file)
    if fertilizer_dataset is not None and 'Nitrogen (N)' in result and 'Phosphorus (P)' in result and 'Potassium (K)' in result:
        target_N = float(result['Nitrogen (N)'])
        target_P = float(result['Phosphorus (P)'])
        target_K = float(result['Potassium (K)'])
        best_fertilizer = find_best_fertilizer(fertilizer_dataset, target_N, target_P, target_K)
        if best_fertilizer:
            print(f"The recommended fertilizer is: {best_fertilizer}")
        else:
            print("No suitable fertilizer found in the dataset.")

if __name__ == '__main__':
    main()
