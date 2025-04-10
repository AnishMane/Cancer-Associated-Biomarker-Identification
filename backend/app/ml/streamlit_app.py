import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json

# Set page configuration
st.set_page_config(
    page_title="Cancer Gene Role Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define API endpoints
API_BASE = "http://localhost:5000"
PREDICT_ENDPOINT = f"{API_BASE}/predict"
HEALTH_ENDPOINT = f"{API_BASE}/health"
FEATURES_ENDPOINT = f"{API_BASE}/features"
CLASSES_ENDPOINT = f"{API_BASE}/classes"

# Add title and description
st.title("Cancer Gene Role Predictor")
st.markdown("""
This application predicts the role of genes in cancer based on the features of the gene.
Enter the information below to get a prediction from the machine learning model.
""")

# Check API connection
api_status = "Unknown"
try:
    health_response = requests.get(HEALTH_ENDPOINT)
    if health_response.status_code == 200:
        api_status = "Connected"
    else:
        api_status = f"Error: {health_response.status_code}"
except Exception as e:
    api_status = f"Connection Error: {str(e)}"

st.sidebar.markdown("## API Status")
if api_status == "Connected":
    st.sidebar.success("API Server: Connected")
else:
    st.sidebar.error(f"API Server: {api_status}")

# Get feature information
features = []
try:
    features_response = requests.get(FEATURES_ENDPOINT)
    if features_response.status_code == 200:
        features = features_response.json().get('features', [])
    else:
        st.warning(f"Could not retrieve feature information: {features_response.status_code}")
except Exception as e:
    st.warning(f"Error retrieving features: {str(e)}")

# Get class information
classes = []
try:
    classes_response = requests.get(CLASSES_ENDPOINT)
    if classes_response.status_code == 200:
        classes = classes_response.json().get('classes', [])
    else:
        st.warning(f"Could not retrieve class information: {classes_response.status_code}")
except Exception as e:
    st.warning(f"Error retrieving classes: {str(e)}")

# Display class information in sidebar
if classes:
    st.sidebar.markdown("## Possible Predictions")
    for c in classes:
        st.sidebar.markdown(f"- {c}")

# Define categorical variables and their possible values
categorical_mappings = {
    "Germline": ["yes", "no", "unknown"],
    "Somatic": ["yes", "no", "unknown"],
    "Hallmark": ["yes", "no", "unknown"],
    "Other Germline Mut": ["yes", "no", "unknown"],
    "Molecular Genetics": ["Dominant", "Recessive", "X-linked", "Unknown"],
    "Mutation Type": ["D", "F", "Mis", "N", "A", "O", "S"],  # Removed duplicate "F"
    "mutation type": ["D", "F", "Mis", "N", "A", "O", "S"],  # Adding lowercase version
    "MUTATION TYPE": ["D", "F", "Mis", "N", "A", "O", "S"],  # Adding uppercase version
    "mutation_type": ["D", "F", "Mis", "N", "A", "O", "S"],  # Adding with underscore
    "Tissue Type": ["Epithelial", "Lymphatic", "Mesenchymal", "Hematopoietic", "Other"],
}

# Define numeric variables with reasonable ranges
numeric_ranges = {
    "Tier": (1, 2, 1),  # (min, max, default)
    "CDS length": (0, 10000, 1000),
    "Strand": (-1, 1, 1),
    "MIM Number": (100000, 999999, 100000),
}

# Create input form
with st.form("prediction_form"):
    st.markdown("### Enter Gene Information")
   
    # Create a dictionary to store feature inputs
    input_data = {}
    
    # Display actual feature names for debugging
    with st.expander("Debug - Available Features"):
        st.write(features)
   
    # Create columns for better layout
    num_columns = 2
    cols = st.columns(num_columns)
   
    # Process each feature
    for i, feature in enumerate(features):
        col_idx = i % num_columns
        with cols[col_idx]:
            # Special handling for mutation type - check with various formats
            if feature.lower() == "mutation type" or "mutation" in feature.lower() and "type" in feature.lower():
                input_data[feature] = st.selectbox(
                    f"{feature}",
                    options=["D", "F", "Mis", "N", "A", "O", "S"],
                    index=0,
                    key=f"feature_{feature}"
                )
            # Direct lookup in categorical_mappings 
            elif feature in categorical_mappings:
                options = categorical_mappings[feature]
                default_index = 1 if "no" in options else 0
                input_data[feature] = st.selectbox(
                    f"{feature}",
                    options=options,
                    index=default_index,
                    key=f"feature_{feature}"
                )
            # Check if it's a numerical feature
            elif feature in numeric_ranges:
                min_val, max_val, default_val = numeric_ranges[feature]
                input_data[feature] = st.number_input(
                    f"{feature}",
                    min_value=min_val,
                    max_value=max_val,
                    value=default_val,
                    key=f"feature_{feature}"
                )
            # Generic detection for other categorical features
            elif any(keyword in feature.lower() for keyword in ["type", "status", "role", "category"]):
                input_data[feature] = st.selectbox(
                    f"{feature}",
                    options=["yes", "no", "unknown"],
                    index=1,
                    key=f"feature_{feature}"
                )
            # Generic detection for other numerical features
            elif any(keyword in feature.lower() for keyword in ["count", "number", "score", "id", "length", "position"]):
                input_data[feature] = st.number_input(
                    f"{feature}",
                    min_value=0,
                    max_value=1000000,
                    value=0,
                    key=f"feature_{feature}"
                )
            # Default to text input for everything else
            else:
                input_data[feature] = st.text_input(
                    f"{feature}",
                    value="",
                    key=f"feature_{feature}"
                )

    # Special handling for Tier if needed
    if "Tier" in features and "Tier" not in input_data:
        input_data["Tier"] = st.slider(
            "Tier",
            min_value=0,
            max_value=10,
            value=0,
            step=1,
            key="feature_Tier"
        )
   
    # Add preset configurations
    st.markdown("### Preset Configurations")
    preset = st.selectbox(
        "Select a preset configuration",
        options=["Custom (Use inputs above)", "Typical TSG", "Typical Oncogene", "Fusion Gene", "Tumor Mutation Load"],
        index=0
    )
   
    # Apply preset values if selected
    if preset == "Typical TSG":
        input_data.update({
            "Name":"",
            "Genome Location":"",
            "Tier":1,
            "Hallmark":"no",
            "Chr Band":"",
            "Somatic":"no",
            "Germline":"no",
            "Tissue Type":"Mesenchymal",
            "Molecular Genetics":"Dominant",
            "Mutation Types":"F",
            "Other Germline Mut":"yes",
            "Synonyms":"",
        })
    elif preset == "Fusion Gene":
        input_data.update({
            "Germline": "no",
            "Somatic": "yes",
            "Hallmark": "yes",
            "Tier": 1,
            "Other Germline Mut": "no"
        })
    elif preset == "Typical Oncogene":
        input_data.update({
            "Name":"",
            "Genome Location":"",
            "Tier":1,
            "Hallmark":"no",
            "Chr Band":"",
            "Somatic":"no",
            "Germline":"no",
            "Tissue Type":"Mesenchymal",
            "Molecular Genetics":"Recessive",
            "Mutation Types":"A",
            "Other Germline Mut":"yes",
            "Synonyms":""})
    elif preset == "Tumor Mutation Load":
        input_data.update({
            "Germline": "no",
            "Somatic": "yes",
            "Hallmark": "no",
            "Tier": 1,
            "Other Germline Mut": "yes"
        })
   
    # Submit button
    submit_button = st.form_submit_button("Predict Role in Cancer")

# Make prediction when form is submitted
if submit_button:
    st.markdown("### Input Data")
    input_df = pd.DataFrame([input_data])
    st.dataframe(input_df)
   
    # Debug information
    with st.expander("Debug Information"):
        st.markdown("#### Input JSON")
        st.json(input_data)
   
    try:
        # Make prediction request
        response = requests.post(
            PREDICT_ENDPOINT,
            json=input_data,
            headers={"Content-Type": "application/json"}
        )
       
        if response.status_code == 200:
            result = response.json()
           
            # Display prediction result
            st.markdown("## Prediction Results")
           
            # Main prediction with styled box
            prediction = result['prediction']
            st.markdown(f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px;">
                <h3>Predicted Role in Cancer:</h3>
                <h2 style="color:#1f77b4;">{prediction}</h2>
            </div>
            """, unsafe_allow_html=True)
           
            # Display probabilities
            if 'probabilities' in result:
                st.markdown("### Prediction Probabilities")
               
                # Sort probabilities by value for better visualization
                probs = result['probabilities']
                sorted_probs = {k: v for k, v in sorted(probs.items(), key=lambda item: item[1], reverse=True)}
               
                # Create bar chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(sorted_probs.keys()),
                        y=list(sorted_probs.values()),
                        marker_color='#1f77b4',
                        text=[f"{prob:.2%}" for prob in sorted_probs.values()],
                        textposition='auto'
                    )
                ])
               
                fig.update_layout(
                    title="Probability Distribution",
                    xaxis_title="Role in Cancer",
                    yaxis_title="Probability",
                    yaxis=dict(tickformat=".0%"),
                    height=500
                )
               
                st.plotly_chart(fig, use_container_width=True)
               
                # Show raw response in expander
                with st.expander("View Raw API Response"):
                    st.json(result)
            else:
                st.warning("No probability information available in the prediction result.")
        else:
            st.error(f"Error from API: {response.status_code}")
            st.code(response.text)
           
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")

# Add information about the model
st.markdown("---")
st.markdown("""
### About This Prediction Model
This model was trained using XGBoost with the following parameters:
- colsample_bytree: 0.8
- learning_rate: 0.01
- max_depth: 7
- n_estimators: 600
- subsample: 0.8
The model was trained on cancer gene data to predict the role of genes in cancer development.
### Model Output Classes:
- TSG (Tumor Suppressor Gene)
- Oncogene
- Fusion
- Other
If the model is consistently predicting only "TSG", this could indicate:
1. Class imbalance in the training data
2. Feature encoding issues
3. Model overfitting to the majority class
""")