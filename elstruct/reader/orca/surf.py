"""
Library of functions to retrieve potential surface information
from a Orca 4.0 output file.
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
    cart_hess_block_begin_pattern = '$hessian'
    cart_hess_block_end_pattern = '$vibrational_frequencies'

    # Obtain text block of containing the Hessian
    cart_hess_block = repar.block(cart_hess_block_begin_pattern,
                                  cart_hess_block_end_pattern,
                                  output_string)

    # Hessian Line Pattern: AXN  FLOAT  FLOAT  ...  NEWLINE
    cart_hess_pattern = (
        rep.capturing(
            relib.INTEGER +
            rep.one_or_more(
                rep.one_or_more(relib.WHITESPACE) +
                rep.one_or_more(relib.EXPONENTIAL_FLOAT)
            )
        )
    )

    # Retrieve the Hessian
    cart_hess = repar.hessian_pattern_parser(cart_hess_pattern,
                                             cart_hess_block)

    return cart_hess


def cartesian_gradient_reader(output_string):
    """ gets the xyz gradient
    """

    # Patterns to identify text block where Hessian is located
    cart_grad_block_begin_pattern = 'CARTESIAN GRADIENT'
    cart_grad_block_end_pattern = 'Difference to translation invariance'

    # Obtain text block of containing the Hessian
    cart_grad_block = repar.block(cart_grad_block_begin_pattern,
                                  cart_grad_block_end_pattern,
                                  output_string)

    # Hessian Line Pattern: INT : SYM  FLOAT  FLOAT  FLOAT  NEWLINE
    cart_grad_pattern = (
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(rep.one_or_more(relib.NONWHITESPACE)) +
        rep.one_or_more(relib.WHITESPACE) +
        ':' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Retrieve the Hessian
    cart_hess = repar.cartesian_gradient_pattern_parser(cart_grad_pattern,
                                                        cart_grad_block)

    return cart_hess
