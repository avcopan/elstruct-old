"""
Library of functions to retrieve molecular properties from a CFour 2.0 output file.

Properties currently supported:
(1) Dipole Moment

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read molecular properties #####

def dipole_moment_reader(output_string):
    """ Reads the Permanent Dipole moment from the output file.
        Returns the constants as a list of strings; in Debye.
    """
    
    # scf
    dipole_mom_pattern = (
        '@DRVPRP-I, Properties computed from the SCF density matrix follow.' +
        'Components of electric dipole moment' +
        'X =' +    
        rep.one_or_more(relib.WHITESPACE) +
        rep.caturing(relib.FLOAT) +
        'Y =' +    
        rep.one_or_more(relib.WHITESPACE) +
        rep.caturing(relib.FLOAT) +
        'Z =' +    
        rep.one_or_more(relib.WHITESPACE) +
        rep.caturing(relib.FLOAT) 
    )

    # scf 2
    dip_block_begin = 'Total dipole moment'
    dip_block_begin = 'Conversion factor used: 1 a.u. =   2.54174691 Debye'

    dip_pattern = (
        relib.ANY_CHAR +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT 
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    ) 

    # correlated
    dipole_mom_pattern = (
        '@DRVPRP-I, Properties computed from the correlated density matrix follow.' +
        'Components of electric dipole moment' +
        'X =' +    
        rep.one_or_more(relib.WHITESPACE) +
        rep.caturing(relib.FLOAT) +
        'Y =' +    
        rep.one_or_more(relib.WHITESPACE) +
        rep.caturing(relib.FLOAT) +
        'Z =' +    
        rep.one_or_more(relib.WHITESPACE) +
        rep.caturing(relib.FLOAT) 
    )

    dipole_mom = repar.list_float(pattern, output_string)

    return dipole_mom

def polarizability_reader(output_string):
    """ Reads the polarizability.
    """

    return polarizability



##### Dictionary of functions to read molecular properties in the files #####

PROPERTY_READERS = {
    params.PROPERTY.DIPOLE_MOM : dipole_moment_reader
}
