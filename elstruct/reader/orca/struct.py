"""
Library of functions to retrieve structural information from a Molpro 2015 output file

Structural currently supported:
(1) final optimized geometry in Cartesian (xyz) coordinates;
(2) final optimized geometry in internal coordinates;
(3) initial geometry in Cartesian (xyz) coordinates;
(4) initial geometry in internal coordinates; and
(5) equilibrium Rotational Constants

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-11"

from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### HELPER FUNCTION TO RETRIEVE TEXT BLOCK; TODO: Move to rere library #####

def block(head_string, foot_string, string):
    """ Returns a block of text
    """
    head_pattern = rep.escape(head_string)
    foot_pattern = rep.escape(foot_string)
    block_pattern = rep.capturing(
        head_pattern + rep.one_or_more(relib.ANY_CHAR, greedy=False) +
        foot_pattern)
    return ref.last_capture(block_pattern, string)

##### Patterns #####


def all_geom_xyz_reader(output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom and degrees.
    """

    # Pattern to idetify block of output string where optimized geometry is located
    all_geom_xyz_begin_pattern = 'CARTESIAN COORDINATES (ANGSTROEM)'
    all_geom_xyz_end_pattern = 'CARTESIAN COORDINATES (A.U.)'

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

    # Obtain block of output string containing the optimized geometry in xyz coordinates
    all_geom_block = repar.block(all_geom_xyz_begin_pattern, all_geom_xyz_end_pattern, output_string)

    # Obtain the xyz coordinates from the block
    opt_geom_xyz = ref.capturing(opt_geom_block, opt_geom_xyz_pattern)

    return all_geom_xyz

def all_geom_internal_reader(output_string):
    """ Retrieves the optimized geometry in internal coordinates.
        Units of Angstrom and degrees.
    """

    # internal coords of optimized geom
    all_geom_internal_begin_pattern = 'INTERNAL COORDINATES (ANGSTROEM)'
    all_geom_internal_end_pattern = 'INTERNAL COORDINATES (A.U.)'

    all_geom_internal = (
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

    return all_geom_internal

def equil_rot_constant_reader(output_string):
    """ Retrieves the equilibrium rotational constant of the optimized geometry.
        Units of cm-1.
    """

    return equil_rot_const


##### Dictionary for strings to find the geometries in the files #####

STRUCTURE_READERS = {
    params.STRUCTURE.ALL_GEOM_XYZ: all_geom_xyz_reader,
    params.STRUCTURE.ALL_GEOM_INT: all_geom_internal_reader,
    params.STRUCTURE.EQUIL_ROT_CONST: equil_rot_const_reader,
}
