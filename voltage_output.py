#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from __future__ import print_function
from daqhats import mcc152, OptionFlags, SourceType, HatIDs
import numpy as np

def output_signal(hat, amplitude = .1, offset = 0, num_periods = 10):
    for i in range(num_periods):
        for i in range(360):
            output = amplitude * np.sine(i*(2*np.pi/360)) + offset
            hat.a_out_write(channel = 0, value = output, options = OptionFlags.DEFAULT)
        # Is this going to be adding an extra point redundantly at beginning/end of each period?

def main():

    output_hat = mcc152(1, num_periods = 1000)

    input('\nPress ENTER to begin output ...')
    print('Starting output ... Press Ctrl-C to stop\n')

    output_signal(output_hat)

if __name__ == '__main__':
    main()
