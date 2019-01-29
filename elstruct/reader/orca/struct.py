"""
Library of functions to retrieve structural information
from a Molpro 2015 output file

Structural currently supported:
(1) final optimized geometry in Cartesian (xyz) coordinates;
(2) final optimized geometry in internal coordinates;
(3) initial geometry in Cartesian (xyz) coordinates;
(4) initial geometry in internal coordinates; and
(5) equilibrium Rotational Constants

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib

# Series of functions to read structural information

def optimized_cartesian_geometry_reader(output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom and degrees.
    """

    # Pattern to identify text block where the geometry is located
    cart_geom_begin_pattern = 'CARTESIAN COORDINATES (ANGSTROEM)'
    cart_geom_end_pattern = 'CARTESIAN COORDINATES (A.U.)'

    # Obtain text block containing the geometry
    cart_geom_block = repar.block(cart_geom_begin_pattern,
                                  cart_geom_end_pattern,
                                  output_string)

    # Geometry Line Pattern: CHARS  FLOAT  FLOAT  FLOAT  NEWLINE
    cart_geom_pattern = (
        rep.capturing(rep.one_or_more(relib.NONWHITESPACE)) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Retrieve the geometry
    cart_geom = repar.cartesian_geometry_pattern_parser(
        cart_geom_pattern, cart_geom_block)

    return cart_geom


def optimized_internal_geometry_reader(output_string):
    """ Retrieves the optimized geometry in internal coordinates.
        Units of Angstrom and degrees.
    """

    # Pattern to identify text block where the geometry is located
    int_geom_begin_pattern = 'INTERNAL COORDINATES (ANGSTROEM)'
    int_geom_end_pattern = 'INTERNAL COORDINATES (A.U.)'

    # Obtain text block containing the geometry
    int_geom_block = repar.block(int_geom_begin_pattern,
                                 int_geom_end_pattern,
                                 output_string)

    # Geometry Line Pattern: CHARS  INT  INT  INT  FLOAT  FLOAT  FLOAT  NEWLINE
    int_geom_pattern = (
        rep.one_or_more(relib.ANY_CHAR) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    # Obtain the xyz coordinates from the block
    all_geom_internal = repar.pattern_parser_1(
        int_geom_pattern, int_geom_block)

    return all_geom_internal
