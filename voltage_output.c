/*****************************************************************************

    MCC 152 Functions Demonstrated:
        mcc152_a_out_write
        mcc152_info

    Purpose:
        Write values to analog output 0 in a loop.

    Description:
        This example demonstrates writing output data using analog output 0.

*****************************************************************************/
#include <stdbool.h>
#include <math.h>
#include "daqhats_utils.h"

#define CHANNEL     0               // output channel, set to 1 for channel 1
#define OPTIONS     OPTS_DEFAULT    // default output options (voltage), set to 
                                    // OPTS_NOSCALEDATA to use DAC codes

int main(void)
{
    uint8_t address;
    int result;
    double value;
    char options_str[256];

    address = 1

    result = mcc152_open(1);
   
    while (true)
    {
        result = mcc152_a_out_write(1, 0, OPTIONS, value);
    }

    // Reset the output to 0V.
    result = mcc152_a_out_write(address, CHANNEL, OPTIONS, 0.0);
    if (result != RESULT_SUCCESS)
    {
        print_error(result);
        mcc152_close(address);
        return 1;
    }
    
    // Close the device.
    result = mcc152_close(address);
    if (result != RESULT_SUCCESS)
    {
        print_error(result);
        return 1;
    }

    return 0;
}