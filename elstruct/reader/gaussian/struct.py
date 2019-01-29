"""
Library of functions to retrieve structural information
from a Gaussian 09e output file

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import phys_constants


# Series of functions to read structural information

def optimized_cartesian_geometry_reader(output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom and Degrees.
    """

    # Pattern to idetify text block of where the geometry is located
    geom_xyz_block_begin_pattern = '-- Stationary point found.'
    geom_xyz_block_end_pattern = 'Distance matrix (angstroms):'

    # Obtain text block of containing the geometry
    geom_xyz_block = repar.block(geom_xyz_block_begin_pattern,
                                 geom_xyz_block_end_pattern,
                                 output_string)

    # Geometry Pattern: INT  INT  INT  FLOAT  FLOAT  FLOAT  NEWLINE 
    geom_xyz_pattern = (
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Grabs the geometry with the atoms indexed by the atom number
    cart_geom_atom_num = repar.cartesian_geometry_pattern_parser(
        geom_xyz_pattern, geom_xyz_block)

    # Change the atom number to the corresponding atomic symbol
    cart_geom = tuple((phys_constants.ATOM_NUM[int(num)], coord)
                      for num, coord in cart_geom_atom_num)

    return cart_geom


def optimized_internal_geometry_reader(output_string):
    """ Retrieves the optimized geometry in internal coordinates.
        Units of Angstrom and Degrees.
    """

    # Pattern to idetify text block of where the geometry is located
    geom_int_block_begin_pattern = '-- Stationary point found.'
    geom_int_block_end_pattern = 'Distance matrix (angstroms):'

    # Obtain text block of containing the geometry
    geom_int_block = repar.block(geom_int_block_begin_pattern,
                                 geom_int_block_end_pattern,
                                 output_string)

    # Geometry Pattern: !  CHARS  FLOAT  -DE/DX =  FLOAT  !  NEWLINE  
    geom_int_pattern = (
        '!' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.ANY_CHAR +
        rep.one_or_more(relib.NONWHITESPACE) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        '-DE/DX =' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        '!'
    )

    # Geometry Pattern: !  CHARS  LETTER  (INT,)  -DE/DX =  FLOAT  !  NEWLINE  
    geom_int_pattern_2 = (
        '!' +
        relib.WHITESPACE +
        relib.ANY_CHAR +
        rep.one_or_more(relib.NONWHITESPACE) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.UPPERCASE_LETTER +
        rep.escape('(' + relib.INTEGER + ',' + ')') +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        '-DE/DX =' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        '!'
    )

    # Get the geometry
    int_geom = repar.pattern_parser(geom_int_pattern, output_string)
    if int_geom is None:
        int_geom = repar.pattern_parser(geom_int_pattern_2, output_string)

    return int_geom


def optimized_zmat_reader(output_string):
    """ zmat
    """

    # PatternS to idetify text block of where the Z-matrix 
    zmat_block_begin_pattern = 'Z-MATRIX (ANGSTROMS AND DEGREES)'
    zmat_block_end_pattern = 'Z-Matrix orientation:'

    # Obtain text block of containing the Z-matrix 
    zmat_block = repar.block(zmat_block_begin_pattern,
                             zmat_block_end_pattern,
                             output_string)

    # Z-Matrix Pattern: INT  INT  CHARS  INT  FLOAT()  INT  FLOAT()  INT  FLOAT()  0
    zmat_pattern = (
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(LETTER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.escape('(') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.INTEGER) +
        relib.INTEGER +
        rep.escape(')') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.escape('(') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape(')') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.escape('(') +
        rep.one_or_more(relib.WHITESPACE) +
        relib.INTEGER +
        rep.escape(')') +
        rep.one_or_more(relib.WHITESPACE) +
        '0'
    )

    return zmat


def init_zmat_reader():
    """ Grab the initial Z-matrix
    """
    # zmat
    begin = 'Symbolic Z-matrix'
    end = 'Initial Paramters'

    #coord
    begin = 'Variables'
    end = 'Initial Paramters'


    return init_zmat


def equil_rot_constant_reader(output_string):
    """ Retrieves the equilibrium rotational constant of the optimized geometry.
        Units of cm-1.
    """

    equil_rot_const_pattern = (
        rep.escape('Rotational constants (GHZ):') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain equil_const string
    all_rot_consts = repar.pattern_parser_list_single_str(equil_rot_const_pattern, output_string)

    # Remove any instances of 0.0000s as well as duplicates
    rot_const_ghz = tuple((const for const in all_rot_consts if const != 0.0))

    # Convert from GHz to cm-1
    equil_rot_const = tuple((const * phys_constants.GHZ_TO_CM
                            for const in rot_const_ghz))

    return equil_rot_const


def effective_rot_constants_reader(output_string):
    """ get effective constants the B(A)
    """

    begin = (
        rep.escape('Be in cm^-1') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('B(A) in cm^-1') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('B(A) in MHz') +
        rep.one_or_more(relib.WHITESPACE)
    )
    end = 'Nielsen Centrigugal Distorsion Constants'

    pattern = (
        relib.LOWERCASE_LETTER +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT
    )

    return eff_rot_consts
