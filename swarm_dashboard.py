import streamlit as st
import pandas as pd
import joblib
import os

# --- 1. Load the Model Safely ---
# This ensures Streamlit looks for the model in the exact right folder
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'drone_model.pkl')

try:
    model = joblib.load(model_path)
    model_loaded = True
except FileNotFoundError:
    model_loaded = False

# --- 2. Build the Dashboard UI ---
st.title("🚁 Multi-Sensor Drone Swarm Detection")
st.markdown("Adjust the incoming sensor telemetry below to classify the airspace threat.")

# Create a clean layout with columns for the sliders
col1, col2 = st.columns(2)

with col1:
    alt = st.slider("Altitude (meters)", 10, 1000, 150)
    speed = st.slider("Speed (m/s)", 0, 100, 20)
    rcs = st.slider("Radar Cross-Section (m²)", 0.0, 10.0, 0.2)

with col2:
    acoustic = st.slider("Acoustic Signature (dB)", 0, 150, 45)
    thermal = st.slider("Thermal Signature (°C)", 20, 120, 50)
    rf = st.slider("RF Signal Strength", 0, 150, 30)

st.markdown("---")

# --- 3. The "Analyse Airspace" Logic ---
if st.button("Analyse Airspace", type="primary"):
    
    if not model_loaded:
        st.error("⚠️ Error: 'drone_model.pkl' not found. Please run your training script first.")
    else:
        # Package the slider inputs into a DataFrame matching our training data EXACTLY
        input_data = pd.DataFrame({
            'Altitude': [alt],
            'Speed': [speed],
            'Radar_Cross_Section': [rcs],
            'Acoustic_Signature': [acoustic],
            'Thermal_Signature': [thermal],
            'RF_Signal_Strength': [rf]
        })
        
        # Feed the data into the Random Forest model
        prediction = model.predict(input_data)[0]
        
        # --- 4. Display the Tactical Output ---
        st.subheader("📡 Tactical Assessment:")
        
        if prediction == "Drone Swarm":
            st.error("🚨 CRITICAL THREAT: DRONE SWARM DETECTED")
            st.write("Multiple distinct signatures converging. Initiate counter-swarm protocols immediately.")
        elif prediction == "Single Drone":
            st.warning("⚠️ ALERT: SINGLE DRONE DETECTED")
            st.write("Mechanical signatures match standard UAV profile. Track and monitor.")
        else:
            st.success("✅ CLEAR: BIRD / BIOLOGICAL CLUTTER")
            st.write("Signatures align with biological entities. No RF emission detected. Ignore.")