import numpy as np
from scipy.signal import firwin, filtfilt, hilbert

def autocorrelation_slow(time_series, lag_interval=0):
    
    mean = sum(time_series)/len(time_series)
    normed_series = time_series-mean
    variance = sum((normed_series)**2) #/len(time_series) normally, but cancels with factor later.
    
    lagged_auto_covariances = np.zeros(len(time_series)-lag_interval)
    lagged_auto_covariances[0] = sum((normed_series)*(normed_series))
    for i in range(1,len(normed_series)-lag_interval-1):
        k = i+lag_interval # lag
        lagged_auto_covariances[i] = sum((normed_series[:-k])*(normed_series[k:])) #/len(time_series))
      
    autocorrelations = np.array(lagged_auto_covariances)/variance
    return autocorrelations

def autocorrelation(time_series, lag_interval=0):
    
    time_series_fft = np.fft.rfft(time_series)
    power_spectrum = np.abs(time_series_fft)**2
    autocorrelations = np.real(np.fft.ifft(power_spectrum))
    normed_autocorrelations = autocorrelations/autocorrelations[0]
    return normed_autocorrelations

def get_harmonic_envelope(received_signal, sample_rate, driving_signal, driving_frequency, order):
    '''
    Computes the envelope for a particular harmonic.\n
    received_signal: time series for which to compute the envelope \n
    sample_rate: frequency at which the received signal is sampled, in [Hz] \n
    driving_signal: time series of the driving signal used to perform lock-in \n
    driving_frequency: frequency of the driving signal, in [Hz] \n
    order: order of the harmonic \n
    returns: tuple of (in-phase component, out-of-phase component, full harmonic envelope)
    '''
    # constructs the analytic representation of the time series for the primary coil
    analytic_fundamental = hilbert(driving_signal)
    # normalizing the driving signal by dividing its time series by the instantaneous envelope
    normed_analytic_fundamental = hilbert(driving_signal / np.abs(analytic_fundamental)) 
    # locks-in received signal at a particular harmonic of the driving frequency
    locked_harmonic = received_signal * normed_analytic_fundamental**order
    # applies a low-pass filter to remove carrier signal and retain only the harmonic envelope
    filter_coeffs = firwin(numtaps=int(sample_rate/(.01*driving_frequency)), cutoff=1, fs=sample_rate, window='boxcar')
    filtered_harmonic = filtfilt(filter_coeffs, 1.0, locked_harmonic)
    filtered_harmonic_inphase_envelope = np.abs(2*filtered_harmonic.real)
    filtered_harmonic_outofphase_envelope = np.abs(2*filtered_harmonic.imag)
    filtered_harmonic_envelope = np.sqrt(filtered_harmonic_inphase_envelope**2 + filtered_harmonic_outofphase_envelope**2)
    return filtered_harmonic_inphase_envelope, filtered_harmonic_outofphase_envelope, filtered_harmonic_envelope

def get_multi_harmonic_envelope(received_signal, sample_rate, driving_signal, driving_frequencies, order):
    '''
    Computes the total envelope for a particular harmonic given a discrete multi-frequency driving signal (i.e. comb).\n
    received_signal: time series for which to compute the envelope \n
    sample_rate: frequency at which the received signal is sampled, in [Hz] \n
    driving_signal: time series of the driving signal used to perform lock-in \n
    driving_frequencies: frequency of the driving signal, in [Hz] \n
    order: order of the harmonic \n
    returns: tuple of (in-phase component, out-of-phase component, full harmonic envelope)
    '''
    # constructs the analytic representation of the time series for the primary coil
    analytic_fundamental = hilbert(driving_signal)
    # normalizing the driving signal by dividing its time series by the instantaneous envelope
    normed_analytic_fundamental = hilbert(driving_signal / np.abs(analytic_fundamental)) 
    # locks-in received signal at a particular harmonic of the driving signal frequencies
    locked_harmonic = received_signal * sum([normed_analytic_fundamental**(f_comb/driving_frequencies[0])
                                                                        **order for f_comb in driving_frequencies])
    # applies a low-pass filter scaled by lowest comb frequency to remove carrier signal and retain only harmonic envelopes
    filter_coeffs = firwin(numtaps=int(sample_rate/(.01*driving_frequencies[0])), cutoff=1, fs=sample_rate, window='boxcar')
    filtered_harmonic = filtfilt(filter_coeffs, 1.0, locked_harmonic)
    filtered_harmonic_inphase_envelope = np.abs(2*filtered_harmonic.real)
    filtered_harmonic_outofphase_envelope = np.abs(2*filtered_harmonic.imag)
    filtered_harmonic_envelope = np.sqrt(filtered_harmonic_inphase_envelope**2 + filtered_harmonic_outofphase_envelope**2)
    return filtered_harmonic_inphase_envelope, filtered_harmonic_outofphase_envelope, filtered_harmonic_envelope

def get_total_envelope(received_signal, sample_rate, driving_frequency):
    '''
    Gets the total envelope for the received signal after low-pass filtering for noise. \n
    received_signal: time series for which to compute the envelope \n
    sample_rate: frequency at which the received signal is sampled, in [Hz] \n
    returns: total envelope
    '''
    filter_coeffs = firwin(numtaps=int(sample_rate/(10*driving_frequency)), cutoff=200, fs=sample_rate, window='boxcar')
    filtered_received_signal = filtfilt(filter_coeffs, 1.0, received_signal)
    return np.abs(hilbert(filtered_received_signal))

