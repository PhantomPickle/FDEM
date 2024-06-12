import daqhats as daq

daq.hat_list()

#######################################################################
# Initializing DAQ hats

# MCC 152 DAQ hat used for signal generation
sig_gen = daq.mcc152()

# MCC 172 DAQ hat used for signal acquisition
sig_acq = daq.mcc172() 
sig_acq.blink_led(10)

# ADC sampling clock generated on signal acquisition hat and not shared
# sample rate ~1kHz (rounded to 51.2 kHz / 51)
# sig_acq.a_in_clock_config_write(daq.LOCAL, 1000) 
# print(sig_acq.a_in_clock_config_read())
# print(sig_acq.a_in_scan_actual_rate())

########################################################################
# Signal acquisition

# sig_acq.a_in_scan_start()
# scan_data = sig_acq.a_in_scan_read()
# sig_acq.a_in_scan_cleanup()


########################################################################