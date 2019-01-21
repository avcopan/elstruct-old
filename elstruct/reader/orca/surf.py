"""
Library of functions to retrieve potential surface information
from a Orca 4.0 output file.
"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"
#
# from ..rere import parse as repar
# from ..rere import find as ref
# from ..rere import pattern as rep
# from ..rere import pattern_lib as relib
# from ... import params
#
#
# ##### Series of functions to read the frequency information #####
#
# # think its XYZ? hessian is in .hess (maybe print opts put it in output file)
# HESS_XYZ_BEGIN = '$hessian'
# HESS_XYZ_END = '$vibrational_frequencies'
# # internla coord grad in output file (in some units
# GRAD_INT_BEGIN = ( 'Definition' +
#                    rep.one_or_more(relib.WHITESPACE) +
#                    'Value    dE/dq     Step     New-Value' +
#                  )
# GRAD_INT_END = '*********************'
#
# # Dictionary of functions to read frequency information in the files
#
# SURFACE_READERS = {
# }
