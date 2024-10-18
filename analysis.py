import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Data from the image in structured format
data1 = {
    'name': ['TO KALOKAIRI AUTO', 'Me Zilevoun', 'TO YPOGEIO (STIN YPOGA)', 'AURIO', 'OLA',
             'KENODOKSIA / VOULIMIA', 'KOBORRIMON KAI APLISTOS', 'APOPSE VRADI', '10\'', 'LAGNEIA'],
    'danceability': [0.759, 0.734, 0.836, 0.762, 0.592, 0.612, 0.546, 0.679, 0.807, 0.813],
    'energy': [0.835, 0.672, 0.492, 0.546, 0.68, 0.526, 0.505, 0.595, 0.799, 0.622],
    'speechiness': [0.263, 0.172, 0.247, 0.401, 0.0868, 0.423, 0.373, 0.0868, 0.0824, 0.3],
    'acousticness': [0.649, 0.469, 0.116, 0.055, 0.149, 0.0443, 0.101, 0.174, 0.0593, 0.15],
    'instrumentalness': [5.32e-06, 5.76e-06, 0, 2.18e-06, 0.0045, 0.000105, 0, 1.63e-05, 4.46e-06, 0],
    'liveness': [0.175, 0.119, 0.516, 0.0951, 0.177, 0.266, 0.156, 0.194, 0.524, 0.423],
    'valence': [0.355, 0.616, 0.746, 0.56, 0.131, 0.254, 0.511, 0.304, 0.834, 0.678],
    'tempo': [98.932, 75.008, 121.988, 129.981, 120.022, 120.14, 141.89, 104.969, 106.942, 119.995]
}

data2 = {
    'name': ['Eye In The Sky', 'Easy Lover', 'Alive - Remastered Demo', 'Showbiz', 'Supersonic - 2014 Remaster', 
             'Uno', 'untitled 06 | 06.30.2014.', 'Sunburn', 'O Roben Ton Kammenon Dason', 'Unintended'],
    'danceability': [0.823, 0.749, 0.257, 0.236, 0.703, 0.394, 0.669, 0.440, 0.547, 0.487],
    'energy': [0.417, 0.699, 0.912, 0.635, 0.765, 0.654, 0.541, 0.905, 0.301, 0.279],
    'speechiness': [0.032, 0.0674, 0.0488, 0.0565, 0.0452, 0.052, 0.0992, 0.0341, 0.057, 0.0265],
    'acousticness': [0.562, 0.0674, 0, 0.0123, 0.0153, 0.0019, 0.254, 0.018, 0.753, 0.647],
    'instrumentalness': [0.001, 0.0019, 0.0042, 0.216, 0.00339, 0.0019, 0, 0.00452, 0.00746, 0.0019],
    'liveness': [0.0765, 0.0763, 0.144, 0.109, 0.0891, 0.356, 0.254, 0.066, 0.135, 0.110],
    'valence': [0.522, 0.935, 0.219, 0.166, 0.183, 0.526, 0.254, 0.322, 0.378, 0.162],
    'tempo': [111.928, 128.904, 147.711, 124.785, 103.999, 114.694, 89.083, 143.354, 200.542, 139.362]
}

# Convert the data to DataFrames
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Normalize the data (Min-Max Normalization)
def normalize(df):
    return (df - df.min()) / (df.max() - df.min())

# Apply normalization
df1_normalized = normalize(df1.drop(columns=['name']))
df2_normalized = normalize(df2.drop(columns=['name']))

# Plot the normalized data for both datasets
plt.figure(figsize=(14, 6))

# First dataset plot
plt.subplot(1, 2, 1)
df1_normalized.mean().plot(kind='bar', color='b', alpha=0.7)
plt.title('Normalized Features (First Dataset)')
plt.ylabel('Normalized Value')
plt.xticks(rotation=45, ha='right')

# Second dataset plot
plt.subplot(1, 2, 2)
df2_normalized.mean().plot(kind='bar', color='g', alpha=0.7)
plt.title('Normalized Features (Second Dataset)')
plt.xticks(rotation=45, ha='right')

# Display the plots
plt.tight_layout()
plt.show()
