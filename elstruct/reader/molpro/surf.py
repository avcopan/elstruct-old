"""
Library of functions to retrieve potential surface information
from a Molpro 2015 output file.
"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-30"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib


# Series of functions to read the frequency information

def cartesian_hessian_reader(output_string):
    """ gets the xyz hessian
    """

    # Patterns to identify text block where Hessian is located
    cart_hess_block_begin_pattern = (
        'Force Constants (Second Derivatives of the Energy) in [a.u.]')
    cart_hess_block_end_pattern = (
        'Atomic Masses')

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
    cart_hess = repar.hessian_pattern_parser(cart_hess_pattern,
                                             cart_hess_block)

    return cart_hess


def cartesian_gradient_reader(output_string):
    """ Reads the Cartesian gradient
    """

    # GET ATOM SYMBOLS FOR GEOMETRY CHANGES #

    # FIRST PATTERN FOR THE GRADIENT #

    # Patterns to identify text block where gradient is located
    cart_grad_block_begin_pattern_1 = (
        'Atom' #+
        #rep.one_or_more(relib.WHITESPACE) +
        #'dE/dx' 
        #rep.one_or_more(relib.WHITESPACE) +
        #'dE/dy' +
        #rep.one_or_more(relib.WHITESPACE) +
        #'dE/dz'
    )
    cart_grad_block_end_pattern_1 = (
        'Nuclear force contribution to virial'# =' 
        # rep.one_or_more(relib.WHITESPACE) +
        # relib.FLOAT
    )

    # Obtain text block of containing the optimized geometry in xyz coordinates
    cart_grad_block_1 = repar.block(cart_grad_block_begin_pattern_1,
                                    cart_grad_block_end_pattern_1,
                                    output_string)

    # PATTERN: INTEGER   FLOAT   FLOAT   FLOAT   FLOAT   FLOAT   FLOAT
    cart_grad_pattern_1 = (
        rep.capturing(relib.INTEGER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # SECOND PATTERN FOR THE GRADIENT #

    # Patterns to identify text block where gradient is located
    cart_grad_block_begin_pattern_2 = (
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
    cart_grad_block_end_pattern_2 = 'wavefunction'

    # Obtain text block of containing the optimized geometry in xyz coordinates
    cart_grad_block_2 = repar.block(cart_grad_block_begin_pattern_2,
                                    cart_grad_block_end_pattern_2,
                                    output_string)

    # PATTERN: INTEGER   FLOAT   FLOAT   FLOAT   FLOAT   FLOAT   FLOAT
    cart_grad_pattern_2 = (
        rep.capturing(relib.INTEGER) +
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

    # THIRD PATTERN FOR THE GRADIENT #

    # PATTERN: 'GXN / STRING'   FLOAT   FLOAT   FLOAT    FLOAT   FLOAT
    cart_grad_pattern_3 = (
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

    cart_grad = repar.cartesian_gradient_pattern_parser(
        cart_grad_pattern_1, cart_grad_block_1)
    if cart_grad is None:
        cart_grad = repar.cartesian_gradient_pattern_parser(
            cart_grad_pattern_2, cart_grad_block_2)
        if cart_grad is None:
            cart_grad = repar.cartesian_gradient_pattern_parser(
                cart_grad_pattern_3, output_string)

    return cart_grad
