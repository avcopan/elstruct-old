"""
Library of functions to retrieve structural information
from a Psi4 1.0 output file

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib


# Series of functions to read structural information

def optimized_cartesian_geometry_reader(output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """

    # Pattern to identify text block where geometry is located
    cart_geom_begin_pattern = 'Final (previous) structure:'
    cart_geom_end_pattern = 'Saving final (previous) structure'

    # Obtain text block containing the geometry
    cart_geom_block = repar.block(cart_geom_begin_pattern,
                                  cart_geom_end_pattern,
                                  output_string)

    # Pattern for the xyz coordinate of each atom
    cart_geom_pattern = (
        rep.capturing(relib.UPPERCASE_LETTER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    cart_geom = repar.cartesian_geometry_pattern_parser(
        cart_geom_pattern, cart_geom_block)

    return cart_geom


# def opt_geom_internal_reader(output_string):
#    """ Retrieves the optimized geometry in internal coordinates.
#        Units of Angstrom and degrees.
#        TODO Grab stuff for the initial coords
#    """
#
#    # internal coords of optimized geom
#    opt_geom_internal_begin_pattern = 'OPTKING Finished Execution'
#    opt_geom_internal_end_pattern = 'Removing binary optimization data file.'
#
#    # Obtain test block containing the optimized geometry in xyz coordinates
#    opt_geom_internal_block = repar.block(opt_geom_internal_begin_pattern,
#                                          opt_geom_internal_end_pattern,
#                                          output_string)
#
#    # Pattern for the xyz coordinate of each atom
#    opt_geom_zmat_pattern = (
#        rep.capturing(
#            rep.one_or_more(relib.UPPERCASE_LETTER) +
#            rep.one_or_more(relib.DIGIT) +
#            '=' +
#            rep.one_or_more(relib.WHITESPACE) +
#            relib.FLOAT
#        )
#    )
#
#    opt_geom_coords_pattern = (
#        rep.capturing(
#            rep.one_or_more(relib.ANY_CHAR) +
#            rep.one_or_more(relib.WHITESPACE) +
#            '=' +
#            rep.one_or_more(relib.WHITESPACE) +
#            relib.FLOAT
#        )
#    )
#
#    # Obtain the xyz coordinates from the block
#    opt_geom_zmat = repar.pattern_parser_1(
#      opt_geom_internal_pattern, opt_geom_internal_block)
#
#
#    return opt_geom_internal


def equil_rot_constant_reader(output_string):
    """ Retrieves the equilibrium rotational constant of the optimized geometry.
        Units of cm-1.
    """

    equil_rot_const_pattern = (
        'Rotational constants:' +
        rep.one_or_more(relib.WHITESPACE) +
        'A =' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'B =' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'C =' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('[cm^-1]')
    )

    # Obtain equil_const string
    all_rot_consts = repar.pattern_parser_list_single_str(equil_rot_const_pattern, output_string)

    # Remove any instances of 0.0000s as well as duplicates
    equil_rot_const = [const for const in all_rot_consts if const != 0.0]

    return equil_rot_const
