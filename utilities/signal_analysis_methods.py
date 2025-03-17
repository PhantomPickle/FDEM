import numpy as np

def autocorrelation(time_series, lag_interval=0):
    
    mean = sum(time_series)/len(time_series)
    variance = sum((time_series-mean)**2) #/len(time_series) normally, but cancels with factor later.
    
    lagged_auto_covariances = np.zeros(len(time_series)-lag_interval)
    for i in range(len(time_series)-lag_interval):
        k = i+lag_interval # lag
        lagged_auto_covariances[i] = sum((time_series[:-k]-mean)*(time_series[k:]-mean)) #/len(time_series))
      
    autocorrelations = np.array(lagged_auto_covariances)/variance
    return autocorrelations