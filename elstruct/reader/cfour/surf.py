"""
Library of functions to retrieve potential surface information from a CFOUR 2.0 output file.
"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read the frequency information #####


##### Dictionary of functions to read frequency information in the files #####

SURFACE_READERS = {
}
