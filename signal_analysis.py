import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utilities.signal_analysis_methods import autocorrelation

path = 'data/mag_data_fixed.csv'
data = pd.read_csv(path)

Ch1_volts = data['Ch 1 Voltage (V)']
Ch2_volts = data['Ch 2 Voltage (V)']
sample_rate = 1000

# plt.plot(Ch1_volts)
# plt.plot(Ch2_volts)
# plt.show()
# #display(data)
# #print(np.mean(np.square([Ch1_volts[i*10000:(i+1)*10000].tolist() for i in range(30)])))
# plt.title('Binned RMS Averages of Secondary Coil Voltages')
# plt.plot([np.sqrt(np.mean(np.square(Ch1_volts[i*10000:(i+1)*10000]))).tolist() for i in range(30)], label='Channel 1')
# plt.plot([np.sqrt(np.mean(np.square(Ch2_volts[i*10000:(i+1)*10000]))).tolist() for i in range(30)], label='Channel 2')
# plt.xlabel('Time (s)')
# plt.ylabel('RMS Voltage (V)')
# plt.legend()
# plt.show()

Ch1_autocorrelation = autocorrelation(Ch1_volts)
Ch2_autocorrelation = autocorrelation(Ch2_volts)
# print(Ch1_autocorrelation)
# plt.title('Autocorrelations of Secondary Coil Voltages')
# plt.plot(Ch1_autocorrelation, label='Channel 1')
# plt.plot(Ch2_autocorrelation, label='Channel 2')
# plt.xlabel('Time Lag (steps)')
# plt.ylabel('Autocorrelation')
# plt.legend()
# plt.show()

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