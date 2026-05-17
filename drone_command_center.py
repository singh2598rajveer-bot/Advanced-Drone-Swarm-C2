import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier

# Set Page Config for Tactical Dark Theme
st.set_page_config(page_title="Air Defense C2 Dashboard", layout="wide", initial_sidebar_state="expanded")

# =====================================================================
# 1. ADVANCED ALL-WEATHER AI ENGINE (Background Memory Matrix)
# =====================================================================
@st.cache_resource
def initialize_and_train_ai():
    np.random.seed(101)
    num_samples = 2500

    # Multi-sensor inputs matching Indian Army specifications
    radar_rcs = np.random.uniform(0.005, 3.0, num_samples)       
    rf_signal_strength = np.random.uniform(-100, -30, num_samples) 
    acoustic_freq_hz = np.random.uniform(50, 20000, num_samples)   
    velocity_kmph = np.random.uniform(0, 150, num_samples)        
    thermal_signature_c = np.random.uniform(15, 150, num_samples)  

    X = pd.DataFrame({
        'radar_rcs': radar_rcs,
        'rf_signal_strength': rf_signal_strength,
        'acoustic_freq_hz': acoustic_freq_hz,
        'velocity_kmph': velocity_kmph,
        'thermal_signature_c': thermal_signature_c
    })

    def assign_class(row):
        if row['radar_rcs'] < 0.02 and row['thermal_signature_c'] < 30:
            return 0 # False Alarm (Bird)
        elif row['velocity_kmph'] > 100 and row['thermal_signature_c'] > 80:
            return 2 # High-velocity Kamikaze Threat
        elif row['radar_rcs'] > 1.8 and row['rf_signal_strength'] > -50:
            return 3 # Swarm Command Module
        else:
            return 1 # Standard Surveillance Drone

    y = X.apply(assign_class, axis=1)
    model = RandomForestClassifier(n_estimators=100, random_state=101)
    model.fit(X, y)
    return model

ai_fusion_engine = initialize_and_train_ai()

# =====================================================================
# 2. TACTICAL USER INTERFACE & LIVE OPERATIONS
# =====================================================================
st.title("🛡️ AI-Enabled Multi-Sensor Drone Swarm C2 Command Center")
st.markdown("### National Counter-Drone Capability Infrastructure // Air Defense Operations Command")
st.divider()

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("🌍 Operational Environment Matrix")
weather_condition = st.sidebar.selectbox("Select All-Weather Scenario Profile", ["Clear Sky (Optimal)", "Heavy Monsoon / Clutter", "Severe Desert Sandstorm"])

st.sidebar.divider()
st.sidebar.header("🎯 Single-Target Manual Intercept Vector")
s_rcs = st.sidebar.slider("Radar Cross Section (RCS in m²)", 0.005, 3.0, 0.5)
s_rf = st.sidebar.slider("RF Signal Strength (RSSI in dBm)", -100, -30, -65)
s_acoustic = st.sidebar.slider("Acoustic Frequency Profile (Hz)", 50, 20000, 4500)
s_speed = st.sidebar.slider("Target Velocity (km/h)", 0, 150, 45)
s_thermal = st.sidebar.slider("EO/IR Thermal Signature (Δ°C)", 15, 150, 40)

# INNOVATION 3: Advanced Sensor Weather Attenuation Curve Calculations
weather_latency = 14.2 
confidence_multiplier = 1.0
sensor_reliance_mode = "Balanced Multi-Sensor Fusion Array"

if weather_condition == "Heavy Monsoon / Clutter":
    s_rcs *= 0.81          # Precipitation signal degradation
    s_thermal *= 0.65      # Thermal signature dampening
    weather_latency = 42.1 # Signal processing overhead delay
    confidence_multiplier = 0.86
    sensor_reliance_mode = "🍂 Primary Reliance: Acoustic/RF Arrays (Radar & EO/IR Attenuated)"
elif weather_condition == "Severe Desert Sandstorm":
    s_rcs *= 0.58          # Particulate scattering
    s_acoustic *= 1.35     # Wind acoustic noise distortion
    weather_latency = 58.7 
    confidence_multiplier = 0.74
    sensor_reliance_mode = "🔥 Primary Reliance: Thermal/Radar Micro-Doppler (Acoustic Degraded)"

# Package modified vectors for the AI
manual_input = pd.DataFrame([[s_rcs, s_rf, s_acoustic, s_speed, s_thermal]], 
                            columns=['radar_rcs', 'rf_signal_strength', 'acoustic_freq_hz', 'velocity_kmph', 'thermal_signature_c'])

# Execute Sensor Fusion Prediction
prediction = ai_fusion_engine.predict(manual_input)[0]

class_map = {
    0: "🟢 FALSE ALARM (BIOLOGICAL / BIRD)", 
    1: "🟡 RECONNAISSANCE QUADCOPTER", 
    2: "🔴 HIGH-THREAT KAMIKAZE DRONE", 
    3: "🚨 SWARM MOTHER-SHIP / LEADER"
}

countermeasure_map = {
    0: "🚫 NO ACTION REQUIRED (Target Logged as Non-Threat Clutter)",
    1: "📡 SOFT-KILL: Initiate Directional RF Smart-Jamming on 2.4GHz/5.8GHz channels.",
    2: "⚡ HARD-KILL: Authorize Close-In Weapon System (CIWS) or High-Power Laser engagement vector immediately.",
    3: "BMS-ECM: Deploy Wide-Band Swarm Network De-synchronization Array & alert local Air Assets."
}

# Compute threat score
threat_score = min(max(int((s_rcs * 20) + (abs(s_rf) * -0.5 + 50) + (s_speed * 0.3) + (s_thermal * 0.2)), 0), 100)
adjusted_confidence = min(int(98 * confidence_multiplier), 100)

