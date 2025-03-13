import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = 'data/mag_data.csv'
data = pd.read_csv(path)

Ch1_volts = data[' Ch 1 Voltage (V)']
Ch2_volts = data[' Ch 2 Voltage (V)']
sample_rate = 1000

plt.plot(Ch1_volts)
plt.plot(Ch2_volts)
plt.show()
#display(data)
plt.plot([max(Ch1_volts[i*10000:(i+1)*10000].tolist()) for i in range(30)])
plt.plot([max(Ch2_volts[i*10000:(i+1)*10000].tolist()) for i in range(30)])
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