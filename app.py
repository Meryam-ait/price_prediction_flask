from flask import Flask, request, jsonify
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load the saved model
model_filename = 'xgb_regressor_model.pkl'
with open(model_filename, 'rb') as file:
    xgb_regressor = pickle.load(file)

# Initialize the LabelEncoders and StandardScaler
label_encoders = {}
scaler = StandardScaler()

# Load the previously saved encoders and scaler
with open('label_encoders.pkl', 'rb') as file:
    label_encoders = pickle.load(file)
with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON data
        data = request.json

        # Extract user inputs
        abtest = data['abtest']
        vehicle_type = data['vehicleType']
        gearbox = data['gearbox']
        model = data['model']
        fuel_type = data['fuelType']
        brand = data['brand']
        not_repaired_damage = data['notRepairedDamage']
        kilometer = data['kilometer']
        power_ps = data['powerPS']
        car_age = data['carAge']

        # Encode categorical variables
        encoded_inputs = [
            label_encoders['abtest'].transform([abtest])[0],
            label_encoders['vehicleType'].transform([vehicle_type])[0],
            label_encoders['gearbox'].transform([gearbox])[0],
            label_encoders['model'].transform([model])[0],
            label_encoders['fuelType'].transform([fuel_type])[0],
            label_encoders['brand'].transform([brand])[0],
            label_encoders['notRepairedDamage'].transform([not_repaired_damage])[0]
        ]

        # Normalize numerical variables
        numerical_inputs = scaler.transform([[kilometer, power_ps, car_age]])

        # Combine encoded and numerical features
        features = np.array([encoded_inputs + numerical_inputs[0].tolist()])

        # Make prediction
        prediction = xgb_regressor.predict(features)

        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
