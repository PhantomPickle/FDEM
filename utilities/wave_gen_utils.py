import numpy as np

amplitude = 32767

def gen_chirp(duration, f_i, f_f, sample_rate):
    
    '''
    Generates a chirp (rising instantaneous frequency) \n
    duration: total duration of chirp, in [s] \n
    f_i: starting frequency, in [Hz] \n
    f_f: ending frequency, in [Hz] \n
    sample_rate: sample rate, in [Hz]
    '''
    
    num_frames = int(duration*sample_rate)
    # (frequency in 1/s / sample_rate points per second) * 
    # [(sample_rate points per second / 1 point per cycle) * (2 pi radians per cycle)]
    f_instant = [f_i + i*(f_f-f_i)/num_frames for i in range(num_frames)]
    chirp = [int(amplitude * np.sin(i*(f_instant[i]/sample_rate)*(2*np.pi))) for i in range(num_frames)]
    
    return chirp

def gen_comb(duration, f_min, num_teeth, spacing, sample_rate):
    
    '''
    Generates a frequency comb (evenly spaced frequencies) \n
    duration: total duration of comb, in [s] \n
    f_min: lowest frequency tooth, in [Hz] \n
    num_teeth: number of teeth in the comb \n
    spacing: spacing between teeth, in [Hz] \n
    sample_rate: sample rate, in [Hz]
    '''
    
    num_frames = int(duration*sample_rate)
    # (frequency in 1/s / sample_rate points per second) * 
    # [(sample_rate points per second / 1 point per cycle) * (2 pi radians per cycle)]
    comb_frequencies = [f_min + j*spacing for j in range(num_teeth)]
    comb = sum([np.array([np.sin(i*(f/sample_rate)*(2*np.pi)) for i in range(num_frames)]) for f in comb_frequencies])
    comb = (amplitude * comb/max(comb)).astype(int) # scales normalized comb by desired amplitude
    return comb

def gen_pure_wave(duration, f, sample_rate):
    
    '''
    Generates a single frequency sine wave \n
    duration: duration, in [s] \n
    f: frequency, in [Hz] \n
    sample_rate: sample rate, in [Hz]
    '''
    
    num_frames = int(duration*sample_rate)
    # (frequency in 1/s / sample_rate points per second) * 
    # [(sample_rate points per second / 1 point per cycle) * (2 pi radians per cycle)]
    pure_wave = [int(amplitude * np.sin(i*(f/sample_rate)*(2*np.pi))) for i in range(num_frames)]
    
    return pure_wave