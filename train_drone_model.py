import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# 1. Load the dataset
# Ensure the script looks in the same directory it is saved in
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'sensor_data.csv')

print("Loading sensor data...")
try:
    data = pd.read_csv(csv_path)
except FileNotFoundError:
    print(f"Error: Could not find 'sensor_data.csv' at {csv_path}.")
    print("Please ensure your data generation script has been run in this folder.")
    exit()

# 2. Separate features (X) and target labels (y)
X = data.drop(columns=['Target_Type'])
y = data['Target_Type']

# 3. Split the data into Training (80%) and Testing (20%) sets
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. Initialize and train the Random Forest Classifier (The Sensor Fusion Engine)
print("Training the Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate the model's performance on the unseen test data
print("\n--- Model Evaluation ---")
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Overall Accuracy: {accuracy * 100:.2f}%\n")

print("Detailed Classification Report:")
print(classification_report(y_test, y_pred))

# 6. Save the trained model for offline deployment
model_filename = os.path.join(script_dir, 'drone_model.pkl')
joblib.dump(model, model_filename)

print(f"\nSuccess! Model trained and saved as '{model_filename}'.")
print("You can now load this .pkl file in your deployment script for real-time predictions.")