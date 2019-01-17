"""
Library of functions to retrieve structural information from a CFour 2.0 output file

Structural currently supported:
(1) final optimized geometry in Cartesian (xyz) coordinates;
(2) final optimized geometry in internal coordinates;
(3) initial geometry in Cartesian (xyz) coordinates;
(4) initial geometry in internal coordinates; and
(5) equilibrium Rotational Constants

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read structural information #####

def all_geom_xyz_reader(output_string):
    """ Retrieves all geometries but last in Cartesian xyz coordinates.
        Units of Angstrom and degrees.
    """

    # Pattern to idetify block of output string where optimized geometry is located
    m1_geom_xyz_begin_pattern = 'Z-matrix   Atomic' + rep.one_or_more(relib.WHITESPACE) + 'Coordinates (in bohr)'
    m1_geom_xyz_end_pattern = 'Interatomic distance matrix (Angstroms)'

    # Pattern for the xyz coordinate of each atom
    m1_geom_xyz_pattern = (
        rep.one_or_more(relib.ANY_CHAR) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    # Obtain block of output string containing the optimized geometry in xyz coordinates
    m1_geom_block = repar.block(m1_geom_xyz_begin_pattern, m1_geom_xyz_end_pattern, output_string)

    # Obtain the xyz coordinates from the block
    opt_geom_xyz = ref.capturing(m1_geom_block, m1_geom_xyz_pattern)

    return opt_geom_xyz

def opt_geom_internal_reader(output_string):
    """ Retrieves the optimized geometry in internal coordinates.
        Units of Angstrom and degrees.
    """

    # internal coords of optimized geom
    opt_geom_internal_begin_pattern = 'Final ZMATnew file'
    opt_geom_internal_end_pattern = 'Property integrals will be calculated'

    opt_geom_internal_pattern = (
        rep.one_or_more(relib.ANY_CHAR) +
        rep.one_or_more(relib.WHITESPACE) +
        '='
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    return opt_geom_internal

def equil_rot_constant_reader(output_string):
    """ Retrieves the equilibrium rotational constant of the optimized geometry.
        Units of cm-1.
    """

    equil_rot_const_pattern = (
        'Rotational constants:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'GHz  \(calculated with average atomic masses\)'
    )

    return equil_rot_const


##### Dictionary for strings to find the geometries in the files #####

STRUCTURE_READERS = {
    params.STRUCTURE.OPT_GEOM_XYZ: opt_geom_xyz_reader,
    params.STRUCTURE.OPT_GEOM_INT: opt_geom_internal_reader,
    params.STRUCTURE.INIT_GEOM_XYZ: init_geom_xyz_reader,
    params.STRUCTURE.INIT_GEOM_INT: init_geom_internal_reader,
    params.STRUCTURE.EQUIL_ROT_CONST: equil_rot_const_reader,
}
