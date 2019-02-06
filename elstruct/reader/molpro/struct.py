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
__updated__ = "2019-01-30"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ._zmat import first_zmatrix_string
from ._zmat import internal_coordinate_entries
from ._zmat import zmatrix_dummy_atom_support_indices
from ... import mol
from ... import phys_constants


# Series of functions to read structural information
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


def initial_internal_geometry_reader(output_string):
    """ Retrieves the initial geometry in internal coordinates.
        Units of Angstrom and degrees.
    """
    float_string_pattern = relib.STRING_START + relib.FLOAT + relib.STRING_END

    zmat_str = first_zmatrix_string(output_string)
    intco_entry_dct = internal_coordinate_entries(zmat_str)
    intco_value_dct = {}
    for intco_key, intco_entry in intco_entry_dct.items():
        if ref.has_match(float_string_pattern, intco_entry):
            value = float(intco_entry)
        else:
            value_pattern = (
                'SETTING' +
                rep.one_or_more(relib.NONNEWLINE_WHITESPACE) +
                intco_entry.upper() +
                rep.one_or_more(relib.NONNEWLINE_WHITESPACE) +
                '=' +
                rep.one_or_more(relib.NONNEWLINE_WHITESPACE) +
                rep.capturing(relib.FLOAT)
            )
            value_string = ref.first_capture(value_pattern, output_string)
            assert value_string is not None
            value = float(value_string)

        intco_value_dct[intco_key] = value

    return intco_value_dct


def optimized_internal_geometry_reader(output_string):
    """ Retrieves the optimized geometry in internal coordinates.
        Units of Angstrom and degrees.
    """
    init_int_geom_dct = initial_internal_geometry_reader(output_string)
    dummy_sidx_dct = zmatrix_dummy_atom_support_indices(output_string)

    # first we insert the dummy atoms into the cartesian geometry
    opt_cart_geom = optimized_cartesian_geometry_reader(output_string)
    atm_syms, atm_xyzs = map(list, zip(*opt_cart_geom))
    for dummy_idx, (sidx1, sidx2, sidx3) in sorted(dummy_sidx_dct.items()):
        sxyz1 = atm_xyzs[sidx1]
        sxyz2 = atm_xyzs[sidx2]
        sxyz3 = atm_xyzs[sidx3]
        dist = init_int_geom_dct[(dummy_idx, sidx1)]
        ang = (init_int_geom_dct[(dummy_idx, sidx1, sidx2)] *
               phys_constants.DEG_TO_RAD)
        tors = (init_int_geom_dct[(dummy_idx, sidx1, sidx2, sidx3)] *
                phys_constants.DEG_TO_RAD)
        xyz = mol.intco.cartesian_coordinates(
            dist, ang, tors, sxyz1, sxyz2, sxyz3)
        atm_syms.insert(dummy_idx, 'X')
        atm_xyzs.insert(dummy_idx, xyz)

    opt_cart_geom_with_dummies = tuple(zip(atm_syms, atm_xyzs))
    opt_int_geom_dct = mol.geom.internal_coordinates(opt_cart_geom_with_dummies,
                                                     init_int_geom_dct.keys())
    return opt_int_geom_dct
