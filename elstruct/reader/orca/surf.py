"""
Library of functions to retrieve potential surface information from a Orca 4.0 output file.
"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read the frequency information #####

# I think it is XYZ? also hessian is in .hess (although maybe print options can put it in output file)
HESS_XYZ_BEGIN = '$hessian'
HESS_XYZ_END = '$vibrational_frequencies'
# internla coord grad in output file (in some units
GRAD_INT_BEGIN = 'Definition                    Value    dE/dq     Step     New-Value'
GRAD_INT_END = '*********************'

##### Dictionary of functions to read frequency information in the files #####

SURFACE_READERS = {
}
