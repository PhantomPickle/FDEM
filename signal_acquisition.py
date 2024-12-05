from time import sleep
from sys import stdout, version_info
from daqhats import mcc172, OptionFlags, SourceType, HatIDs, HatError
from datetime import datetime as date
import numpy as np
import os

'''
amplitude = .1
dc_offset = 0
for i in range(360):
    output = amplitude * np.sine(i*(2*np.pi/360)) + dc_offset
    output_hat.a_out_write(0, output, options)
'''

def main(): # pylint: disable=too-many-locals, too-many-statements

    scan_duration = 30 # In [s]
    scan_rate = int(1e4)
    num_samples = scan_duration*scan_rate
    options = OptionFlags.DEFAULT

    try:

        hat = mcc172()

        #hat.iepe_config_write(0, 0)

        # Configure the clock and wait for sync to complete.
        hat.a_in_clock_config_write(SourceType.LOCAL, scan_rate)

        synced = False
        while not synced:
            (_source_type, actual_scan_rate, synced) = hat.a_in_clock_config_read()
            if not synced:
                sleep(0.005)

        # Gets start time in [s] and starts scan
        start_time = date.now().second                            
        hat.a_in_scan_start(0x01, num_samples, options)

        print(f'Starting scan ... Press Ctrl-C to stop\nActual Sampling Frequency: {actual_scan_rate} Hz')

        try:
            scan_data = read_and_store_data(hat, num_samples, start_time)
            print('\n')
            export(scan_data, start_time, scan_rate)

        except KeyboardInterrupt:
            hat.a_in_scan_stop()

        hat.a_in_scan_cleanup()

    except (HatError, ValueError) as err:
        print('\n', err)

def read_and_store_data(hat, num_samples_per_channel, t0):
    """
    Reads data from the DAQ HAT and stores the data in a csv file.  
    The reads are executed in a loop that continues until either 
    the scan completes or an overrun error is detected.

    Args:
        hat (mcc172): The mcc172 HAT device object.
        samples_per_channel: The number of samples to read for each channel.

    Returns:
        None
    """

    total_samples_read = 0
    read_request_size = 1000
    timeout = 5.0
    scan_data = np.zeros(num_samples_per_channel)

    # Since the read_request_size is set to a specific value, a_in_scan_read()
    # will block until that many samples are available or the timeout is
    # exceeded.

    # Continuously reads data until Ctrl-C is
    # pressed or the number of samples requested has been read.
    while total_samples_read < num_samples_per_channel:
        read_result = hat.a_in_scan_read(read_request_size, timeout)

        # Check for an overrun error
        if read_result.hardware_overrun:
            print('\n\nHardware overrun\n')
            break
        elif read_result.buffer_overrun:
            print('\n\nBuffer overrun\n')
            break

        samples_read = len(read_result.data)
        total_samples_read += samples_read

        print(f'\r Samples read: {total_samples_read:12}/{num_samples_per_channel}.......\
               {int(100*total_samples_read/num_samples_per_channel)}%', end='')

        # Stores the current chunk of data
        start_index = total_samples_read - read_request_size
        stop_index = total_samples_read
        scan_data[start_index:stop_index] = read_result.data

    return scan_data

def export(scan_data, start_time, scan_rate):
    '''
    Generates array of times for each sample, referenced to the system time at the start of
    recording by the DAQ.
    Exports magnetic data from the DAQ and corresponding timings to a CSV.

    Args:
    scan_data: magnetic data recorded by the DAQ
    start_time: initial system time
    scan_rate: sampling frequency of the DAQ
    '''
    
    scan_times = [(start_time/scan_rate)*i for i in range(len(scan_data))]

    logname = "mag_data.csv"
    path = os.path.expanduser('~apa/Documents/FDEM/data/'+logname)
    logfile = open(path, "w")
    logfile.write("Times (s), Voltage (V)\n")
    for i in range(len(scan_data)):
        logfile.write(f"{scan_times[i]}, {scan_data[i]:.7f}\n")
    logfile.close()

if __name__ == '__main__':
    main()
