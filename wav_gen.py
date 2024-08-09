import numpy as np
import wave as wav
import struct
# from scipy.io import wavfile
# import matplotlib.pyplot as plt


sample_rate = 44100. # in [Hz]
duration = 100. # in [s]
frequency = 500. # in [Hz]
num_frames = int(duration*sample_rate)

wav_obj = wav.open('output.wav', 'wb')
wav_obj.setnchannels(1) # mono
wav_obj.setsampwidth(2) # num bytes
wav_obj.setframerate(sample_rate)
 
amplitude = 32767
# (frequency in 1/s / sample_rate points per second) * [(sample_rate points per second / 1 point per cycle) * (2 pi radians per cycle)]
values = [int(amplitude * np.sin(i*(frequency/sample_rate)*(2*np.pi))) for i in range(num_frames)] 
print(values)

for i, value in enumerate(values):
    data = struct.pack('<h', value)
    wav_obj.writeframesraw(data)

wav_obj.close()

# sample_rate, samples = wavfile.read('output.wav')
# print(samples)
# plt.plot(samples)
# plt.show()
