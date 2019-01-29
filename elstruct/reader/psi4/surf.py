"""
Library of functions to retrieve potential surface information
from a Psi4 1.0 output file.
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
    cart_hess_block_begin_pattern = 'Hessian (Symmetry '
    cart_hess_block_end_pattern = 'Psi4 stopped on:'

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
                rep.one_or_more(relib.FLOAT)
            )
        )
    )

    # Retrieve the Hessian
    cart_hess = repar.hessian_pattern_parser(cart_hess_pattern, cart_hess_block)

    return cart_hess
