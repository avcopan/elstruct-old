""" set of parsers to return bits of info
"""

from collections import OrderedDict
from .find import all_captures
from .find import last_capture
from .pattern import maybe
from .pattern import escape
from .pattern import capturing
from .pattern import one_or_more
from .pattern_lib import ANY_CHAR
from .pattern_lib import FLOAT


# Helper function to find text block

def block(head_string, foot_string, string):
    """ Returns a block of text
    """
    head_pattern = escape(head_string)
    foot_pattern = escape(foot_string)
    block_pattern = capturing(
        head_pattern +
        one_or_more(ANY_CHAR, greedy=False) +
        foot_pattern)

    return last_capture(block_pattern, string)


def all_blocks(head_string, foot_string, string):
    """ Returns a block of text
    """
    head_pattern = escape(head_string)
    foot_pattern = escape(foot_string)
    block_pattern = capturing(
        head_pattern +
        one_or_more(ANY_CHAR, greedy=False) +
        foot_pattern)

    return all_captures(block_pattern, string)


# ENERGY PATTERN PARSER FUNCTIONS #

def energy_pattern_parser(pattern, output_string):
    """ Searches for single string pattern to capture a single energy.
        Returns the LAST instance of this value as a float.
    """

    # Capture the final pattern in the output file
    energy_str = last_capture(pattern, output_string)

    # Check if pattern values is found, if so, convert to float
    energy_val = (None if energy_str is None else float(energy_str))

    return energy_val


# FREQUENCY PATTERN PARSER FUNCTIONS #

def harmonic_frequencies_pattern_parser(pattern, output_string):
    """ Searches for pattern in out_string to capture series of values.
        Return each instance of these values in a single list of floats.
    """

    # Locate the final pattern in the output file
    harm_freq_strings = all_captures(pattern, output_string)
    
    
    # Check if pattern values is found, if so, convert to float, remove zeros and imags
    if harm_freq_strings is not None:
        harm_freq_lists = []
        for harm_freq_string in harm_freq_strings:
            harm_freq_lists.append(
                    all_captures(
                        FLOAT+maybe('i'), harm_freq_string
                    )
            ) 

        all_harm_freq_vals = []
        for harm_freq_list in harm_freq_lists:
            for freq in harm_freq_list:
                if 'i' in freq:
                    val = -1.0 * float(freq.replace('i', '').strip())
                else:
                    val = float(freq.strip())
                all_harm_freq_vals.append(val)
                harm_freq_vals = [freq for freq in all_harm_freq_vals if freq != 0.0]
    else:
        harm_freq_vals = None

    return harm_freq_vals


def harmonic_frequencies_pattern_parser_2(pattern, output_string):
    """ Searches for pattern in out_string to capture series of values.
        Return each instance of these values in a single list of floats.
    """

    # Locate the final pattern in the output file
    harm_freqs = all_captures(pattern, output_string)
    
    # Check if pattern values is found, if so, convert to float, remove zeros and imags
    if harm_freqs is not None:
        all_harm_freq_vals = []
        for freq in harm_freqs:
            if 'i' in freq:
                val = -1.0 * float(freq.replace('i', '').strip())
            else:
                val = float(freq.strip())
            all_harm_freq_vals.append(val)
        harm_freq_vals = [freq for freq in all_harm_freq_vals if freq != 0.0]
    else:
        harm_freq_vals = None

    return harm_freq_vals


# def anharm_matrix_pattern_parser(output_string):
#     """ Return anharm matrix
#     """
#     anharm_matrix 
#     same as hessian
# 
#     return anharm_matrix
# 
# 
# def vib_rot_matrix_pattern_parser(output_string):
#     """ vib rot matrix
#     """
# 
#     vib-rot
#     similar to geom Q[dontneed]  float float float
# 
#     return vib_rot_matrix
# 
# 
# def centrif_dist_pattern_parser(output_string):
#     """ centrig dist constants
#     """
#     centrif constants
#     similar to geom
# 
#     return cent_dist_consts


# STRUCTURE PATTERN PARSER FUNCTIONS #

def cartesian_geometry_pattern_parser(pattern, output_string):
    """ Return the geometry, consisting of lines of atomic symbols and coordinates
    """
    cart_geom_elements = all_captures(pattern, output_string)

    cart_geom = tuple((sym, (float(x), float(y), float(z)))
                      for sym, x, y, z in cart_geom_elements)

    return cart_geom


# SURFACE PATTERN PARSER FUNCTIONS #

def hessian_pattern_parser(pattern, output_string):
    """ Return the Hessian in either Cartesian or internal coordinates
    """

    # Get the list of each elements as strings
    hess_lines = all_captures(pattern, output_string)

    # Create ordered dict to maintain order
    hess = OrderedDict()

    # Add the lines
    for line in hess_lines:
        hess_id = line.strip().split()[0]
        hess_elems = line.strip().split()[1:]
        if hess_id not in hess:
            hess[hess_id] = hess_elems
        else:
            hess[hess_id] += hess_elems

    hess2 = []
    for key, value in hess.iteritems():
        hess2.append(value)

    return hess2


def cartesian_gradient_pattern_parser(pattern, output_string):
    """ Return the geometry, consisting of lines of atomic symbols and coordinates
    """
    cart_grad_elements = all_captures(pattern, output_string)

    cart_grad = tuple((sym, (float(x), float(y), float(z)))
                      for sym, x, y, z in cart_grad_elements)

    return cart_grad

# def hessian_pattern_parser_2(output_string):
#     """ Return the Hessian in either Cartesian or internal coordinates
#     """
# hessian cart and internal
#     read from a 3xn cfour
# 
# 
# def cartesian_gradient_pattern_parser_2(output_string):
#     """ Get cart grad 2
#     """
#     long list molpro
# 
#     return cart_grad
