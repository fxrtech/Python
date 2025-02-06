#!/usr/bin/env python
#=============================================================================
#
# Gear Shifting Sequence Generator
#
#=============================================================================

"""
Gear Shifting Sequence Generator
================================

This program generates a sequence of shift changes from one combination of
gears to a new combination of gears for a goal gear ratio.

Usage:

    python shiftseq.py ratio front rear

    Where:
        ratio is the desired gear ratio
        front is the initial front gear
        rear is the initial rear gear

"""


import sys


#=============================================================================
# Constants used in this module.
_FRONT_COGS = [ 38, 30 ]            # Front cog tooth counts
_REAR_COGS  = [ 28, 23, 19, 16 ]    # Rear cog tooth counts


#=============================================================================
# Pre-compute a table of all gearing combinations as gear ratios.
_combos = []
for front in _FRONT_COGS:
    row = list()
    for rear in _REAR_COGS:
        row.append( front / float(  rear ) )
    _combos.append( row )


#=============================================================================
def find_next( curr_y, curr_x, final_y, final_x ):
    """
    Determines the next pair of coordinates within the gear-shifting
    combination table that takes the smallest step possible towards the final
    coordinates.

    @param curr_y  The current Y coordinate
    @param curr_x  The current X coordinate
    @param final_y The final Y coordinate
    @param final_x The final X coordinate
    """

    # Need to increment Y.
    if curr_y < final_y:
        next_y = curr_y + 1

    # Need to decrement Y.
    elif curr_y > final_y:
        next_y = curr_y - 1

    # Reached Y.
    else:
        next_y = curr_y

    # Need to increment X.
    if curr_x < final_x:
        next_x = curr_x + 1

    # Need to decrement X.
    elif curr_x > final_x:
        next_x = curr_x - 1

    # Reached X.
    else:
        next_x = curr_x

    # Check for the case where both coordinates can change.
    if ( next_y != curr_y ) and ( next_x != curr_x ):

        # Compute the distance to the next ratio.
        delta_x = _combos[ curr_y ][ next_x ]
        delta_y = _combos[ next_y ][ curr_x ]

        # Favor making smaller changes.
        if delta_x < delta_y:
            return curr_y, next_x
        else:
            return next_y, curr_x

    # Return the next coordinate.
    return next_y, next_x


#=============================================================================
def generate_shifts( ratio, ifront, irear ):
    """
    Produces a sequence of gear shifting steps to produce a desired gear ratio
    given an initial front/rear gearing.

    @param ratio  The desired gear ratio
    @param ifront The initial front gear tooth count
    @param irear  The initial rear gear tooth count
    @return       A list containing two-tuples of gear combination indexes
                  that reach the goal ratio as close as possible
    """

    # Ratio must be a valid ratio (positive, non-zero).
    if ratio <= 0.0:
        raise ValueError( "Invalid gear ratio '{}'".format( ratio ) )

    # Make sure the initial front and rear gears are value.
    if ifront not in _FRONT_COGS:
        raise ValueError( "Invalid front gear '{}'".format( front ) )
    if irear not in _REAR_COGS:
        raise ValueError( "Invalid rear gear '{}'".format( rear ) )

    # Minimum ratio delta for goal ratio.
    min_delta = 999999.0

    # The origin and goal coorindates.
    origin = None
    goal   = None

    # Iterate through each gear combination.
    for findex, front in enumerate( _FRONT_COGS ):
        for rindex, rear in enumerate( _REAR_COGS ):

            # Check to see if this is the origin.
            if ( front == ifront ) and ( rear == irear ):
                origin = ( findex, rindex )

            # Check to see if this is a candidate goal.
            delta = ratio - ( front / float( rear ) )
            if ( delta >= 0 ) and ( delta < min_delta ):
                min_delta = delta
                goal = ( findex, rindex )

    # Check to see if shifting is necessary.
    if origin == goal:
        return []

    # Create a list to store each shift step.
    sequence = [ origin ]

    # Begin shifting through adjacent gear combinations.
    combo = find_next( *( origin + goal ) )
    sequence.append( combo )
    while combo != goal:
        combo = find_next( *( combo + goal ) )
        sequence.append( combo )

    # Return the shift sequence steps.
    return sequence


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
        description = 'Gear Shifting Sequence Generator',
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
    parser.add_argument(
        'front',
        help = 'Specify the initial front gear tooth count.',
        type = int
    )
    parser.add_argument(
        'rear',
        help = 'Specify the initial rear gear tooth count.',
        type = int
    )

    # Parse the arguments.
    args = parser.parse_args( argv[ 1 : ] )

    # Generate the list of shifting changes to achieve the goal ratio.
    sequence = generate_shifts( args.ratio, args.front, args.rear )

    # Check for no shifting sequence necessary.
    if len( sequence ) == 0:
        print 'Goal ratio is already achieved: F:{} R:{} Ratio:{:.4}'.format(
            args.front,
            args.rear,
            ( args.front / float( args.rear ) )
        )

    # Shifting is necessary.
    else:

        # Reference to the final step for reporting.
        final = sequence[ -1 ]

        # Create a message to display.
        message = '''Desired ratio : {goal}
Initial Front : {ifront}
 Initial Rear : {irear}
  Final Front : {ffront}
   Final Rear : {frear}
     Sequence :
  {sequence}'''

        # Format the sequence steps for readability.
        steps = []
        for offset, step in enumerate( sequence ):
            front = _FRONT_COGS[ step[ 0 ] ]
            rear  = _REAR_COGS[ step[ 1 ] ]
            steps.append(
                '{}: F:{} R:{} Ratio:{:.4}'.format(
                    offset + 1,
                    front,
                    rear,
                    ( front / float( rear ) )
                )
            )

        # Display the results.
        print message.format(
            goal     = args.ratio,
            ifront   = args.front,
            irear    = args.rear,
            ffront   = _FRONT_COGS[ final[ 0 ] ],
            frear    = _REAR_COGS[ final[ 1 ] ],
            sequence = '\n  '.join( steps )
        )

    # Return normal exit status.
    return 0


#=============================================================================
if __name__ == "__main__":
    sys.exit( main( sys.argv ) )

