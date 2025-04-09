# model_training.py
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from joblib import dump

# Load data
csv_path = r"D:\repos\Cancer-Associated-Biomarker-Identification\backend\app\ml\data\cancer_data.csv"
data = pd.read_csv(csv_path)

# Copy data
X = data.copy()

# Restore dropped columns and handle missing values
columns_to_restore = {
    'Germline': 'no',
    'Hallmark': 'no',
    'Other Germline Mut': 'no',
    'Tier': 0,
    'Somatic': 'no'
}
for col, replacement in columns_to_restore.items():
    if col not in X.columns:  # Add column if missing
        X[col] = replacement
    else:  # Replace missing values
        X.fillna({col:replacement}, inplace=True)

# Remove specific columns from X
columns_to_remove = [
    'Cancer Syndrome',
    'Other Syndrome',
    'Translocation Partner',
    'Tumour Types(Germline)',
    'Gene Symbol',
    'Entrez GeneId',
    'Tumour Types(Somatic)',
]
X.drop(columns=[col for col in columns_to_remove if col in X.columns], inplace=True)

# Drop rows without the target variable
X.dropna(subset=['Role in Cancer'], inplace=True)

# Separate target variable
y = X.pop("Role in Cancer")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Save a copy of the X_train columns for later use
X_columns = list(X_train.columns)
dump(X_columns, 'feature_columns.joblib')

# Encode categorical variables
one_hot = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_train = one_hot.fit_transform(X_train)
X_test = one_hot.transform(X_test)

# Normalize numerical variables
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Handle class imbalance
smote = SMOTE()
X_train, y_train = smote.fit_resample(X_train, y_train)

# Encode target labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Train the model
end_model = XGBClassifier(
    colsample_bytree=0.8,
    learning_rate=0.01,
    max_depth=7,
    n_estimators=600,
    subsample=0.8, 
    random_state=42
)
end_model.fit(X_train, y_train_encoded)

# Evaluate the model
end_pred = end_model.predict(X_test)
print("Final Accuracy:", accuracy_score(y_test_encoded, end_pred))

# Save the model and preprocessing components
end_model.save_model('cancer_model.json')
dump(one_hot, 'one_hot_encoder.joblib')
dump(scaler, 'scaler.joblib')
dump(label_encoder, 'label_encoder.joblib')
dump(columns_to_restore, 'default_values.joblib')
dump(columns_to_remove, 'columns_to_remove.joblib')