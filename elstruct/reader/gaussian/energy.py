"""
Library of functions to retrieve electronic energies from a Gaussian 09e output file.

Energies currently supported:
(1) RHF, ROHF, and UHF
(2) RHF, ROHF, and UHF reference MP2, UMP2, RMP2, CCSD, UCCSD, RCCSD, CCSD(T), UCCSD(T), RCCSD(T)
(3) Custom, User-Defined Energies

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read the electronic energy #####


##### Dictionary of functions to read the energies in the files #####

ENERGY_READERS = {
}
#def gaussian_energy(lines,method=''):
#
#    if method == '':
#        method = gaussian_method(lines)
#    if 'CCSD' in method or 'MP' in method:
#        method = method.replace('(','\(').replace(')','\)')
#    #    energ  = method + '=([u,U,r,R]*[\w,\.,\s,-,D,\+]*)'
#        energ  = method + '=([u,U,r,R]*[\w,\.,\s,-]*)'
#        energ  = re.findall(energ,lines.replace('\n','').replace(' ',''))
#    #    return (method,float(energ[-1].replace('D','E').replace('\n','').replace(' ','')))
#        return (method,float(energ[-1].replace('\n','').replace(' ','')))
#    else:
#        lines = lines.strip().replace('\n','').replace(' ','')
#        if 'anharm' in lines:
#            energ = 'MP2=\s*([\d,\-,\.,D,\+]*)'
#            energ = re.findall(energ,lines)
#            if energ:
#                return (method, float(energ[-1].replace('D','E')))
#            else:
#                energ = 'HF=\s*([\d,\-,\.,D,\+]*)'
#                energ = re.findall(energ,lines)
#                return (method, float(energ[-1].replace('D','E')))
#       # energ = '(\S+)\s*A\.U\.'
#        energ = 'E\([u,U,r,R]*' + method + '\)\s*=\s*([\d,\-,\.,D,\+]*)'
#        energ = re.findall(energ,lines)
#        return (method, float(energ[-1].replace('D','E')))
#    return 
#
