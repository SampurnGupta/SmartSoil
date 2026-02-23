from flask import Flask, jsonify, send_from_directory
import os
from flask_cors import CORS
from PIL import ImageStat
from flask import Flask, request, jsonify
from PIL import Image
import io

from prediction.Soil_prediction import (
    open_and_convert_image,
    extract_rgb_values,
    choose_random_rgb_value,
    load_csv_data,
    train_model,
    predict_ph_value,
    get_npk_values,
    find_best_fertilizer
)

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/analyze_soil', methods=['GET'])
def analyze_soil():
    """Capture the latest image, compute simple moisture metric, and return status and action."""
    image_path = os.path.join('captured_images', 'latest.jpg')
    try:
        img = open_and_convert_image(image_path)
        stat = ImageStat.Stat(img)
        mean_val = sum(stat.mean) / len(stat.mean)
        if mean_val < 100:
            moisture = 'low'
            action = 'Soil is dry. \nPlease water your plants.'
        else:
            moisture = 'sufficient'
            action = 'Soil moisture sufficient. No watering needed.'
        image_url = 'http://localhost:5000/captured_images/latest.jpg'
        return jsonify({'image_url': image_url, 'moisture': moisture, 'action': action})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_soil', methods=['GET'])
def predict_soil():
    """Predict pH, NPK values and fertilizer recommendation with Python-native types."""
    image_path = os.path.join('captured_images', 'latest.jpg')
    ph_csv = os.path.join('prediction', 'soilpH_rgb1.csv')
    crop_csv = os.path.join('prediction', 'Crop_recommendation_edited.csv')
    fert_csv = os.path.join('prediction', 'Fertilizer Prediction.csv')
    try:
        img = open_and_convert_image(image_path)
        rgb_vals = extract_rgb_values(img)
        rand_rgb = choose_random_rgb_value(rgb_vals)
        ph_ds = load_csv_data(ph_csv)
        if ph_ds is None:
            return jsonify({'error':'pH dataset not found'}),500
        model = train_model(ph_ds)
        ph_val = predict_ph_value(model, rand_rgb)
        crop_ds = load_csv_data(crop_csv)
        if crop_ds is None:
            return jsonify({'error':'Crop dataset not found'}),500
        res = get_npk_values(crop_ds, ph_val)
        if not res:
            return jsonify({'error':f'No crop data for pH {ph_val}'}),404
        fert_ds = load_csv_data(fert_csv)
        if fert_ds is None:
            return jsonify({'error':'Fertilizer dataset not found'}),500
        best = find_best_fertilizer(
            fert_ds,
            float(res['Nitrogen (N)']),
            float(res['Phosphorus (P)']),
            float(res['Potassium (K)'])
        )
        response = {
            'ph_value': float(ph_val),
            'NPK': {
                'Nitrogen (N)': int(res['Nitrogen (N)']),
                'Phosphorus (P)': int(res['Phosphorus (P)']),
                'Potassium (K)': int(res['Potassium (K)']),
                'Crop(C)': res['Crop(C)']
            },
            'recommended_fertilizer': best
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# route for Mobile App to upload soil image and get prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream)

    # Your soil processing logic
    # Example: Convert to RGB, predict, etc.
    rgb = image.resize((1, 1)).getpixel((0, 0))  # Dummy RGB
    result = {'r': rgb[0], 'g': rgb[1], 'b': rgb[2], 'ph': 6.5}

    return jsonify(result)

@app.route('/captured_images/<filename>')
def serve_captured_image(filename):
    """Serve the latest captured soil image."""
    return send_from_directory('captured_images', filename)

if __name__ == '__main__':
    app.run(debug=True)


