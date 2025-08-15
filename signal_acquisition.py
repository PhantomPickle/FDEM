from time import sleep
from sys import stdout, version_info
from daqhats import mcc172, OptionFlags, SourceType, HatError, TriggerModes
from utilities.daqhats_utils import select_hat_device, enum_mask_to_string, \
chan_list_to_mask
from datetime import datetime as dt
import numpy as np
import os

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'

def main():

    channels = [{0},{0, 1}]
    scan_duration = 5 # In [s]
    sample_rate = int(2e3)
    num_samples = scan_duration*sample_rate
    options = OptionFlags.DEFAULT
    trigger_mode = TriggerModes.RISING_EDGE

    try:

        primary_hat = mcc172(address=2)
        secondary_hat = mcc172(address=0)
        hats = [primary_hat, secondary_hat]

        # Configure the clocks with primary hat as master and wait for sync to complete.
        primary_hat.a_in_clock_config_write(SourceType.MASTER, sample_rate)
        secondary_hat.a_in_clock_config_write(SourceType.SLAVE, sample_rate)
        synced = False
        while not synced:
            (_source_type, actual_sample_rate, synced) = primary_hat.a_in_clock_config_read()
            if not synced:
                sleep(0.005)
        
        # Configure the triggers
        primary_hat.trigger_config(SourceType.MASTER, trigger_mode)
        secondary_hat.trigger_config(SourceType.SLAVE, trigger_mode)

        # Gets start time in [s] and starts scan
        start_time = dt.now().hour*3600 + dt.now().minute*60 + dt.now().second                            
        for i, hat in enumerate(hats):
            channel_mask = chan_list_to_mask(channels[i])
            hat.a_in_scan_start(channel_mask, num_samples, options)

        #print('\nWaiting for trigger ... Press Ctrl-C to stop scan \n')

        try:
            # Monitor the trigger status on the master device.
            #wait_for_trigger(primary_hat)
            print(f'\nStarting scan ... \nActual Sampling Frequency: {actual_sample_rate} Hz')
            scan_data = read_and_store_data(hats, num_samples, start_time, channels)
            print('\n')
            export(scan_data, start_time, sample_rate)

        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\nAborted\n')
    
    except (HatError, ValueError) as error:
        print('\n', error) 
            
    finally:
        for hat in hats:
            hat.a_in_scan_stop()
            hat.a_in_scan_cleanup()

def wait_for_trigger(hat):
    """
    Monitor the status of the specified HAT device in a loop until the \n
    triggered status is True or the running status is False. \n

    Args: \n
        hat: The mcc172 HAT device object on which the status will be monitored.
    """
    # Read the status only to determine when the trigger occurs.
    is_running = True
    is_triggered = False
    while is_running and not is_triggered:
        status = hat.a_in_scan_status()
        is_running = status.running
        is_triggered = status.triggered

def calc_rms(data, channel, num_channels, num_samples_per_channel):
    """ Calculate RMS value from a block of samples. """
    rms_voltage = np.sqrt(np.array([data[i]**2 for i in range(len(data))])/num_samples_per_channel)
    return rms_voltage

def read_and_store_data(hats, num_samples_per_channel, t0, channels):
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
        scan_data
    """

    samples_read_per_channel = [0,0] # Two elements, one for each hat
    total_samples_read_per_channel = [0,0]
    read_request_size = 1000
    timeout = 5.0
    is_running = True
    scan_data = {'Primary': np.zeros(num_samples_per_channel),
                 'Ch 1': np.zeros(num_samples_per_channel), 
                 'Ch 2': np.zeros(num_samples_per_channel)}

    # Since the read_request_size is set to a specific value, a_in_scan_read()
    # will block until that many samples are available or the timeout is
    # exceeded.

    # Continuously reads data until Ctrl-C is
    # pressed or the number of samples requested has been read.
    while True:
        for i, hat in enumerate(hats):
            read_result = hat.a_in_scan_read(read_request_size, timeout)
            is_running &= read_result.running
            # Records total samples read so far
            samples_read_per_channel[i] = int(len(read_result.data) / len(channels[i]))
            total_samples_read_per_channel[i] += samples_read_per_channel[i]
            # Stores the current chunk of data
            if i == 0:
                scan_data['Primary'][total_samples_read_per_channel[i]-samples_read_per_channel[i]:\
                                     total_samples_read_per_channel[i]] = read_result.data
            if i == 1:
                scan_data['Ch 1'][total_samples_read_per_channel[i]-samples_read_per_channel[i]:\
                                     total_samples_read_per_channel[i]] = read_result.data[0]
                scan_data['Ch 2'][total_samples_read_per_channel[i]-samples_read_per_channel[i]:\
                                     total_samples_read_per_channel[i]] = read_result.data[1]

            # Check for an overrun error
            if read_result.hardware_overrun:
                print('\n\nHardware overrun\n')
                break
            elif read_result.buffer_overrun:
                print('\n\nBuffer overrun\n')
                break

        
        # Displays the progress in terms of samples read
        print(f'\r Samples read: {total_samples_read_per_channel[0]:12}/{num_samples_per_channel}.......\
               {int(100*total_samples_read_per_channel[0]/num_samples_per_channel)}%\n')
        
        # Displays the RMS voltage for the current chunk of data
        rms_voltage = calc_rms(scan_data['Primary'], num_samples_per_channel)
        print(f'Primary: {rms_voltage:.5f} Vrms\n')
        rms_voltage = calc_rms(scan_data['Ch 1'], num_samples_per_channel)
        print(f'Ch 1: {rms_voltage:.5f} Vrms\n')
        rms_voltage = calc_rms(scan_data['Ch 2'], num_samples_per_channel)
        print(f'Ch 2: {rms_voltage:.5f} Vrms\n')
        
        if not is_running:
            print("Scan completed.")
            break
        return scan_data

def export(scan_data, start_time, sample_rate):
    '''
    Generates array of times for each sample, referenced to the system time at the start of
    recording by the DAQ.
    Exports magnetic data from the DAQ and corresponding timings to a CSV.

    Args:
    scan_data: magnetic data recorded by the DAQ
    start_time: initial system time
    sample_rate: sampling frequency of the DAQ
    '''
    
    scan_times = [start_time+(i/sample_rate) for i in range(len(scan_data['Ch 1']))]

    logname = "mag.csv"
    path = os.path.expanduser('~apa/Documents/FDEM/data/'+logname)
    logfile = open(path, "w")
    print("Writing mag data to log file.")
    logfile.write("Times (s),Secondary Ch 1 Voltage (V),Secondary Ch 2 Voltage (V),Primary Voltage (V)\n")
    for i in range(len(scan_data['Primary'])):
        logfile.write(f"{scan_times[i]}, {scan_data['Primary'][i]:.7f}, \
                                         {scan_data['Ch 1'][i]:.7f}, {scan_data['Ch 2'][i]:.7f}\n")
    logfile.close()

if __name__ == '__main__':
    main()

