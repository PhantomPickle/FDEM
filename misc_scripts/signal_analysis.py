import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.signal import spectrogram
from utilities.signal_analysis_utils import autocorrelation

path = 'data/mag_data_fixed.csv'
data = pd.read_csv(path)

Ch1_voltage = data['Ch 1 Voltage (V)'].to_numpy()
Ch2_voltage = data['Ch 2 Voltage (V)'].to_numpy()
sample_rate = 1000

# plt.plot(Ch1_voltage)
# plt.plot(Ch2_voltage)
# plt.show()

fig = go.Figure()
fig.add_trace(go.Line(
    y= Ch1_voltage, 
    mode='lines', 
    name='Channel 1',
    line=dict(color='rebeccapurple', width=2)
))
fig.add_trace(go.Line(
    y= Ch2_voltage, 
    mode='lines', 
    name='Channel 2',
    line=dict(color='royalblue', width=2)
))
fig.update_layout(
    title='Secondary Coil Voltages',
    xaxis_title='Time (steps)',
    yaxis_title='Voltage (V)',
    template='plotly_dark',
    hovermode='x unified'
)
fig.show()

# plt.title('Binned RMS Averages of Secondary Coil Voltages')
# plt.plot([np.sqrt(np.mean(np.square(Ch1_volts[i*10000:(i+1)*10000]))).tolist() for i in range(30)], label='Channel 1')
# plt.plot([np.sqrt(np.mean(np.square(Ch2_volts[i*10000:(i+1)*10000]))).tolist() for i in range(30)], label='Channel 2')
# plt.xlabel('Time (s)')
# plt.ylabel('RMS Voltage (V)')
# plt.legend()
# plt.show()

Ch1_rms_voltage = [np.sqrt(np.mean(np.square(Ch1_voltage[i*10000:(i+1)*10000]))).tolist() for i in range(30)]
Ch2_rms_voltage = [np.sqrt(np.mean(np.square(Ch2_voltage[i*10000:(i+1)*10000]))).tolist() for i in range(30)]

fig = go.Figure()
fig.add_trace(go.Line(
    y= Ch1_rms_voltage, 
    mode='lines', 
    name='Channel 1',
    line=dict(color='rebeccapurple', width=2)
))
fig.add_trace(go.Line(
    y= Ch2_rms_voltage, 
    mode='lines', 
    name='Channel 2',
    line=dict(color='royalblue', width=2)
))
fig.update_layout(
    title='Binned RMS Averages of Secondary Coil Voltages',
    xaxis_title='Time (s)',
    yaxis_title='RMS Voltage (V)',
    template='plotly_dark',
    hovermode='x unified'
)
fig.show()

Ch1_autocorrelation = autocorrelation(Ch1_voltage[:10000], lag_interval=1)
Ch2_autocorrelation = autocorrelation(Ch2_voltage[:10000], lag_interval=1)

# plt.title('Autocorrelations of Secondary Coil Voltages')
# plt.plot(Ch1_autocorrelation, label='Channel 1')
# plt.plot(Ch2_autocorrelation, label='Channel 2')
# plt.xlabel('Time Lag (steps)')
# plt.ylabel('Autocorrelation')
# plt.legend()
# plt.show()

fig = go.Figure()
fig.add_trace(go.Line(
    y= Ch1_autocorrelation, 
    mode='lines', 
    name='Channel 1',
    line=dict(color='rebeccapurple', width=2)
))
fig.add_trace(go.Line(
    y= Ch2_autocorrelation, 
    mode='lines', 
    name='Channel 2',
    line=dict(color='royalblue', width=2)
))
fig.update_layout(
    title='Autocorrelations of Secondary Coil Voltages',
    xaxis_title='Time Lag (steps)',
    yaxis_title='Autocorrelation',
    template='plotly_dark',
    hovermode='x unified'
)
fig.show()

frequencies, times, Sxx = spectrogram(Ch1_voltage, fs=sample_rate, nperseg=256)

fig = go.Figure(data=go.Heatmap(
    z=10 * np.log10(Sxx),  # Convert to dB scale
    x=times,
    y=frequencies,
    colorscale='Plasma'
))
fig.update_layout(
    title='Channel 1 Spectrogram',
    xaxis_title='Time [s]',
    yaxis_title='Frequency [Hz]',
    coloraxis_colorbar=dict(title='Power (dB)'),
    template='plotly_dark'
)
fig.show()

frequencies, times, Sxx = spectrogram(Ch2_voltage, fs=sample_rate, nperseg=256)

fig = go.Figure(data=go.Heatmap(
    z=10 * np.log10(Sxx),  # Convert to dB scale
    x=times,
    y=frequencies,
    colorscale='Plasma'
))
fig.update_layout(
    title='Channel 2 Spectrogram',
    xaxis_title='Time [s]',
    yaxis_title='Frequency [Hz]',
    coloraxis_colorbar=dict(title='Power (dB)'),
    template='plotly_dark'
)
fig.show()


# plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
# plt.title('Channel 1 Spectrogram')
# plt.xlabel('Time [s]')
# plt.ylabel('Frequency [Hz]')
# plt.colorbar(label='Power (dB)')
# plt.show()

# f, t_spec, Sxx = spectrogram(Ch2_volts, fs=sample_rate, nperseg=256)
# plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
# plt.title('Channel 2 Spectrogram')
# plt.xlabel('Time [s]')
# plt.ylabel('Frequency [Hz]')
# plt.colorbar(label='Power (dB)')
# plt.show()

# data_fft = np.fft.rfft(data_volts)
# data_fftfreq = np.fft.rfftfreq(len(data_volts),1./sample_rate)
# plt.plot(data_fftfreq, np.abs(data_fft))
# plt.xlim(0,10)
# #plt.plot([60,60], [0, 400])
# plt.yscale('log')
# #plt.xscale('log')
# plt.show()

# Hilbert transform? Multiply time traces of primary and secondary (basically like a lock-in technique)

# Call campus recreation 