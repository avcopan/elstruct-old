"""
Library of functions to retrieve molecular properties from a Molpro 2015 output file.

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
    # HF dipole moment
    rhf_dipole_mom = (
        'RHF STATE' + 
        relib.WHITESPACE +
        relib.FLOAT + 
        relib.WHITESPACE + 
        'Dipole Moment' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) 
    )

    rhf_2 = (
        'Dipole moment Hartree-Fock' +
        rep.one_or_more(relib.WHITESPACE) +
        ':'
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT 
    )

    # MP2 dipole moment
    mp2_dipole_mom = (
        'MP2 STATE' + 
        relib.WHITESPACE +
        relib.FLOAT + 
        relib.WHITESPACE + 
        'Dipole Moment' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) 
    )

    # CCSD dipole moment
    ccsd_dipole_mom = (
        'XCCSD Dipole moment total:' +
        rep.one_or_more(relib.WHITESPACE) +
        ':'
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT 
    )

    # QISD dipole moment
    qicsd_dipole_mom = (
        'QCISD STATE' + 
        relib.WHITESPACE +
        relib.FLOAT + 
        relib.WHITESPACE + 
        'Dipole Moment' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) 
    )

    # QISD dipole moment
    qicsd_t_dipole_mom = (
        'QCISD(T) STATE' + 
        relib.WHITESPACE +
        relib.FLOAT + 
        relib.WHITESPACE + 
        'Dipole Moment' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) 
    )



    dipole_mom = repar.list_float(pattern, dipole_mom_block)

    return dipole_mom

def polarizability_reader(output_string)
    """ Reads dipole polarizability. """

    scf_polar_block_begin = 'SCF polarizabilities' 
    scf_polar_block_end = 'Average' + rep.one_or_more(relib.WHITESPACE) + relib.FLOAT 
    mp2_polar_block_begin = 'MP2 polarizabilities' 
    mp2_polar_block_end = 'Average' + rep.one_or_more(relib.WHITESPACE) + relib.FLOAT 


    polar_pattern = (
        rep.capturing(
            'DM' +
            relib.UPPERCASE_LETTER+
            rep.one_or_more(relib.WHITESPACE) +
            rep.capturing(relib.FLOAT) 
            rep.one_or_more(relib.WHITESPACE) +
            rep.capturing(relib.FLOAT) 
            rep.one_or_more(relib.WHITESPACE) +
            rep.capturing(relib.FLOAT) 
        )
    )
    

    return polarizability


##### Dictionary of functions to read molecular properties in the files #####

PROPERTY_READERS = {
    params.PROPERTY.DIPOLE_MOM : dipole_moment_reader
}
