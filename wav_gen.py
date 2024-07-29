import numpy as np
import wave as wav
import struct
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt


sampleRate = 1000. # in [Hz]
duration = 10. # in [s]
frequency = 100. # in [Hz]
num_frames = int(1e4)

wav_obj = wav.open('output.wav', 'wb')
wav_obj.setnchannels(1) # mono
wav_obj.setsampwidth(2) # num bytes
wav_obj.setframerate(sampleRate)
 
amplitude = 32767 # 16 bit peak to trough, why?
values = [int(amplitude * np.sin(i*(2*np.pi/360))) for i in range(num_frames)]

for i, value in enumerate(values):
#for i in range(num_frames):
#    value =  random.randint(-32767, 32767)
    data = struct.pack('<h', value) # 16 bit bc 'h' is short int apparently
    wav_obj.writeframesraw(data)

wav_obj.close()

sample_rate, samples = wavfile.read('output.wav')
plt.plot(samples)
plt.show()

# wav_obj = wav.open('output.wav', 'rb')
# print(wav_obj.getsampwidth())
# data_buffer = wav_obj.readframes(num_frames)
# print(data_buffer)
# data = struct.unpack('<h', wav_obj.readframes(num_frames))
