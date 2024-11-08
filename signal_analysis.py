import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = 'data/scan_3m_4Hz.csv'
data = pd.read_csv(path)

data_volts = data['Voltage (V)']
sample_rate = 1000
#display(data)
plt.plot(data_volts[0:1000])
plt.show()

data_fft = np.fft.rfft(data_volts)
data_fftfreq = np.fft.rfftfreq(len(data_volts),1./sample_rate)
plt.plot(data_fftfreq, np.abs(data_fft))
plt.xlim(0,10)
#plt.plot([60,60], [0, 400])
plt.yscale('log')
#plt.xscale('log')
plt.show()