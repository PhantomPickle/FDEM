import numpy as np
import matplotlib.pyplot as plt

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
