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
from ... import params


# Series of functions to read structural information

def all_geom_xyz_reader(output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom and degrees.
    """

    # Pattern to idetify text block where optimized geometry is located
    all_geom_xyz_begin_pattern = 'CARTESIAN COORDINATES (ANGSTROEM)'
    all_geom_xyz_end_pattern = 'CARTESIAN COORDINATES (A.U.)'

    # Obtain text block of containing the optimized geometry in xyz coordinates
    all_geom_xyz_block = repar.block(all_geom_xyz_begin_pattern,
                                     all_geom_xyz_end_pattern,
                                     output_string)

    # Pattern for the xyz coordinate of each atom
    all_geom_xyz_pattern = (
        rep.one_or_more(relib.ANY_CHAR) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    cart_geom = repar.pattern_parser_cartesian_geometry(
        all_geom_xyz_pattern, all_geom_xyz_block)

    return cart_geom


def all_geom_internal_reader(output_string):
    """ Retrieves the optimized geometry in internal coordinates.
        Units of Angstrom and degrees.
    """

    # internal coords of optimized geom
    all_geom_internal_begin_pattern = 'INTERNAL COORDINATES (ANGSTROEM)'
    all_geom_internal_end_pattern = 'INTERNAL COORDINATES (A.U.)'

    # Obtain text block containing the optimized geometry in xyz coordinates
    all_geom_internal_block = repar.block(
        all_geom_internal_begin_pattern,
        all_geom_internal_end_pattern,
        output_string)

    all_geom_internal_pattern = (
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
        all_geom_internal_pattern, all_geom_internal_block)

    return all_geom_internal


# Dictionary for strings to find the geometries in the files

STRUCTURE_READERS = {
    params.STRUCTURE.OPT_GEOM_XYZ: all_geom_xyz_reader,
    params.STRUCTURE.OPT_GEOM_INT: all_geom_internal_reader,
}
