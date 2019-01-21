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

def gradient_xyz_reader(output_string):
    """ Reads the Cartesian gradient
    """

    # Get the atom symbols

    # Grab cartesian grad

    # Pattern to idetify text block of where Cartesian gradient is located
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

    # Grabs the cartesian grad other way

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

    # Obtain the Cartesian gradient
    cart_grad = repar.pattern_parser_cartesian_geometry(
        cart_grad_pattern, cart_grad_block)
    if cart_grad is None:
        cart_grad = repar.pattern_parser_2(
            cart_grad_pattern_2, output_string)
        # turn it into a cartesian block

    gradient = 0.0

    return gradient

# def hessian_xyz_reader(output_string):
#     """ Reads the unprojected Cartesian Hessian from the output file.
#         Returns the Hessian in a string; in UNITS
#         need: (1) Grabber only works if job is run without symmetry
#               (2) Convert Hessian to a full Hessian? or lower/upper Triangular?
#     """
#
#     hess_start_line = 'Force Constants (Second Derivatives of the Energy)'
#     hess_end_line = 'Atomic Masses'
#
#     # Isolate block of lines from output file containing the Hessian
#     start_line_num = io.get_line_number( HESS_START_LINE, lines=lines ) + 1
#     end_line_num   = io.get_line_number( HESS_END_LINE, lines=lines ) - 2
#     hess_lines = lines.split()[ start_line_num, end_line_num ]
#     if start_line < 0:
#         return ''
#     hess = ''
#
#     # Read the Hessian
#     if symmetry == False:
#
#         for line in lines[sline+1:eline-2]:
#             hessline = ''
#             for val in line.split():
#                 if 'G'  in val:
#                     if 'GX' in val:
#                         add = 1
#                         val = val.replace('GX', '')
#                     elif 'GY' in val:
#                         add = 2
#                         val = val.replace('GY', '')
#                     else:
#                         add = 3
#                         val = val.replace('GZ', '')
#                 val = str((int(val) - 1) * 3 + add)
#             hessline += '\t' +  val
#         hess +=  hessline + '\n'
#
#     else:
#
#      print('Put Code')
#
#     return hess
#
# def hessian_internal(output_string):
#
#     hess_pattern = (
#         relib.UPPERCASE_LETTER +
#         relib.UPPERCASE_LETTER +
#         relib.INTEGER +
#         relib.WHITESPACE +
#         '/' +
#         relib.WHITESPACE +
#         rep.one_or_more(relib.UPPERCASE_LETTER) +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT)
#     )
#
#
#     return hessian_internal
