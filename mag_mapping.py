import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate as interp

# mag_path = 'data/mag_data.csv'
# gps_path = 'data/gps.csv'

# mag_data = pd.read_csv(mag_path)
# gps_data = pd.read_csv(gps_path)

# Synthetic data for testing
mag_times = [i for i in range(20)]
mag_voltages = [1.2, 2.2, 2.5, 3.1, 2.7, 2.1, 1.8, 2.7, 4.2, 3.8, 
                2.9, 2.3, 1.5, 1.2, .7, 1.6, 2.6, 3.2, 3.9, 4.8]
mag_data = pd.DataFrame({'times': mag_times, 'voltage': mag_voltages})

gps_times = [i+.5 for i in range(20)]
gps_lat = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
gps_lon = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
gps_data = pd.DataFrame({'times':gps_times, 'latitude': gps_lat, 'longitude': gps_lon})

# interpolate mag data to gps coords

#

plt.plot(gps_data)
