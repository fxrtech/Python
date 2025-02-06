#!/usr/bin/env python
#=============================================================================
#
# Low-pass Filter Response Plotter
#
# This is a Python 2 script that depends on matplotlib and numpy.
#
#=============================================================================

"""
Low-pass Filter Response Plotter
================================

This script generates a plot of vOUT vs. time for a passive "RC" low-pass
circuit (shown below).

Low-pass filter circuit:

    o----^^^^----+----o
   vIN    R      |   vOUT
              C ---
                ---
                 |
    o------------+----o

Assumptions:

    vIN @ t0 = 0 Volts
    vIN exhibits an ideal step response to input changes

Usage:

    python lowpass.py vIN R C

    Where:
        vIN is the final input voltage in volts.
        R is the resistance of R in ohms.
        C is the capacitance of C in farads.

"""


import math
import sys

import matplotlib
import matplotlib.pyplot as pyplot
import numpy


#=============================================================================
def get_vout( t, vin, r, c ):
    """
    Computes vOUT at a given time for the given circuit parameters.

    The normal RC voltage response for a given time is:

        vOUT(t) = vIN * ( 1 - ( e ** ( ( -1 * t ) / ( R * C ) ) ) )

    @param t   Charge time value in seconds
    @param vin Input voltage in volts
    @param r   Series resistance in ohms
    @param c   Parallel capacitance in farads
    @return    Output voltage at the given time
    """
    tau   = r * c                       # Time constant
    exp   = -1 * t / tau                # Exponent
    ratio = ( 1 - ( math.e ** exp ) )   # Voltage ratio
    vout  = vin * ratio                 # Output voltage
    return vout


#=============================================================================
def plot_filter( vin, r, c ):
    """
    Plots the low-pass filter response for the given circuit parameters.

    @param vin Input voltage in volts
    @param r   Series resistance in ohms
    @param c   Parallel capacitance in farads
    """

    # Intermediate and constant values.
    tau      = r * c    # Time constant
    tfinal   = 5 * tau  # Plot five time constants worth of points
    points   = 2048     # Number of points to calculate
    times    = []       # X-axis data (time values)
    response = []       # Y-axis data (voltage values)

    # Compute all output voltages at each time point.
    for t in numpy.arange( 0.0, tfinal, ( 1.0 / points ) ):
        times.append( t )
        response.append( get_vout( t, vin, r, c ) )

    # Set descriptive title and labels for the data in the plot.
    pyplot.title(
        'RC Circuit Voltage Response vs. Time'
        '\nR: {} Ohms, C: {} Farads, vIN: {} Volts'.format( r, c, vin )
    )
    pyplot.xlabel( 'Time (seconds)' )
    pyplot.ylabel( 'vOUT (volts)' )

    # Add the X-Y data to the plot.
    pyplot.plot( times, response )

    # Display the plot UI.
    pyplot.show()


#=============================================================================
def main( argv ):
    """
    Script execution entry point

    @param argv List of arguments passed to the script
    @return     Shell exit code (0 = success)
    """

    # Imports when using this as a script
    import argparse

    # Create and configure an argument parser.
    parser = argparse.ArgumentParser(
        description = 'Low Pass Filter Response Plotter'
    )
    parser.add_argument(
        'vIN',
        help = 'Final input voltage in volts.',
        type = float
    )
    parser.add_argument(
        'R',
        help = 'Series resistance in ohms.',
        type = float
    )
    parser.add_argument(
        'C',
        help = 'Parallel capacitance in farads.',
        type = float
    )

    # Parse the arguments.
    args = parser.parse_args( argv[ 1 : ] )

    # Plot the filter response.
    plot_filter( args.vIN, args.R, args.C )

    # Return normal exit status.
    return 0


#=============================================================================
if __name__ == "__main__":
    sys.exit( main( sys.argv ) )

