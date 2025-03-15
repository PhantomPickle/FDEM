import numpy as np

def autocorrelation(time_series, lag=1):
    
    mean = sum(time_series)/len(time_series)
    variance = sum((time_series-mean)**2)/len(time_series)
    print(variance)
    
    lagged_auto_covariances = []
    for i in range(len(time_series)-lag):
        k = i+lag
        #print(time_series[i+1:]-mean)
        #print('lac', sum((time_series[k:]-mean)*(time_series[k-1:]-mean))/len(time_series))
        lagged_auto_covariances.append(sum((time_series[i+1:]-mean)*(time_series[i:]-mean))/len(time_series))
      
    print('lac list', lagged_auto_covariances)  
    autocorrelations = np.array(lagged_auto_covariances)/variance
    return autocorrelations