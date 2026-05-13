import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define the number of samples per class
n_samples_per_class = 1000
total_samples = n_samples_per_class * 3

# ==========================================
# 1. Generate Data for 'Bird'
# ==========================================
# Birds fly low, relatively slow, have tiny radar cross-sections, 
# low acoustic/thermal output, and zero RF emission.
birds = pd.DataFrame({
    'Altitude': np.random.uniform(10, 200, n_samples_per_class),          # Meters
    'Speed': np.random.uniform(5, 25, n_samples_per_class),               # m/s
    'Radar_Cross_Section': np.random.uniform(0.01, 0.05, n_samples_per_class), # m^2
    'Acoustic_Signature': np.random.uniform(10, 30, n_samples_per_class), # dB
    'Thermal_Signature': np.random.uniform(37, 42, n_samples_per_class),  # Rel. Heat (C)
    'RF_Signal_Strength': np.zeros(n_samples_per_class),                  # Zero RF signature
    'Target_Type': 'Bird'
})

# ==========================================
# 2. Generate Data for 'Single Drone'
# ==========================================
# Drones have higher operational altitudes, distinct RF communication signals,
# moderate heat from battery/motors, and distinct acoustic buzzing.
single_drones = pd.DataFrame({
    'Altitude': np.random.uniform(50, 1000, n_samples_per_class),
    'Speed': np.random.uniform(10, 50, n_samples_per_class),
    'Radar_Cross_Section': np.random.uniform(0.1, 0.5, n_samples_per_class),
    'Acoustic_Signature': np.random.uniform(40, 70, n_samples_per_class),
    'Thermal_Signature': np.random.uniform(45, 65, n_samples_per_class),
    'RF_Signal_Strength': np.random.uniform(20, 60, n_samples_per_class), # dBm/Relative signal
    'Target_Type': 'Single Drone'
})

# ==========================================
# 3. Generate Data for 'Drone Swarm'
# ==========================================
# Swarms share altitude and speed profiles with single drones but act as a massive
# multiplier for Radar, Acoustic, Thermal, and RF signatures due to density.
drone_swarms = pd.DataFrame({
    'Altitude': np.random.uniform(50, 1000, n_samples_per_class),
    'Speed': np.random.uniform(10, 45, n_samples_per_class),              # Swarms might fly slightly slower to maintain formation
    'Radar_Cross_Section': np.random.uniform(1.5, 6.0, n_samples_per_class),
    'Acoustic_Signature': np.random.uniform(75, 110, n_samples_per_class),
    'Thermal_Signature': np.random.uniform(70, 100, n_samples_per_class),
    'RF_Signal_Strength': np.random.uniform(70, 120, n_samples_per_class),
    'Target_Type': 'Drone Swarm'
})

# ==========================================
# 4. Combine, Shuffle, and Save
# ==========================================
# Combine all three dataframes
dataset = pd.concat([birds, single_drones, drone_swarms], ignore_index=True)

# Shuffle the dataset so the classes aren't in perfectly sequential blocks
dataset = dataset.sample(frac=1, random_state=42).reset_index(drop=True)

# Round the numerical columns to 2 decimal places for clean data
numerical_cols = ['Altitude', 'Speed', 'Radar_Cross_Section', 
                  'Acoustic_Signature', 'Thermal_Signature', 'RF_Signal_Strength']
dataset[numerical_cols] = dataset[numerical_cols].round(2)

# Save to local CSV file
csv_filename = 'sensor_data.csv'
dataset.to_csv(csv_filename, index=False)

print(f"Success! Synthetic dataset with {len(dataset)} rows generated and saved to '{csv_filename}'.")
print("\nClass Distribution:")
print(dataset['Target_Type'].value_counts())