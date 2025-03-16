#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from __future__ import print_function
from daqhats import mcc152, OptionFlags, SourceType, HatIDs
import numpy as np

def output_signal(hat, amplitude = .1, offset = 0, num_periods = 10):
    one_period_vals = np.array([amplitude * np.sin(i*(2*np.pi/360)) + offset for i in range(360)])
    full_vals = np.array([])
    for i in range(num_periods):
        full_vals = np.append(full_vals, one_period_vals)
    for i, val in enumerate(full_vals):
        hat.a_out_write(channel = 0, value = val, options = OptionFlags.DEFAULT)
    # Is this going to be adding an extra point redundantly at beginning/end of each period?

def main():

    output_hat = mcc152(1)

    input('\nPress ENTER to begin output ...')
    print('Starting output ... Press Ctrl-C to stop\n')

    while(True): 
        output_hat.a_out_write(channel = 0, value = 0, options = OptionFlags.DEFAULT)
        output_hat.a_out_write(channel = 0, value = 5, options = OptionFlags.DEFAULT)

    #output_signal(output_hat, amplitude = 1, offset = 1, num_periods = 1000)
    output_hat.a_out_write(channel = 0, value = 0, options = OptionFlags.DEFAULT) # sets output back to 0

if __name__ == '__main__':
    main()
