import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import re
from urllib.parse import unquote_plus
import time

# Set page configuration
st.set_page_config(
    page_title="Cancer Gene Role Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define API endpoints
API_BASE = "http://localhost:5001"
PREDICT_ENDPOINT = f"{API_BASE}/predict"
HEALTH_ENDPOINT = f"{API_BASE}/health"
FEATURES_ENDPOINT = f"{API_BASE}/features"
CLASSES_ENDPOINT = f"{API_BASE}/classes"

# Function to fix malformed JSON
def fix_json_format(malformed_json):
    """Fix common JSON formatting issues"""
    # Add missing commas between key-value pairs
    fixed_json = re.sub(r'"\n"', '":"', malformed_json)
    
    # Ensure property names are quoted
    fixed_json = re.sub(r'(\n)([^"{\[\s][^:]*?):', r'\1"\2":', fixed_json)
    
    # Add commas between properties
    fixed_json = re.sub(r'"\n', '",\n"', fixed_json)
    
    # Fix array elements
    fixed_json = re.sub(r'\}\n(\d+):', r'},\n\1:', fixed_json)
    
    return fixed_json

# Add title and description
st.title("Cancer Gene Role Predictor")
st.markdown("""
This application predicts the role of genes in cancer based on the features of the gene.
Enter the information below to get a prediction from the machine learning model.
""")

# Get query parameters from URL
query_params = st.query_params

# Check if 'data' exists in query params
if "data" in query_params:
    try:
        # Get the data from query params and decode it properly
        encoded_data = query_params["data"]
        decoded_data = unquote_plus(encoded_data)
        
        # Debug output to see what's being parsed
        with st.expander("Raw decoded data"):
            st.text(decoded_data[:1000] + "..." if len(decoded_data) > 1000 else decoded_data)
        
        # Try to fix and parse JSON
        try:
            # Try direct parsing first
            parsed_data = json.loads(decoded_data)
            st.success("Data received and parsed successfully!")
        except json.JSONDecodeError:
            st.warning("JSON parsing error - attempting to fix formatting...")
            try:
                # Try to fix the JSON format
                fixed_json = fix_json_format(decoded_data)
                # Further cleanup for array data
                if '[' in fixed_json and ']' in fixed_json:
                    fixed_json = re.sub(r'(\d+):{', r'{\n"id": \1,', fixed_json)
                parsed_data = json.loads(fixed_json)
                st.success("Data fixed and parsed successfully!")
            except Exception as e:
                st.error(f"Failed to fix JSON: {str(e)}")
                st.code(fixed_json[:500], language="json")
                parsed_data = None
        
        if parsed_data:
            st.write("### Parsed Data")
            if isinstance(parsed_data, list):
                st.write(f"Found {len(parsed_data)} gene records")
                st.dataframe(parsed_data)
            else:
                st.write(parsed_data)
    except Exception as e:
        st.error(f"Failed to parse data: {e}")
else:
    st.info("No data found in URL query parameters.")

# Check API connection with retries
api_status = "Unknown"
max_retries = 3
retry_count = 0

with st.sidebar:
    st.markdown("## API Connection Status")
    status_placeholder = st.empty()
    
    while retry_count < max_retries and api_status != "Connected":
        try:
            status_placeholder.info(f"Attempting to connect to API ({retry_count+1}/{max_retries})...")
            health_response = requests.get(HEALTH_ENDPOINT, timeout=5)
            
            if health_response.status_code == 200:
                api_status = "Connected"
                status_placeholder.success("✅ API Server: Connected")
                break
            else:
                api_status = f"Error: {health_response.status_code}"
                status_placeholder.error(f"❌ API Server returned: {api_status}")
        except requests.exceptions.ConnectionError:
            api_status = "Connection Refused"
            status_placeholder.error(f"❌ API Server: Connection refused. Is the server running?")
        except Exception as e:
            api_status = f"Error: {str(e)}"
            status_placeholder.error(f"❌ API Server: {api_status}")
        
        retry_count += 1
        if retry_count < max_retries and api_status != "Connected":
            # Wait before retrying
            time.sleep(2)
    
    if api_status != "Connected":
        st.sidebar.error("""
        Failed to connect to the API server. Please ensure:
        1. Flask server is running (python inference.py)
        2. It's running on port 5000
        3. No firewall is blocking the connection
        """)
        
        # Show command to start the API server
        st.sidebar.markdown("### How to start the API server")
        st.sidebar.code("python inference.py")
        
        # Add troubleshooting tips
        st.sidebar.markdown("### Troubleshooting")
        st.sidebar.markdown("""
        - Check if another process is using port 5000
        - Try restarting both servers
        - Verify the file paths in inference.py
        - Check console for Python errors
        """)

# Get features and classes if API is connected
features = []
classes = []

if api_status == "Connected":
    # Get feature information
    try:
        with st.spinner("Loading feature information..."):
            features_response = requests.get(FEATURES_ENDPOINT, timeout=5)
            if features_response.status_code == 200:
                features = features_response.json().get('features', [])
                st.sidebar.success(f"✅ Loaded {len(features)} features")
            else:
                st.warning(f"Could not retrieve feature information: Status {features_response.status_code}")
    except Exception as e:
        st.warning(f"Error retrieving features: {str(e)}")

    # Get class information
    try:
        with st.spinner("Loading class information..."):
            classes_response = requests.get(CLASSES_ENDPOINT, timeout=5)
            if classes_response.status_code == 200:
                classes = classes_response.json().get('classes', [])
                st.sidebar.success(f"✅ Loaded {len(classes)} prediction classes")
            else:
                st.warning(f"Could not retrieve class information: Status {classes_response.status_code}")
    except Exception as e:
        st.warning(f"Error retrieving classes: {str(e)}")

    # Display class information in sidebar
    if classes:
        st.sidebar.markdown("## Possible Predictions")
        for c in classes:
            st.sidebar.markdown(f"- {c}")
    else:
        st.sidebar.warning("Could not retrieve prediction classes from API")
else:
    st.warning("⚠️ Cannot load feature and class information - API server unavailable")

# Add default features if API connection fails
if not features:
    st.warning("⚠️ Using default feature set as API didn't return features list")
    features = ["Name", "Genome Location", "Tier", "Hallmark", "Chr Band", "Somatic", 
                "Germline", "Tissue Type", "Molecular Genetics", "Mutation Types", 
                "Other Germline Mut", "Synonyms"]

# Define categorical variables and their possible values
categorical_mappings = {
    "Germline": ["yes", "no", "unknown"],
    "Somatic": ["yes", "no", "unknown"],
    "Hallmark": ["yes", "no", "unknown"],
    "Other Germline Mut": ["yes", "no", "unknown"],
    "Molecular Genetics": ["Dominant", "Recessive", "X-linked", "Unknown", "Dom/Rec", "Rec/X"],
    "Mutation Type": ["D", "F", "Mis", "N", "A", "O", "S", "T", "Promoter Mis", "Mis. N, F"],
    "mutation type": ["D", "F", "Mis", "N", "A", "O", "S", "T", "Promoter Mis", "Mis. N, F"],
    "MUTATION TYPE": ["D", "F", "Mis", "N", "A", "O", "S", "T", "Promoter Mis", "Mis. N, F"],
    "mutation_type": ["D", "F", "Mis", "N", "A", "O", "S", "T", "Promoter Mis", "Mis. N, F"],
    "Mutation Types": ["D", "F", "Mis", "N", "A", "O", "S", "T", "Promoter Mis", "Mis. N, F"],
    "Tissue Type": ["Epithelial", "Lymphatic", "Mesenchymal", "Hematopoietic", "Other", "E", "L", "M", "H", "O", "O, M", "L, E", "O, L"],
}

# Define numeric variables with reasonable ranges
numeric_ranges = {
    "Tier": (1, 2, 1),  # (min, max, default)
    "CDS length": (0, 10000, 1000),
    "Strand": (-1, 1, 1),
    "MIM Number": (100000, 999999, 100000),
}

# Check if we have data from query parameters to process in batch
batch_data = None
if "data" in query_params and "parsed_data" in locals() and parsed_data:
    batch_data = parsed_data

# Batch processing section
if batch_data and isinstance(batch_data, list) and len(batch_data) > 0:
    st.markdown("## Batch Prediction")
    st.write(f"Processing {len(batch_data)} genes from URL data")
    
    # Add a button to start batch processing
    if st.button("Start Batch Prediction"):
        if api_status != "Connected":
            st.error("⚠️ Cannot make predictions - API server is not connected. Start the Flask server first.")
        else:
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, gene_data in enumerate(batch_data):
                status_text.text(f"Processing gene {i+1} of {len(batch_data)}...")
                
                try:
                    # Make prediction request
                    response = requests.post(
                        PREDICT_ENDPOINT,
                        json=gene_data,
                        headers={"Content-Type": "application/json"},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        results.append({
                            "gene_id": i,
                            "input": gene_data,
                            "prediction": result.get("prediction"),
                            "probabilities": result.get("probabilities", {})
                        })
                    else:
                        st.warning(f"Error from API for gene {i}: {response.status_code}")
                        results.append({
                            "gene_id": i,
                            "input": gene_data,
                            "error": f"API returned status {response.status_code}"
                        })
                except Exception as e:
                    st.warning(f"Error processing gene {i}: {str(e)}")
                    results.append({
                        "gene_id": i,
                        "input": gene_data,
                        "error": str(e)
                    })
                
                # Update progress
                progress_bar.progress((i + 1) / len(batch_data))
            
            status_text.text("Batch processing complete!")
            
            # Display results
            if results:
                st.markdown("### Prediction Results")
                
                # Create a dataframe for display
                result_data = []
                for r in results:
                    if "error" not in r:
                        result_data.append({
                            "Gene ID": r["gene_id"],
                            "Name": r["input"].get("Name", ""),
                            "Chr Band": r["input"].get("Chr Band", ""),
                            "Prediction": r["prediction"],
                            "Top Probability": max(r["probabilities"].values()) if r["probabilities"] else 0
                        })
                
                if result_data:
                    st.dataframe(result_data)
                    
                    # Create visualization of predictions
                    prediction_counts = {}
                    for r in result_data:
                        pred = r["Prediction"]
                        prediction_counts[pred] = prediction_counts.get(pred, 0) + 1
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=list(prediction_counts.keys()),
                            y=list(prediction_counts.values()),
                            marker_color='#1f77b4',
                        )
                    ])
                    
                    fig.update_layout(
                        title="Prediction Distribution",
                        xaxis_title="Predicted Role",
                        yaxis_title="Count",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("No prediction results available.")
            else:
                st.error("No prediction results available.")

# Create input form for single prediction
st.markdown("## Single Gene Prediction")
with st.form("prediction_form"):
    st.markdown("### Enter Gene Information")
   
    # Create a dictionary to store feature inputs
    input_data = {}
   
    # Create columns for better layout
    num_columns = 2
    cols = st.columns(num_columns)
   
    # Process each feature
    for i, feature in enumerate(features):
        col_idx = i % num_columns
        with cols[col_idx]:
            # Special handling for mutation type - check with various formats
            if feature.lower() == "mutation type" or feature.lower() == "mutation types" or ("mutation" in feature.lower() and "type" in feature.lower()):
                input_data[feature] = st.selectbox(
                    f"{feature}",
                    options=categorical_mappings.get("Mutation Types", ["D", "F", "Mis", "N", "A", "O", "S"]),
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
    if api_status != "Connected":
        st.error("⚠️ Cannot make prediction - API server is not connected. Start the Flask server first.")
    else:
        st.markdown("### Input Data")
        input_df = pd.DataFrame([input_data])
        st.dataframe(input_df)
       
        # Debug information
        with st.expander("Debug Information"):
            st.markdown("#### Input JSON")
            st.json(input_data)
       
        try:
            # Make prediction request
            with st.spinner("Making prediction..."):
                response = requests.post(
                    PREDICT_ENDPOINT,
                    json=input_data,
                    headers={"Content-Type": "application/json"},
                    timeout=10
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
                
                # Provide troubleshooting advice
                st.error("""
                Troubleshooting steps:
                1. Check that the Flask server is running
                2. Verify your feature names match what the API expects
                3. Try restarting both servers
                """)
               
        except requests.exceptions.ConnectionError:
            st.error("Connection to API server failed. Is the server running?")
        except requests.exceptions.Timeout:
            st.error("API request timed out. The server might be overloaded.")
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