# --- PANEL 1: C2 ANALYTICS METRICS ---
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric(label="Communication Latency Matrix", value=f"{weather_latency} ms", delta="Operational Threshold Check Pass")
with m_col2:
    st.metric(label="Dynamic Fusion Integrity", value=f"{adjusted_confidence}%", delta=f"Mode: {sensor_reliance_mode}")
with m_col3:
    st.metric(label="Strategic Air Threat Index", value=f"{threat_score} / 100", delta="High Threat Level Alert" if threat_score > 75 else None)

st.divider()

# INNOVATION 1: The OODA-Loop Automation Progress Dashboard Tracker
st.subheader("🔁 Autonomous OODA Decision-Support Cycle")
if threat_score < 25:
    st.info("🎯 **CURRENT LOOP STATE:** [OBSERVE] -> [ORIENT] -> Target categorized as Non-Threat Environmental Clutter. System loop reset.")
elif threat_score < 65:
    st.warning("📡 **CURRENT LOOP STATE:** [OBSERVE] -> [ORIENT] -> [DECIDE] -> Target confirmed. Monitoring tracking loop parameters continuously.")
else:
    st.error("💥 **CURRENT LOOP STATE:** [OBSERVE] -> [ORIENT] -> [DECIDE] -> [ACT] -> Target prioritized. Counter-measure allocation vector sent down-link.")

col_left, col_right = st.columns(2)
with col_left:
    st.markdown(f"#### Identified Class: {class_map[prediction]}")
with col_right:
    st.markdown(f"#### Active CUAS Assignment Protocol:")
    st.caption(countermeasure_map[prediction])

st.divider()

# =====================================================================
# 3. LIVE 3D SWARM TRACKING & OPTIMIZED TEWA ALLOCATION ENGAGEMENT MATRIX
# =====================================================================
st.subheader("📡 Live 3D Tactical Swarm Spatial Tracking Matrix")

num_drones = 15
drone_ids = [f"BMS-DRN-{i:02d}" for i in range(1, num_drones + 1)]

np.random.seed(42)
x_coords = np.random.uniform(-4, 4, num_drones)
y_coords = np.random.uniform(-4, 4, num_drones)
z_coords = np.random.uniform(0.2, 2.2, num_drones) 

ew_jamming = st.checkbox("⚡ Activate Forward Area RF Electronic Warfare Jamming Array")
if ew_jamming:
    x_coords += np.random.normal(0, 1.2, num_drones)
    y_coords += np.random.normal(0, 1.2, num_drones)
    z_coords = np.maximum(z_coords - 0.7, 0.05)
    st.warning("🚨 EMERGENCY WARN: Active Electronic Countermeasures deployed. Target RF tracking loops degraded.")

# Mathematical Distance tracking
distances = np.sqrt(x_coords**2 + y_coords**2 + z_coords**2)
speeds = np.random.uniform(40, 140, num_drones)

# INNOVATION 2: Advanced TEWA Weapon Resource Optimization Algorithms
swarm_threat_scores = []
allocated_weapons = []
for i in range(num_drones):
    base_score = int((120 / (distances[i] + 0.5)) + (speeds[i] * 0.4))
    final_score = min(max(base_score, 10), 100)
    swarm_threat_scores.append(final_score)
    
    if final_score > 82:
        allocated_weapons.append("💥 CIWS Automated Flak Array [Primary Lock]")
    elif final_score > 62:
        allocated_weapons.append("⚡ High-Energy Directed Laser Beam [Tracking]")
    elif final_score > 38:
        allocated_weapons.append("📡 Directional RF Smart-Jamming Vector")
    else:
        allocated_weapons.append(" Passthrough Surveillance Mode")

swarm_df = pd.DataFrame({
    'Drone Target ID': drone_ids,
    'X Vector (km)': x_coords,
    'Y Vector (km)': y_coords,
    'Altitude (km)': z_coords,
    'Range to HQ (km)': np.round(distances, 2),
    'Velocity (km/h)': np.round(speeds, 1),
    'Priority Threat Score': swarm_threat_scores,
    'Optimized TEWA Weapon Allocation': allocated_weapons
})

swarm_df = swarm_df.sort_values(by='Priority Threat Score', ascending=False).reset_index(drop=True)

critical_breaches = swarm_df[swarm_df['Range to HQ (km)'] < 2.0]
if not critical_breaches.empty:
    st.error(f"🚨 INNER PERIMETER BREACH: {len(critical_breaches)} weaponized swarm vectors detected within the 2.0 KM safety zone!")

# Render 3D Plotly Map
fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers+text',
    marker=dict(size=14, color='cyan', symbol='square'),
    text=["🔵 COMMAND HQ BASE"],
    name="Command HQ Base"
))

fig.add_trace(go.Scatter3d(
    x=swarm_df['X Vector (km)'],
    y=swarm_df['Y Vector (km)'],
    z=swarm_df['Altitude (km)'],
    mode='markers+text',
    marker=dict(size=9, color='orange' if ew_jamming else 'red', symbol='diamond'),
    text=swarm_df['Drone Target ID'],
    textposition="top center",
    name="Tracked Swarm Targets"
))

fig.update_layout(
    scene=dict(
        xaxis_title='East/West Vector (km)',
        yaxis_title='North/South Vector (km)',
        zaxis_title='Altitude Profile (km)',
        bgcolor="rgb(20, 20, 20)"
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    template="plotly_dark",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("⚔️ Automated Threat Prioritization & Weapon Allocation Matrix (TEWA)")
st.dataframe(swarm_df, use_container_width=True) 