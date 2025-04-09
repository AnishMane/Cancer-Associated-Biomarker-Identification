# app.py
from flask import Flask, request, jsonify
from joblib import load
import pandas as pd
import numpy as np
from xgboost import XGBClassifier

app = Flask(__name__)

# Load the model and preprocessing components
model = XGBClassifier()
model.load_model(r'D:\repos\Cancer-Associated-Biomarker-Identification\backend\app\ml\pred_ser_data\cancer_model.json')
one_hot_encoder = load(r'D:\repos\Cancer-Associated-Biomarker-Identification\backend\app\ml\pred_ser_data\one_hot_encoder.joblib')
scaler = load(r'D:\repos\Cancer-Associated-Biomarker-Identification\backend\app\ml\pred_ser_data\scaler.joblib')
label_encoder = load(r'D:\repos\Cancer-Associated-Biomarker-Identification\backend\app\ml\pred_ser_data\label_encoder.joblib')
default_values = load(r'D:\repos\Cancer-Associated-Biomarker-Identification\backend\app\ml\pred_ser_data\default_values.joblib')
columns_to_remove = load(r'D:\repos\Cancer-Associated-Biomarker-Identification\backend\app\ml\pred_ser_data\columns_to_remove.joblib')
feature_columns = load(r'D:\repos\Cancer-Associated-Biomarker-Identification\backend\app\ml\pred_ser_data\feature_columns.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.json
        
        # Convert to DataFrame
        input_df = pd.DataFrame([data])
        
        # Apply preprocessing steps exactly as in training
        # Fill missing values with default values
        for col, replacement in default_values.items():
            if col not in input_df.columns:
                input_df[col] = replacement
            else:
                input_df.fillna({col: replacement}, inplace=True)
        
        # Remove columns that were removed during training
        input_df = input_df.drop(columns=[col for col in columns_to_remove if col in input_df.columns])
        
        # Ensure all required columns are present and in the correct order
        for col in feature_columns:
            if col not in input_df.columns:
                input_df[col] = default_values.get(col, 'no')
        
        # Reorder columns to match the training data
        input_df = input_df[feature_columns]
        
        # Apply one-hot encoding
        input_encoded = one_hot_encoder.transform(input_df)
        
        # Apply scaling
        input_scaled = scaler.transform(input_encoded)
        
        # Make prediction
        prediction = model.predict(input_scaled)
        predicted_label = label_encoder.inverse_transform(prediction)[0]
        
        # Get probabilities for all classes
        probabilities = model.predict_proba(input_scaled)[0]
        class_names = label_encoder.inverse_transform(range(len(probabilities)))
        
        # Create dictionary of probabilities
        prob_dict = {str(class_name): float(prob) for class_name, prob in zip(class_names, probabilities)}
        
        return jsonify({
            'prediction': str(predicted_label),
            'probabilities': prob_dict
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/classes', methods=['GET'])
def get_classes():
    """Return all possible class labels"""
    classes = label_encoder.classes_.tolist()
    return jsonify({'classes': classes})

@app.route('/features', methods=['GET'])
def get_features():
    """Return required features for prediction"""
    return jsonify({'features': feature_columns})

if __name__ == '__main__':
    print("Cancer prediction model server running on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)