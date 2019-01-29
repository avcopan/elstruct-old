"""
Library of functions to retrieve potential surface information
from a Molpro 2015 output file.
"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib


# Series of functions to read the frequency information

def cartesian_hessian_reader(output_string):
    """ gets the xyz hessian
    """

    # Patterns to identify text block where Hessian is located
    cart_hess_block_begin_pattern = 'Force Constants (Second Derivatives of the Energy) in [a.u.]'
    cart_hess_block_end_pattern = 'Atomic Masses'

    # Obtain text block of containing the Hessian
    cart_hess_block = repar.block(cart_hess_block_begin_pattern,
                                  cart_hess_block_end_pattern,
                                  output_string)

    # Hessian Line Pattern: AXN  FLOAT  FLOAT  ...  NEWLINE
    cart_hess_pattern = (
        rep.capturing(
            relib.UPPERCASE_LETTER +
            rep.one_of_these(['X', 'Y', 'Z']) +
            relib.INTEGER +
            rep.one_or_more(
                rep.one_or_more(relib.WHITESPACE) +
                rep.one_or_more(relib.FLOAT)
            )
        )
    )

    # Retrieve the Hessian
    cart_hess = repar.hessian_pattern_parser(cart_hess_pattern, cart_hess_block)

    return cart_hess


def cartesian_gradient_reader(output_string):
    """ Reads the Cartesian gradient
    """

    # GET ATOM SYMBOLS FOR GEOMETRY CHANGES #
    
    # FIRST PATTERN FOR THE GRADIENT #

    # Patterns to identify text block where gradient is located
    cart_grad_block_begin_pattern = (
        'Atom' +
        rep.one_or_more(relib.WHITESPACE) +
        'dE/dx' +
        rep.one_or_more(relib.WHITESPACE) +
        'dE/dy' +
        rep.one_or_more(relib.WHITESPACE) +
        'dE/dz' +
        rep.one_or_more(relib.WHITESPACE) +
        'd2E/dx2' +
        rep.one_or_more(relib.WHITESPACE) +
        'd2E/dy2' +
        rep.one_or_more(relib.WHITESPACE) +
        'd2E/dz2'
    )
    cart_grad_block_end_pattern = 'wavefunction'

    # Obtain text block of containing the optimized geometry in xyz coordinates
    cart_grad_block = repar.block(cart_grad_block_begin_pattern,
                                  cart_grad_block_end_pattern,
                                  output_string)


    # PATTERN: INTEGER   FLOAT   FLOAT   FLOAT   FLOAT   FLOAT   FLOAT
    cart_grad_pattern = (
        rep.capturing(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT
    )

    # SECOND PATTERN FOR THE GRADIENT #

    # PATTERN: 'GXN / STRING'   FLOAT   FLOAT   FLOAT    FLOAT   FLOAT
    cart_grad_pattern_2 = (
        relib.UPPERCASE_LETTER +
        relib.UPPERCASE_LETTER +
        relib.INTEGER +
        relib.WHITESPACE +
        '/' +
        relib.WHITESPACE +
        rep.one_or_more(relib.UPPERCASE_LETTER) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT
    )

    # RETRIEVE THE GRADIENT #
    
    cart_grad = repar.pattern_parser_cartesian_geometry(
        cart_grad_pattern, cart_grad_block)
    if cart_grad is None:
        cart_grad = repar.pattern_parser_2(
            cart_grad_pattern_2, output_string)
        # turn it into a cartesian block

    gradient = 0.0

    return gradient
