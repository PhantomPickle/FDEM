import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate as interp
import utm

# mag_path = 'data/mag_data.csv'
gps_path = 'data/gps.csv'

# mag_data = pd.read_csv(mag_path)
gps_data = pd.read_csv(gps_path)

utm_lat, utm_lon, zone_num, zone_letter = utm.from_latlon(gps_data['Latitude'], gps_data['Longitude'])

#########################################################################
# Generating synthetic data for testing
# mag_times = [i for i in range(10)]
# mag_voltages = [1.2, 2.2, 2.5, 3.1, 2.7, 2.1, 1.8, 2.7, 4.2, 3.8] 
#                 #2.9, 2.3, 1.5, 1.2, .7, 1.6, 2.6, 3.2, 3.9, 4.8]
# mag_data = pd.DataFrame({'times': mag_times, 'voltage': mag_voltages})

# gps_times = [i+.5 for i in range(10)]
# gps_lat = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# gps_lon = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
# gps_data = pd.DataFrame({'times':gps_times, 'latitude': gps_lat, 'longitude': gps_lon})

# #print(gps_data)
# print(gps_times)

# # Interpolate mag data to gps coords
# mag_voltages_interp = interp.interp1d(mag_times, mag_voltages, kind='cubic', fill_value='extrapolate')
# mag_voltages_at_gps_coords = mag_voltages_interp(gps_times)
# print(mag_voltages_at_gps_coords)
# print(list(zip(gps_lat, gps_lon)))
# #gps_lat_

# # Plotting interpolating magnetic data
# #plt.contour(, mag_voltages_at_gps_coords)
# #plt.plot()
# plt.scatter(mag_times, mag_voltages, label='mag voltages')
# plt.scatter(gps_times, gps_lat, label='latitude')
# plt.scatter(gps_times, mag_voltages_at_gps_coords, label='interpolated mag voltages')
# plt.legend()
# plt.show()
# #plt.scatter(gps_lat, mag_voltages_at_gps_coords)
# plt.show()
############################################################################

