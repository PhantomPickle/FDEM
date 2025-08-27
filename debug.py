import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utilities.signal_analysis_utils import get_harmonic_envelope, get_multi_harmonic_envelope, get_total_envelope

mag_path = 'data/mag_comb_dynamic_engi_08-19-25.csv'

sample_rate = int(2e3) # in [Hz]
driving_frequency = 100 # in [Hz]
comb_frequencies = [i for i in range(10, 110, 10)]
mag_data = pd.read_csv(mag_path)
mag_times = mag_data['Times (s)'].to_numpy()
ch1_voltages = mag_data['Ch 1 (V)'].to_numpy()
ch2_voltages = mag_data['Ch 2 (V)'].to_numpy()
primary_voltages = mag_data['Primary (V)'].to_numpy()
# AC voltages computed by subtracting means from raw voltages
ch1_AC_voltages = ch1_voltages - np.mean(ch1_voltages)
ch2_AC_voltages = ch2_voltages - np.mean(ch2_voltages)
primary_AC_voltages = primary_voltages - np.mean(primary_voltages)

ch1_total_comb_envelope = get_multi_harmonic_envelope(ch1_AC_voltages, sample_rate, primary_AC_voltages, comb_frequencies, 1)[2]
plt.plot(ch1_total_comb_envelope)
plt.show()