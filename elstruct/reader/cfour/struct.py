"""
Library of functions to retrieve structural information
from a CFour 2.0 output file

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
from ... import phys_constants


# Series of functions to read structural information

def optimized_cartesian_geometry_reader(output_string):
    """ Retrieves all geometries but last in Cartesian xyz coordinates.
        Units of Angstrom and degrees.
    """

    # Pattern to idetify text block where geometry is located
    cart_geom_begin_pattern = (
        'Z-matrix   Atomic' +
        rep.one_or_more(relib.WHITESPACE) +
        'Coordinates (in bohr)'
    )
    cart_geom_end_pattern = 'Interatomic distance matrix (Angstroms)'

    # Obtain text block of containing the geometry
    cart_geom_block = repar.block(cart_geom_begin_pattern,
                                  cart_geom_end_pattern,
                                  output_string)

    # Geometry Line Pattern: CHARS  INTEGER  FLOAT  FLOAT  FLOAT  NEWLINE
    cart_geom_pattern = (
        rep.capturing(relib.ANY_CHAR) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Retrieve the geometry; currently in Bohrs 
    cart_geom_bohr = repar.pattern_parser_cartesian_geometry(
        cart_geom_pattern, cart_geom_block)

    # Convert from Bohrs to Angstroms
    cart_geom = tuple((sym, (x * phys_constants.BOHR_TO_ANG,
                             y * phys_constants.BOHR_TO_ANG,
                             z * phys_constants.BOHR_TO_ANG))
                      for sym, coord in cart_geom_bohr
                      for x, y, z in coord)

    return cart_geom


def optimized_internal_geometry_reader(output_string):
    """ Retrieves the optimized geometry in internal coordinates.
        Units of Angstrom and degrees.
    """

    # internal coords of optimized geom
    opt_geom_internal_begin_pattern = 'Final ZMATnew file'
    opt_geom_internal_end_pattern = (
        rep.escape('*CFOUR(') +
        rep.one_or_more(relib.ANY_CHAR)
    )

    # Obtain text block of containing the optimized geom in internals
    geom_block = repar.block(opt_geom_internal_begin_pattern,
                             opt_geom_internal_end_pattern,
                             output_string)

    # Retrieve the Z-matrix

    # Retrieve internal coords
    opt_geom_internal_pattern = (
        rep.one_or_more(relib.ANY_CHAR) +
        rep.one_or_more(relib.WHITESPACE) +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    # opt_geom_internal = rep.capturing(opt_geom_internal_pattern)
    opt_geom_internal = 0.0

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
        rep.escape('GHz  (calculated with average atomic masses)')
    )

    # Obtain equil_const string
    all_rot_consts = repar.pattern_parser_list_single_str(equil_rot_const_pattern, output_string)

    # Remove any instances of 0.0000s as well as duplicates
    rot_const_ghz = tuple((const for const in all_rot_consts if const != 0.0))

    # Convert from GHz to cm-1
    equil_rot_const = tuple((const * phys_constants.GHZ_TO_CM
                             for const in rot_const_ghz))

    return equil_rot_const
