import numpy as np
import wave as wav
import struct
from utilities.wave_gen_utils import gen_chirp, gen_comb, gen_pure_wave
from scipy.io import wavfile
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import chart_studio.plotly as ply

sample_rate = 48000. # in [Hz]
duration = 10. # in [s]
frequency = 10. # in [Hz]

wav_obj = wav.open('network_analysis_chirp.wav', 'wb')
wav_obj.setnchannels(1) # mono
wav_obj.setsampwidth(2) # num bytes
wav_obj.setframerate(sample_rate)

#values = gen_pure_wave(duration=duration, f=frequency, sample_rate=sample_rate)
values = gen_chirp(duration=duration, f_i=1e3, f_f=100e3, sample_rate=sample_rate)
#values = gen_comb(duration=duration, f_min=10, num_teeth=10, spacing=10, sample_rate=sample_rate)

for i, value in enumerate(values):
    data = struct.pack('<h', value)
    wav_obj.writeframesraw(data)

wav_obj.close()

# sample_rate, samples = wavfile.read('output_waveform.wav')
# wav_fft = np.fft.rfft(samples)
# wav_fftfreq = np.fft.rfftfreq(len(samples),1./sample_rate)

# fig = go.Figure()
# fig.add_trace(go.Scatter(
#     x= wav_fftfreq,
#     y= np.abs(wav_fft), 
#     mode='lines', 
#     name='Comb',
#     line=dict(color='rebeccapurple', width=2)
# ))
# fig.update_layout(
#     title='WAV Frequency Spectrum',
#     xaxis_title='Frequency (Hz)',
#     yaxis_title='Power',
#     template='plotly_dark',
#     hovermode='x unified'
# )
# fig.update_xaxes(range=[0, 200])
# fig.show()
