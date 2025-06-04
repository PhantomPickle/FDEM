from time import sleep
from sys import stdout, version_info
from daqhats import mcc172, OptionFlags, SourceType, HatError
from utilities.daqhats_utils import select_hat_device, enum_mask_to_string, \
chan_list_to_mask
from datetime import datetime as date
import numpy as np
import os

def main(): # pylint: disable=too-many-locals, too-many-statements

    channels = [0, 1]
    channel_mask = chan_list_to_mask(channels)
    num_channels = len(channels)

    scan_duration = 60 # In [s]
    scan_rate = int(2e3)
    num_samples = scan_duration*scan_rate
    options = OptionFlags.DEFAULT

    try:

        secondary_hat = mcc172(address=0)
        primary_hat = mcc172(address=2)

        # Configure the clock and wait for sync to complete.
        secondary_hat.a_in_clock_config_write(SourceType.LOCAL, scan_rate)
        primary_hat.a_in_clock_config_write(SourceType.LOCAL, scan_rate)

        synced = False
        while not synced:
            (_source_type, actual_scan_rate, synced) = secondary_hat.a_in_clock_config_read()
            if not synced:
                sleep(0.005)
        synced = False
        while not synced:
            (_source_type, actual_scan_rate, synced) = primary_hat.a_in_clock_config_read()
            if not synced:
                sleep(0.005)

        # Gets start time in [s] and starts scan
        start_time = date.now().second                            
        secondary_hat.a_in_scan_start(channel_mask, num_samples, options)
        primary_hat.a_in_scan_start(channel_mask, num_samples, options)

        print(f'Starting scan ... Press Ctrl-C to stop\nActual Sampling Frequency: {actual_scan_rate} Hz')

        try:
            secondary_scan_data = read_and_store_data(secondary_hat, num_samples, start_time, num_channels)
            primary_scan_data = read_and_store_data(primary_hat, num_samples, start_time, num_channels)
            print('\n')
            export(secondary_scan_data, primary_scan_data, start_time, scan_rate)

        except KeyboardInterrupt:
            secondary_hat.a_in_scan_stop()
            primary_hat.a_in_scan_stop()

        secondary_hat.a_in_scan_cleanup()
        primary_hat.a_in_scan_cleanup()

    except (hatError, ValueError) as err:
        print('\n', err)

def calc_rms(data, channel, num_channels, num_samples_per_channel):
    """ Calculate RMS value from a block of samples. """
    rms_voltage = np.sqrt((data[channel]**2) / num_samples_per_channel)
    return rms_voltage

def read_and_store_data(hat, num_samples_per_channel, t0, num_channels):
    """
    Reads data from the DAQ hat, displays RMS voltages for each block of data,
    and stores the data in a csv file.  
    The reads are executed in a loop that continues until either 
    the scan completes or an overrun error is detected.

    Args:
        hat (mcc172): The mcc172 hat device object.
        mum_samples_per_channel: The number of samples to read for each channel.
        t0: scan start time
        num_channels: number of recording channels

    Returns:
        None
    """

    total_samples_read = 0
    read_request_size = 1000
    timeout = 5.0
    scan_data = {'Channel 1': np.zeros(num_samples_per_channel), 
                 'Channel 2': np.zeros(num_samples_per_channel)}

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

        samples_read = int(len(read_result.data) / num_channels)
        total_samples_read += samples_read

        print(f'\r Samples read: {total_samples_read:12}/{num_samples_per_channel}.......\
               {int(100*total_samples_read/num_samples_per_channel)}%\n')
        
        # Displays the RMS voltage for the current shunk of data
        for i in range(num_channels):
            rms_voltage = calc_rms(read_result.data, i, num_channels, num_samples_per_channel)
            print(f'Ch {i+1}: {rms_voltage:.5f} Vrms\n')

        # Stores the current chunk of data
        start_index = total_samples_read - read_request_size
        stop_index = total_samples_read
        scan_data['Channel 1'][start_index:stop_index] = read_result.data[:-1:2]
        scan_data['Channel 2'][start_index:stop_index] = read_result.data[1::2]

    print("Scan completed.")
    return scan_data

def export(secondary_scan_data, primary_scan_data, start_time, scan_rate):
    '''
    Generates array of times for each sample, referenced to the system time at the start of
    recording by the DAQ.
    Exports magnetic data from the DAQ and corresponding timings to a CSV.

    Args:
    scan_data: magnetic data recorded by the DAQ
    start_time: initial system time
    scan_rate: sampling frequency of the DAQ
    '''
    
    scan_times = [start_time+(i/scan_rate) for i in range(len(secondary_scan_data['Channel 1']))]

    logname = "mag_data.csv"
    path = os.path.expanduser('~apa/Documents/FDEM/data/'+logname)
    logfile = open(path, "w")
    print("Writing mag data to log file.")
    logfile.write("Times (s),Secondary Ch 1 Voltage (V),Secondary Ch 2 Voltage (V),Primary Voltage (V)\n")
    for i in range(len(secondary_scan_data['Channel 1'])):
        logfile.write(f"{scan_times[i]}, {secondary_scan_data['Channel 1'][i]:.7f},{secondary_scan_data['Channel 2'][i]:.7f},\
                                         {primary_scan_data['Channel 1'][i]:.7f}\n")
    logfile.close()

if __name__ == '__main__':
    main()

