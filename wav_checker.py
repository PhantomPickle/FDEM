import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import chart_studio.plotly as ply

# sample_rate, samples_pure = wavfile.read('output_waveform_pure.wav')
# sample_rate, samples_comb = wavfile.read('output_waveform_comb.wav')
# sample_rate, samples_chirp = wavfile.read('output_waveform_chirp.wav')
sample_rate, samples_chirp = wavfile.read('network_analysis_chirp.wav')

# pure_fft = np.fft.rfft(samples_pure)
# pure_fftfreq = np.fft.rfftfreq(len(samples_pure),1./sample_rate)
# comb_fft = np.fft.rfft(samples_comb)
# comb_fftfreq = np.fft.rfftfreq(len(samples_comb),1./sample_rate)
chirp_fft = np.fft.rfft(samples_chirp)
chirp_fftfreq = np.fft.rfftfreq(len(samples_chirp),1./sample_rate)

fig = go.Figure()
# fig.add_trace(go.Scatter(
#     y= samples_pure, 
#     mode='lines', 
#     name='Pure',
#     line=dict(color='gold', width=2)
# ))
# fig.add_trace(go.Scatter(
#     y= samples_comb, 
#     mode='lines', 
#     name='Comb',
#     line=dict(color='tomato', width=2)
# ))
fig.add_trace(go.Scatter(
    y= samples_chirp, 
    mode='lines', 
    name='Chirp',

    line=dict(color='royalblue', width=2)
))
# fig.add_trace(go.Scatter(
#     x= pure_fftfreq,
#     y= np.abs(pure_fft), 
#     mode='lines', 
#     name='Pure',
#     line=dict(color='gold', width=2)
# ))
# fig.add_trace(go.Scatter(
#     x= pure_fftfreq,
#     y= np.abs(comb_fft), 
#     mode='lines', 
#     name='Comb',
#     line=dict(color='tomato', width=2)
# ))
# fig.add_trace(go.Scatter(
#     x= pure_fftfreq,
#     y= np.abs(chirp_fft), 
#     mode='lines', 
#     name='Chirp',
#     line=dict(color='limegreen', width=2)
# ))
# fig.update_layout(
#     title='WAV Frequency Spectrum',
#     xaxis_title='Frequency (Hz)',
#     yaxis_title='Power',
#     template='plotly_dark',
#     hovermode='x unified'
# )
fig.update_layout(
    title='Frequency Comb Time Series',
    xaxis_title='Time (s)',
    yaxis_title='Voltage (V)',
    template='plotly_dark',
    hovermode='x unified'
)
#fig.update_xaxes(range=[0, 200])
fig.show()