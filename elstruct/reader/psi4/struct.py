"""
Library of functions to retrieve structural information from a Psi4 1.0 output file

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read structural information #####

def opt_geom_xyz_reader(output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """

    # Pattern to idetify block of output string where optimized geometry is located
    opt_geom_xyz_begin_pattern = 'Final (previous) structure:'
    opt_geom_xyz_end_pattern = 'Saving final (previous) structure'

    # Obtain block of output string containing the optimized geometry in xyz coordinates
    opt_geom_xyz_block = repar.block(opt_geom_xyz_begin_pattern,
                               opt_geom_xyz_end_pattern,
                               output_string)

    # Pattern for the xyz coordinate of each atom
    opt_geom_xyz_pattern = (
        rep.capturing(
            relib.UPPERCASE_LETTER +
            rep.one_or_more(relib.WHITESPACE) +
            relib.FLOAT +
            rep.one_or_more(relib.WHITESPACE) +
            relib.FLOAT +
            rep.one_or_more(relib.WHITESPACE) +
            relib.FLOAT
        )
    )

    # Obtain the xyz coordinates from the block
    opt_geom_xyz = repar.pattern_parser_1(opt_geom_xyz_pattern, opt_geom_xyz_block)

    return opt_geom_xyz

def opt_geom_internal_reader(output_string):
    """ Retrieves the optimized geometry in internal coordinates.
        Units of Angstrom and degrees.
        TODO Grab stuff for the initial coords
    """

    # internal coords of optimized geom
    opt_geom_internal_begin_pattern = 'OPTKING Finished Execution'
    opt_geom_internal_end_pattern = 'Removing binary optimization data file.'

    # Obtain block of output string containing the optimized geometry in xyz coordinates
    opt_geom_internal_block = repar.block(opt_geom_internal_begin_pattern,
                                    opt_geom_internal_end_pattern,
                                    output_string)

    # Pattern for the xyz coordinate of each atom
    opt_geom_zmat_pattern = (
        rep.capturing(
            rep.one_or_more(relib.UPPERCASE_LETTER) +
            rep.one_or_more(relib.DIGIT) +
            '=' +
            rep.one_or_more(relib.WHITESPACE) +
            relib.FLOAT
        )
    )

    opt_geom_coords_pattern - (
        rep.capturing(
            rep.one_or_more(relib.ANY_CHAR) +
            rep.one_or_more(relib.WHITESPACE) +
            '=' +
            rep.one_or_more(relib.WHITESPACE) +
            relib.FLOAT
        )
    )

    # Obtain the xyz coordinates from the block
    opt_geom_zmat = repar.pattern_parser_1(opt_geom_internal_pattern, opt_geom_internal_block)


    return opt_geom_internal

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
        '\[cm^-1\]'
    )

    # Obtain equil_const string
    all_rot_consts = repar.list_float(equil_rot_const_pattern, output_string)

    # Remove any instances of 0.0000s as well as duplicates
    equil_rot_const = list(set([const for const in all_rot_consts if const != 0.0]))

    return equil_rot_const


##### Dictionary for strings to find the geometries in the files #####

STRUCTURE_READERS = {
    params.STRUCTURE.OPT_GEOM_XYZ: opt_geom_xyz_reader,
    params.STRUCTURE.OPT_GEOM_INT: opt_geom_internal_reader,
    params.STRUCTURE.EQUIL_ROT_CONST: equil_rot_constant_reader,
}
