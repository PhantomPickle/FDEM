from time import sleep
from sys import stdout, version_info
from daqhats import mcc172, OptionFlags, SourceType, HatIDs, HatError
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

    num_samples = int(1e5)
    scan_rate = int(1e4)
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
                                    
        hat.a_in_scan_start(0x01, num_samples, options)

        print(f'Starting scan ... Press Ctrl-C to stop\nActual Sampling Frequency: {actual_scan_rate} Hz')

        try:
            read_and_store_data(hat, num_samples)
        except KeyboardInterrupt:
            hat.a_in_scan_stop()

        hat.a_in_scan_cleanup()

    except (HatError, ValueError) as err:
        print('\n', err)

def read_and_store_data(hat, num_samples_per_channel):
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

    # Exports scan data to a csv
    logname = "scan.csv"
    path = os.path.expanduser('~apa/Documents/FDEM/data/'+logname)
    logfile = open(path, "w")
    logfile.write("Voltage (V)\n")
    for i, voltage in enumerate(scan_data):
        logfile.write(f"{voltage:.7f}\n")

    print('\n')
    print('Data exported to CSV.')


if __name__ == '__main__':
    main()
