from flask import Flask, request, jsonify, Response
from joblib import load
import pandas as pd
import numpy as np
import os
from xgboost import XGBClassifier
import logging
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure paths - adjust these to your actual paths
BASE_DIR = r'D:\Projects\EPICS\temp\Cancer-Associated-Biomarker-Identification\backend\app\ml\pred_ser_data'

# Initialize variables
model = None
one_hot_encoder = None
scaler = None
label_encoder = None
default_values = None
columns_to_remove = None
feature_columns = None

# Load model components
def load_model_components():
    global model, one_hot_encoder, scaler, label_encoder
    global default_values, columns_to_remove, feature_columns
    
    try:
        # Check if files exist
        required_files = {
            'model': os.path.join(BASE_DIR, 'cancer_model.json'),
            'one_hot_encoder': os.path.join(BASE_DIR, 'one_hot_encoder.joblib'),
            'scaler': os.path.join(BASE_DIR, 'scaler.joblib'),
            'label_encoder': os.path.join(BASE_DIR, 'label_encoder.joblib'),
            'default_values': os.path.join(BASE_DIR, 'default_values.joblib'),
            'columns_to_remove': os.path.join(BASE_DIR, 'columns_to_remove.joblib'),
            'feature_columns': os.path.join(BASE_DIR, 'feature_columns.joblib')
        }
        
        for name, path in required_files.items():
            if not os.path.exists(path):
                logger.error(f"Missing file: {path}")
                return False
        
        # Load components
        model = XGBClassifier()
        model.load_model(required_files['model'])
        one_hot_encoder = load(required_files['one_hot_encoder'])
        scaler = load(required_files['scaler'])
        label_encoder = load(required_files['label_encoder'])
        default_values = load(required_files['default_values'])
        columns_to_remove = load(required_files['columns_to_remove'])
        feature_columns = load(required_files['feature_columns'])
        
        logger.info("All model components loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"Error loading model components: {str(e)}")
        return False

# Route for the root path to check if API is working
@app.route('/')
def index():
    """Root endpoint to verify API is working"""
    return jsonify({
        'status': 'API is running',
        'endpoints': {
            '/': 'This information',
            '/health': 'Health check endpoint',
            '/features': 'Get required features for prediction',
            '/classes': 'Get possible prediction classes',
            '/predict': 'Make a prediction (POST)'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    if not all([model, one_hot_encoder, scaler, label_encoder]):
        # Try to load model components if not loaded
        success = load_model_components()
        if not success:
            return jsonify({
                'status': 'unhealthy',
                'message': 'Model components not loaded',
                'model_loaded': False
            }), 503
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'message': 'API is ready to make predictions'
    })

@app.route('/features')
def features():
    """Return the feature names required for prediction"""
    # Ensure model components are loaded
    if not feature_columns:
        success = load_model_components()
        if not success:
            return jsonify({
                'error': 'Could not load model components'
            }), 500
    
    return jsonify({
        'features': feature_columns
    })

@app.route('/classes')
def classes():
    """Return the possible prediction classes"""
    # Ensure model components are loaded
    if not label_encoder:
        success = load_model_components()
        if not success:
            return jsonify({
                'error': 'Could not load model components'
            }), 500
    
    return jsonify({
        'classes': label_encoder.classes_.tolist()
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Make a prediction based on input data"""
    # Ensure model components are loaded
    if not all([model, one_hot_encoder, scaler, label_encoder]):
        success = load_model_components()
        if not success:
            return jsonify({
                'error': 'Model components not loaded'
            }), 500
    
    # Get input data
    try:
        data = request.json
        logger.info(f"Received data: {data}")
        
        if not data:
            return jsonify({
                'error': 'No input data provided'
            }), 400
        
        # Create DataFrame from input data
        input_df = pd.DataFrame([data])
        
        # Apply preprocessing
        # 1. Fill missing values
        for col, replacement in default_values.items():
            if col not in input_df.columns:
                input_df[col] = replacement
            else:
                input_df[col].fillna(replacement, inplace=True)
        
        # 2. Drop unnecessary columns
        input_df = input_df.drop(columns=[col for col in columns_to_remove if col in input_df.columns])
        
        # 3. Ensure all required columns are present
        for col in feature_columns:
            if col not in input_df.columns:
                input_df[col] = default_values.get(col, 'no')
        
        # 4. Reorder columns
        input_df = input_df[feature_columns]
        
        # 5. One-hot encoding
        input_encoded = one_hot_encoder.transform(input_df)
        
        # 6. Scaling
        input_scaled = scaler.transform(input_encoded)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        predicted_label = label_encoder.inverse_transform([prediction])[0]
        
        # Get probabilities
        probabilities = model.predict_proba(input_scaled)[0]
        class_names = label_encoder.classes_
        
        # Create probability dictionary
        prob_dict = {str(cn): float(p) for cn, p in zip(class_names, probabilities)}
        
        return jsonify({
            'prediction': str(predicted_label),
            'probabilities': prob_dict
        })
    
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        return jsonify({
            'error': f'Prediction error: {str(e)}'
        }), 500

# Load model components when the server starts
if __name__ == '__main__':
    # Try to load model components
    load_model_components()
    
    # Run the server
    logger.info("Cancer prediction model server starting on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True)