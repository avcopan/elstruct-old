"""
Library of functions to retrieve potential surface information
from a Gaussian 09e output file.
"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib


# Series of functions to read the surface information

def cartesian_hessian_reader(output_string):
    """ gets the xyz hessian
    """

    # FIRST PATTERN FOR THE HESSIAN #

    # Patterns to identify text block where Hessian is located
    hess_block_begin_pattern = 'Force constants in Cartesian coordinates'
    hess_block_end_pattern = 'FCInt: Cartesian first derivatives'

    # Obtain text block of containing the Hessian
    hess_block = repar.block(hess_block_begin_pattern,
                             hess_block_end_pattern,
                             output_string)

    # Hessian Line Pattern: INTEGER  EXP_D  EXP_D  ...  NEWLINE
    hess_pattern = (
        rep.capturing(
            relib.INTEGER +
            rep.one_or_more(relib.WHITESPACE) +
            rep.one_or_more(relib.EXPONENTIAL_FLOAT_D)
        )
    )

    # SECOND PATTERN FOR THE HESSIAN #

    # Pattern to identify text block where Hessian is located
    hess_block_begin_pattern_2 = 'The second derivative matrix'
    hess_block_end_pattern_2 = 'ITU=  0'

    # Obtain text block containing the Hessian
    hess_block_2 = repar.block(hess_block_begin_pattern_2,
                               hess_block_end_pattern_2,
                               output_string)

    # Hessian Line Pattern: AAA  FLOAT  FLOAT  ...  NEWLINE
    hess_pattern_2 = (
        rep.capturing(
            rep.one_or_more(relib.NONWHITESPACE) +
            rep.one_or_more(
                rep.one_or_more(relib.WHITESPACE) +
                relib.FLOAT
            )
        )
    )

    # RETRIEVE THE HESSIAN #

    if hess_block is not None:
        hess_xyz = repar.hessian_pattern_parser(hess_pattern, hess_block)
    else:
        hess_xyz = repar.hessian_pattern_parser(hess_pattern_2, hess_block_2)

    return hess_xyz


def internal_hessian_reader(output_string):
    """ gets the int hessian
    """

    # FIRST PATTERN FOR THE HESSIAN #

    # Patterns to identify text block where Hessian is located
    hess_block_begin_pattern = 'Force constants in internal coordinates'
    hess_block_end_pattern = 'FCInt: Cartesian first derivatives'

    # Obtain text block of containing the Hessian
    hess_block = repar.block(hess_block_begin_pattern,
                             hess_block_end_pattern,
                             output_string)

    # Hessian Line Pattern: INTEGER  EXP_D  EXP_D  ...  NEWLINE
    hess_pattern = (
        rep.capturing(
            relib.INTEGER +
            rep.one_or_more(relib.WHITESPACE) +
            rep.one_or_more(relib.EXPONENTIAL_FLOAT_D)
        )
    )

    # SECOND PATTERN FOR THE HESSIAN #

    # Patterns to identify text block where Hessian is located
    hess_block_begin_pattern_2 = 'The second derivative matrix'
    hess_block_end_pattern_2 = 'ITU=  0'

    # Obtain text block of containing the Hessian
    hess_block_2 = repar.block(hess_block_begin_pattern_2,
                               hess_block_end_pattern_2,
                               output_string)

    # Hessian Line Pattern: AAA  FLOAT  FLOAT  ...  NEWLINE
    hess_pattern_2 = (
        rep.capturing(
            rep.one_or_more(relib.NONWHITESPACE) +
            rep.one_or_more(
                rep.one_or_more(relib.WHITESPACE) +
                relib.FLOAT
            )
        )
    )

    # RETRIEVE THE HESSIAN  #

    if hess_block is not None:
        hess_int = repar.hessian_pattern_parser(hess_pattern, hess_block)
    else:
        hess_int = repar.hessian_pattern_parser(hess_pattern_2, hess_block_2)

    return hess_int


def cartesian_gradient_reader(output_string):
    """ grabs the gradient in xyz coord
    """

    # FIRST PATTERN FOR THE GRADIENT #

    # Patterns to identify text block where gradient is located
    cart_grad_block_begin_pattern_1 = (
        'Center     Atomic                   Forces (Hartrees/Bohr)'
        #'Center' #+
        #rep.one_or_more(relib.WHITESPACE) +
        #'Atomic' +
        #rep.one_or_more(relib.WHITESPACE) +
        #'Forces (Hartrees/Bohr)'
    )
    cart_grad_block_end_pattern_1 = (
        'Cartesian Forces:' #  Max' +
        #rep.one_or_more(relib.WHITESPACE) +
        #relib.FLOAT +
        #'RMS' +
        #rep.one_or_more(relib.WHITESPACE) +
        #relib.FLOAT
    )

    # Obtain text block containing the gradient
    cart_grad_block_1 = repar.block(cart_grad_block_begin_pattern_1,
                                    cart_grad_block_end_pattern_1,
                                    output_string)

    # Gradient Line Pattern: INT  INT  FLOAT  FLOAT  FLOAT  NEWLINE
    cart_grad_pattern_1 = (
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
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
        'Variable       Old X    -DE/DX   Delta X   Delta X   Delta X     New X'
    )
    cart_grad_block_end_pattern_2 = (
        'Item' +
        rep.one_or_more(relib.WHITESPACE) +
        'Value' +
        rep.one_or_more(relib.WHITESPACE) +
        'Threshold' +
        rep.one_or_more(relib.WHITESPACE) +
        'Converged?'
    )

    # Obtain text block containing the gradient
    cart_grad_block_2 = (cart_grad_block_begin_pattern_2,
                         cart_grad_block_end_pattern_2,
                         output_string)
    
    # Gradient Line Pattern: INT  EXP_D  EXP_D  ...  NEWLINE
    cart_grad_pattern_2 = (
        rep.one_or_more(relib.NONWHITESPACE) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE + relib.FLOAT) 
    )

    # THIRD PATTERN FOR THE GRADIENT #

    # Patterns to identify text block where gradient is located
    cart_grad_block_begin_pattern_3 = 'FCINt: Cartesian first derivatives:'
    cart_grad_block_end_pattern_3 = 'FCInt: Cartesian force constants'

    # Obtain text block containing the gradient
    cart_grad_block_3 = (cart_grad_block_begin_pattern_3,
                         cart_grad_block_end_pattern_3,
                         output_string)
    
    # Gradient Line Pattern: INT  EXP_D  EXP_D  ...  NEWLINE
    cart_grad_pattern_3 = (
        rep.capturing(
            relib.INTEGER +
            rep.one_or_more(relib.WHITESPACE) +
            rep.one_or_more(relib.EXPONENTIAL_FLOAT_D)
        )
    )

    # RETRIEVE THE GRADIENT #
    
    cart_grad = repar.cartesian_gradient_pattern_parser(cart_grad_pattern_1, cart_grad_block_1)
    if cart_grad is None:
        cart_grad = repar.cartesian_gradient_pattern_parser(cart_grad_pattern_2, cart_grad_block_2)
        if cart_grad is None:
            cart_grad = repar.cartesian_gradient_pattern_parser(cart_grad_pattern_3, cart_grad_block_3)

    return cart_grad


def internal_gradient_reader(output_string):
    """ get the internal gradients
    """

    # Patterns to identify text block where gradient is located
    int_grad_block_begin_pattern = 'Internal Coordinate Forces (Hartree/Bohr or radian)'
    int_grad_block_end_pattern = (
        'Internal  Forces:  Max' + 
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT + 
        rep.one_or_more(relib.WHITESPACE) +
        'RMS' + 
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT 
    )   

    # Obtain text block containing the gradient
    int_grad_block = (int_grad_block_begin_pattern,
                      int_grad_block_end_pattern,
                      output_string)

    # Gradient Line Pattern: INT  LETTER  INT  FLOAT( )  INT  FLOAT()  INT  FLOAT()  0  NEWLINE
    int_grad_pattern = (
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

    return int_grad


def irc_geometries_reader(output_string):
    """ Grabs the geometries along the IRC
    """

    # Pattern to idetify text block of where the geometries are located
    irc_geom_block_begin_pattern = 'Point Number:'
    irc_geom_block_end_pattern = 'Distance matrix (angstroms):'


    # Obtain text block of containing the geometry
    irc_geom_blocks = repar.all_blocks(irc_geom_block_begin_pattern,
                                       irc_geom_block_end_pattern,
                                       output_string)
    
    # Geometry Pattern: INT  INT  INT  FLOAT  FLOAT  FLOAT  NEWLINE 
    irc_geom_pattern = (
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

    # Retrieve the geometries from the blocks
    irc_geoms = [repar.cartesian_geometry_pattern_parser(irc_geom_pattern, block)
                for block in irc_geom_blocks]


    return irc_geoms


def irc_cartesian_hessians_reader(output_string):
    """ Grabs the Hessians along the IRC
    """

    # Patterns to identify text block where Hessian is located
    irc_hess_block_begin_pattern = 'Force constants in Cartesian coordinates'
    irc_hess_block_end_pattern = 'FCInt: Cartesian first derivatives'

    # Obtain text block of containing the Hessian
    irc_hess_blocks = repar.all_blocks(hess_block_begin_pattern,
                                       hess_block_end_pattern,
                                       output_string)

    # Hessian Line Pattern: INTEGER  EXP_D  EXP_D  ...  NEWLINE
    irc_hess_pattern = (
        rep.capturing(
            relib.INTEGER +
            rep.one_or_more(relib.WHITESPACE) +
            rep.one_or_more(relib.EXPONENTIAL_FLOAT_D)
        )
    )
    
    # Retrieve the Hessians from the blocks
    irc_hess = [repar.hessian_pattern_parser(irc_hess_pattern, block)
                for block in irc_hess_blocks]

    return irc_hess


def irc_internal_hessians_reader(output_string):
    """ Grabs the Hessians along the IRC
    """

    # Patterns to identify text block where Hessian is located
    irc_hess_block_begin_pattern = 'Force constants in internal coordinates'
    irc_hess_block_end_pattern = 'Final forces over variables'

    # Obtain text block of containing the Hessian
    irc_hess_blocks = repar.all_blocks(hess_block_begin_pattern,
                                       hess_block_end_pattern,
                                       output_string)

    # Hessian Line Pattern: INTEGER  EXP_D  EXP_D  ...  NEWLINE
    irc_hess_pattern = (
        rep.capturing(
            relib.INTEGER +
            rep.one_or_more(relib.WHITESPACE) +
            rep.one_or_more(relib.EXPONENTIAL_FLOAT_D)
        )
    )
    
    # Retrieve the Hessians from the blocks
    irc_hess = [repar.hessian_pattern_parser(irc_hess_pattern, block)
                for block in irc_hess_blocks]

    return irc_hess


def irc_cartesian_gradients_reader(output_string):
    """ Grabs the gradients along the IRC
    """
    
    # Patterns to identify text block where gradient is located
    irc_grad_block_begin_pattern = 'FCINt: Cartesian first derivatives:'
    irc_grad_block_end_pattern = 'FCInt: Cartesian force constants'

    # Obtain text block containing the gradient
    irc_grad_block = (irc_grad_block_begin_pattern,
                       irc_grad_block_end_pattern,
                       output_string)
    
    # Gradient Line Pattern: INT  EXP_D  EXP_D  ...  NEWLINE
    irc_grad_pattern = (
        rep.capturing(
            relib.INTEGER +
            rep.one_or_more(relib.WHITESPACE) +
            rep.one_or_more(relib.EXPONENTIAL_FLOAT_D)
        )
    )


    return irc_grads


def irc_internal_grads_reader(output_string):
    """ Grabs the gradients along the IRC
    """

    # Patterns to identify text block where gradient is located
    irc_grad_block_begin_pattern = 'Final forces over variables, Energy='
    irc_grad_block_end_pattern = 'IRC-IRC-IRC'

    # Obtain text block containing the gradient
    irc_grad_block = repar.all_blocks(irc_grad_block_begin_pattern,
                                      irc_grad_block_end_pattern,
                                      output_string)

    # Gradient Line Pattern: INT  EXP_D  EXP_D  ...  NEWLINE
    pattern

    return irc_grads


def irc_reaction_path_reader(output_string):
    """ Grabs the energy and coordinate along the minimum-energy path
        from an IRC run.
    """

    # Patterns to identify text block where rxn path is located
    rxn_path_block_begin_pattern = 'Summary of reaction path following'
    rxn_path_block_end_pattern = 'Total number of Hessian calculations'

    # Obtain text block containing the rxn path 
    rxn_path_block = repar.block(rxn_path_block_begin_pattern,
                                 rxn_path_block_end_pattern,
                                 output_string)

    return rxn_path_block
