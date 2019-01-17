"""
Library of functions to retrieve potential surface information from a Gaussian 09e output file.
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
#def gaussian_hessian(lines):
#    startkey = 'Force constants in Cartesian coordinates:'
#    endkey   = 'Force constants in internal coordinates:'
#    key2 = 'Leave Link'
#    lines= lines.split('Harmonic vibro-rotational analysis')[-1]
#    lines = lines.splitlines()
#    sline = io.get_line_number(startkey,lines=lines)
#    eline = io.get_line_number(endkey,lines=lines)
#    if sline < 0:
#        return ''
#    hess   = '\n'.join(lines[sline+1:eline]).replace('D','E')
#    hess   = hess.split(key2)[0]
#    return hess
#
