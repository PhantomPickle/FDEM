import numpy as np
import wave as wav
import struct
from utilities.wave_gen_utils import gen_chirp, gen_comb, gen_pure_wave
# from scipy.io import wavfile
# import matplotlib.pyplot as plt


sample_rate = 48000. # in [Hz]
duration = 10. # in [s]
frequency = 10. # in [Hz]

wav_obj = wav.open('output_waveform.wav', 'wb')
wav_obj.setnchannels(1) # mono
wav_obj.setsampwidth(2) # num bytes
wav_obj.setframerate(sample_rate)
 
#values = gen_pure_wave(duration=duration, f=frequency, sample_rate=sample_rate)
#values = gen_chirp(duration=duration, f_i=10, f_f=200, sample_rate=sample_rate)
values = gen_comb(duration=duration, f_min=10, num_teeth=10, spacing=10, sample_rate=sample_rate)

for i, value in enumerate(values):
    data = struct.pack('<h', value)
    wav_obj.writeframesraw(data)

wav_obj.close()

# sample_rate, samples = wavfile.read('output.wav')
# print(samples)
# plt.plot(samples[0:int(5e2)])
# plt.show()
