""" set of parsers to return bits of info
"""

from .find import all_captures
from .find import last_capture
from .pattern import escape
from .pattern import capturing
from .pattern import one_or_more
from .pattern_lib import ANY_CHAR

##### HELPER FUNCTION TO RETRIEVE TEXT BLOCK  #####

def block(head_string, foot_string, string):
    """ Returns a block of text
    """
    head_pattern = escape(head_string)
    foot_pattern = escape(foot_string)
    block_pattern = capturing(
        head_pattern + one_or_more(ANY_CHAR, greedy=False) +
        foot_pattern)
    
    return last_capture(block_pattern, string)


##### Set of parser functions to return information from regex searching functions ####

def sing_float(pattern, output_string):
    """ Searches for pattern in output_string to capture a single value.
        Returns the LAST instance of this value as a float.
    """

    # Capture the final pattern in the output file
    pattern_str = last_capture(pattern, output_string)

    # Check if pattern values is found, if so, convert to float
    sing_float = (None if pattern_str is None else float(pattern_str))

    return sing_float

def list_float(pattern, output_string):
    """ Searches for pattern in out_string to capture series of values.
        Return each instance of these values in a single list of floats.
    """

    # Locate the final pattern in the output file
    pattern_str = all_captures(pattern, output_string)

    # Check if pattern values is found, if so, convert to float
    if pattern_str is not None:
        list_float = [float(val.strip()) for string in pattern_str for val in string.split()]
    else:
        list_float = None

    return list_float

def pattern_parser_1(pattern, output_string):
    """ Returns singles string made of several lines where entire line is captured
    """

    # Obtain the xyz coordinates from the block
    pattern_str = all_captures(pattern, output_string)

    pattern_val = (None if pattern_str is None else '\n'.join(pattern_str))

    return pattern_val

def pattern_parser_2(pattern, output_string):
    """ Returns singles string made of several lines part of line is captured
    """

    # Obtain the xyz coordinates from the block
    pattern_str = all_captures(pattern, output_string)

    if pattern_str is not None:
        pattern_val_init = ['    '.join(elem) for elem in pattern_str]
        pattern_val = '\n'.join(pattern_val_init)
    else:
        pattern_val = None

    return pattern_val

def pattern_parser_cartesian_geometry(pattern, output_string):
    """ Return the geometry, consisting of lines of atomic symbols and coordinates
    """
    cart_geom_elements = all_captures(pattern, output_string)

    cart_geom = tuple((sym, (float(x), float(y), float(z)))
                      for sym, x, y, z in cart_geom_elements)

    return cart_geom

