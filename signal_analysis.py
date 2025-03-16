import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from utilities.signal_analysis_methods import autocorrelation

path = 'data/mag_data_fixed.csv'
data = pd.read_csv(path)

Ch1_volts = data['Ch 1 Voltage (V)'].to_numpy()
Ch2_volts = data['Ch 2 Voltage (V)'].to_numpy()
sample_rate = 1000

plt.plot(Ch1_volts)
plt.plot(Ch2_volts)
plt.show()
plt.title('Binned RMS Averages of Secondary Coil Voltages')
plt.plot([np.sqrt(np.mean(np.square(Ch1_volts[i*10000:(i+1)*10000]))).tolist() for i in range(30)], label='Channel 1')
plt.plot([np.sqrt(np.mean(np.square(Ch2_volts[i*10000:(i+1)*10000]))).tolist() for i in range(30)], label='Channel 2')
plt.xlabel('Time (s)')
plt.ylabel('RMS Voltage (V)')
plt.legend()
plt.show()

Ch1_autocorrelation = autocorrelation(Ch1_volts[:2000], lag_interval=1)
Ch2_autocorrelation = autocorrelation(Ch2_volts[:2000], lag_interval=1)
plt.title('Autocorrelations of Secondary Coil Voltages')
plt.plot(Ch1_autocorrelation, label='Channel 1')
plt.plot(Ch2_autocorrelation, label='Channel 2')
plt.xlabel('Time Lag (steps)')
plt.ylabel('Autocorrelation')
plt.legend()
plt.show()

f, t_spec, Sxx = spectrogram(Ch1_volts, fs=sample_rate, nperseg=256)
plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
plt.title('Channel 1 Spectrogram')
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')
plt.colorbar(label='Power (dB)')
plt.show()

f, t_spec, Sxx = spectrogram(Ch2_volts, fs=sample_rate, nperseg=256)
plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
plt.title('Channel 2 Spectrogram')
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')
plt.colorbar(label='Power (dB)')
plt.show()

# print(len(Ch1_volts))
# print([max(Ch1_volts[i*10000:(i+1)*10000].tolist()) for i in range(30)])

# data_fft = np.fft.rfft(data_volts)
# data_fftfreq = np.fft.rfftfreq(len(data_volts),1./sample_rate)
# plt.plot(data_fftfreq, np.abs(data_fft))
# plt.xlim(0,10)
# #plt.plot([60,60], [0, 400])
# plt.yscale('log')
# #plt.xscale('log')
# plt.show()

# Hilbert transform? Multiply time traces of primary and secondary (basically like a lock-in technique)

#call campus recreation 