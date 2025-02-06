#!/usr/bin/env python
#=============================================================================
#
# Gear Combinarion Calculator
#
#=============================================================================

"""
Gear Combination Calculator
===========================

This program computes the closest gear ratio from a provided set of gear
integer values.  The results are displayed along with the actual gear ratio
achieved with the gearing combination.

Usage:

    python gearcombo.py ratio

    Where:
        ratio is the desired gear ratio

"""


import sys


#=============================================================================
# Constants used in this module.
_FRONT_COGS = [ 38, 30 ]            # Front cog tooth counts
_REAR_COGS  = [ 28, 23, 19, 16 ]    # Rear cog tooth counts


#=============================================================================
def compute_combo( ratio ):
    """
    Computes the closest gearing combination for a specified ratio given the
    constant cog tooth counts.

    @param ratio The desired gear ratio
    @return      A two-tuple containing the front and rear tooth counts to
                 most closely match the requested ratio
    """

    # Ratio must be a valid ratio (positive, non-zero).
    if ratio <= 0.0:
        raise ValueError( "Invalid gear ratio '{}'".format( ratio ) )

    # Store the minimum ratio delta and the gear combination.
    min_delta = 999999.0
    min_combo = ( 0, 0 )

    # Iterate through each combination of gear ratios.
    for front in _FRONT_COGS:
        for rear in _REAR_COGS:

            # Compute the current gear ratio.
            current_ratio = front / float( rear )

            # Compute the difference between this and the goal ratio.
            delta = ratio - current_ratio

            # Check for a new ratio candidate (rounding down).
            if ( delta >= 0 ) and ( delta < min_delta ):
                min_delta = delta
                min_combo = ( front, rear )

    # Return the combination with the closest gear ratio to the goal.
    return min_combo


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
        description = 'Cog Ratio Calculator',
        add_help    = False
    )
    parser.add_argument(
        '-h',
        '--help',
        default = False,
        help    = 'Display this help message and exit.',
        action  = 'help'
    )
    parser.add_argument(
        'ratio',
        help = 'Specify the desired gear ratio.',
        type = float
    )

    # Parse the arguments.
    args = parser.parse_args( argv[ 1 : ] )

    # Compute the gear tooth counts for this ratio.
    front, rear = compute_combo( args.ratio )

    # Create a message to display.
    message = '''Desired ratio : {goal:.4}
        Front : {front}
         Rear : {rear}
  Final ratio : {final:.4}'''

    # Display the results.
    print message.format(
        goal  = args.ratio,
        front = front,
        rear  = rear,
        final = ( front / float( rear ) )
    )

    # Return normal exit status.
    return 0


#=============================================================================
if __name__ == "__main__":
    sys.exit( main( sys.argv ) )

