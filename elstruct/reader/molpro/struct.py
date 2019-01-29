"""
Library of functions to retrieve structural information
from a Molpro 2018 output file

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
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """

    # Pattern to identify text block of where geometry is located
    cart_geom_begin_pattern = 'END OF GEOMETRY OPTIMIZATION'
    cart_geom_end_pattern = 'Geometry written to block'

    # Obtain text block containing the geometry 
    cart_geom_block = repar.block(cart_geom_begin_pattern,
                                  cart_geom_end_pattern,
                                  output_string)

    # Geometry Line Pattern: CHARS  FLOAT  FLOAT  FLOAT  NEWLINE
    cart_geom_pattern = (
        rep.capturing(relib.ANY_CHAR) +
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
        TODO Grab stuff for the initial coords
    """

    # Pattern to identify text block of where geometry is located
    int_geom_begin_pattern = 'Optimized variables'
    int_geom_end_pattern = '*********************'

    # Obtain text block containing the geometry 
    int_geom_block = repar.block(int_geom_begin_pattern,
                                 int_geom_end_pattern,
                                 output_string)

    # Geometry Line Pattern: AAA = FLOAT
    int_geom_pattern = (
        rep.capturing(
            rep.one_or_more(relib.UPPERCASE_LETTER) +
            rep.one_or_more(relib.DIGIT) +
            '=' +
            rep.one_or_more(relib.WHITESPACE) +
            relib.FLOAT
        )
    )

    # Retrieve the geometry
    int_geom = repar.pattern_parser_1(int_geom_pattern, int_geom_block)

    return int_geom


def initial_cartesian_geometry_reader(output_string):
    """ Retrieves the initial geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """

    # Pattern to identify text block of where geometry is located
    cart_geom_begin_pattern = 'ATOMIC COORDINATES'
    cart_geom_end_pattern = 'Bond lengths in Bohr (Angstrom)'

    # Obtain text block containing the geometry
    cart_geom_block = repar.block(cart_geom_begin_pattern,
                                  cart_geom_end_pattern,
                                  output_string)

    # Geometry Line Pattern: INT  CHARS  FLOAT  FLOAT  FLOAT  FLOAT  NEWLINE
    cart_geom_pattern = (
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.UPPERCASE_LETTER) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
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


def initial_internal_geometry_reader(output_string):
    """ Retrieves the initial geometry in internal coordinates.
        Units of Angstrom and degrees.
    """

    # Retrieve the Z-Matrix

    # Initial Z-matrix definition
    init_z_matrix_begin_pattern = 'Geometry = {'
    init_z_matrix_end_pattern = 'Variables initialized'

    # Get the text block containing the Z-matrix
    init_z_matrix_block = repar.block(
        init_z_matrix_begin_pattern,
        init_z_matrix_end_pattern,
        output_string)

    # Pattern for the each line of the Z-matrix
    one_atom_line = (
        relib.UPPERCASE_LETTER +
        rep.maybe(relib.INTEGER)
    )
    two_atom_line = one_atom_line + (
        rep.one_or_more(relib.WHITESPACE) +
        rep.maybe(rep.one_or_more(relib.ANY_CHAR)) +
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.ANY_CHAR) +
        rep.maybe(relib.INTEGER)
    )
    three_atom_line = two_atom_line + (
        rep.one_or_more(relib.WHITESPACE) +
        rep.maybe(rep.one_or_more(relib.ANY_CHAR)) +
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.ANY_CHAR) +
        rep.maybe(relib.INTEGER)
    )
    four_atom_line = three_atom_line + (
        rep.one_or_more(relib.WHITESPACE) +
        rep.maybe(rep.one_or_more(relib.ANY_CHAR)) +
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.ANY_CHAR) +
        rep.maybe(relib.INTEGER)
    )

    init_z_matrix_pattern = (
        rep.capturing(
            rep.one_of_these(
                [one_atom_line, two_atom_line, three_atom_line, four_atom_line]
            )
        )
    )

    print('\n\nZMATRIX\n\n\n')

    # Obtain the Z-matrix from the text block
    init_z_matrix = repar.pattern_parser_2(
        init_z_matrix_pattern, init_z_matrix_block)

    # Initial internal coords defs
    init_coord_begin_pattern = 'ZUNIT=' + rep.one_or_more(relib.UPPERCASE_LETTER)
    init_coord_end_pattern = 'Geometry written to block  1 of record 700'

    # Get the text block containing the internal coord defs
    init_internal_coord_block = repar.block(
        init_coord_begin_pattern,
        init_coord_end_pattern,
        output_string)

    # Pattern for the each of the internal coordinates
    init_internal_coord_pattern = (
        'SETTING' +
        rep.capturing(
            rep.one_or_more(relib.ANY_CHAR) +
            rep.maybe(rep.one_or_more(relib.INTEGER)) +
            rep.one_or_more(relib.WHITESPACE) +
            '=' +
            rep.one_or_more(relib.WHITESPACE) +
            relib.FLOAT
        )
    )

    # Obtain the Z-matrix from the text block
    init_coord_internal = repar.pattern_parser_2(
        init_internal_coord_pattern, init_internal_coord_block)

    print('\n\nCOORDS\n\n\n')

    # Put the Z-matrix and internal coordinates together
    init_geom_internal = init_z_matrix + init_coord_internal

    return init_geom_internal


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
        'GHz' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('(calculated with average atomic masses)')
    )

    # Obtain equil_const string
    all_rot_consts = repar.pattern_parser_list_single_str(equil_rot_const_pattern, output_string)

    # Remove any instances of 0.0000s as well as duplicates
    rot_const_ghz = tuple((const for const in all_rot_consts if const != 0.0))

    # Convert from GHz to cm-1
    equil_rot_const = tuple((const * phys_constants.GHZ_TO_CM
                             for const in rot_const_ghz))

    return equil_rot_const
