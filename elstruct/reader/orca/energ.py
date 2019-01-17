"""
Library of functions to retrieve electronic energies from a Molpro 2015 output file.

Energies currently supported:

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-11"

from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read the electronic energy #####

def general_e_reader(output_string):
    """ Retrieves any energy: the initial, middle, and final
        Returns as a float. Units of Hartrees.
    """

    general_e_pattern = (
        'FINAL SINGLE POINT ENERGY' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)

    )

    return general_energy

def scf_reader(output_string):
    """ Retrieves the RHF, UHF, or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the RHF energy
    scf_pattern = (
        'Total Energy' +
        rep.one_or_more(relib.WHITESPACE) +
        ':' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'Eh' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'eV'
    )

    return scf_energy

def rhf_mp2_reader(output_string):
    """ Retrieves the RHF, UHF, or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    rhf_mp2_pattern = (
        'MP2 TOTAL ENERGY:'
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'Eh'
    )

    return mp2_energy

def rhf_ccsd_reader(output_string):
    """ Retrieves the RHF, UHF, or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_pattern1 = (
        'E(TOT)' +
        rep.one_or_more(relib.WHITESPACE) +
        '...' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    ccsd_pattern2 = (
        'E(CCSD)' +
        rep.one_or_more(relib.WHITESPACE) +
        '...' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    return ccsd_energy

def rhf_ccsd_t_reader(output_string):
    """ Retrieves the RHF, UHF, or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_t_pattern = (
        'E(CCSD(T))' +
        rep.one_or_more(relib.WHITESPACE) +
        '...' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    return ccsdt_energy

ENERGY_READERS = {
    params.METHOD.RHF: hf_reader,
    params.METHOD.ROHF: hf_reader,
    params.METHOD.UHF: hf_reader,
}
