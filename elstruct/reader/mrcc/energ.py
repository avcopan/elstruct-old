"""
Library of functions to retrieve electronic energies from a MRCC 2018 output file.

Energies currently supported:

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read the electronic energy #####

def hf_reader(output_string):
    """ Retrieves the RHF, UHF, or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the RHF energy
    hf_pattern = (
        '***FINAL HARTREE-FOCK ENERGY:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
        rep.one_or_more(relib.WHITESPACE) +
        '[AU]'
    )

    rohf_pattern_2 = (
    '***SEMICANONICAL ROHF ENERGY:' +
    rep.one_or_more(relib.WHITESPACE) +
    rep.one_or_more(relib.FLOAT)
    rep.one_or_more(relib.WHITESPACE) +
    '[AU]'
    )

    # Obtain the RHF energy
    hf_energy = pattern_reader(hf_pattern, output_string)

    return hf_energy

def rhf_mp2_reader(output_string):
    """ Retrieves the RHF, UHF, or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    rhf_mp2_pattern1 = (
        'MP2 energy [au]:'
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    rhf_mp2_pattern2 = (
        'Total MP2 energy [au]:'
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    return mp2_energy

def rhf_ccsd_reader(output_string):
    """ Retrieves the RHF, UHF, or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    rhf_ccsd_pattern = (
    'Total CCSD energy [au]:'
    rep.one_or_more(relib.WHITESPACE) +
    rep.one_or_more(relib.FLOAT)
    )

    return ccsd_energy

def rhf_ccsd_t_reader(output_string):
    """ Retrieves the RHF, UHF, or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    rhf_ccsd_t_pattern = (
        'CCSD(T) total energy [au]:'
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    return ccsd_t_energy

def rhf_ccsdt_reader(output_string):
    """ Retrieves the RHF, UHF, or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    rhf_ccsdt_pattern = (
        'Total CCSDT energy [au]:'
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    return ccsdt_energy

def rhf_ccsdt_q_reader(output_string):
    """ Retrieves the RHF, UHF, or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    rhf_ccsdt_q_pattern = (
        'Total CCSDT(Q) energy [au]:'
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    return ccsdt_q_energy


##### Dictionary of functions to read the energies in the files #####

ENERGY_READERS = {
    params.METHOD.RHF: hf_reader,
    params.METHOD.ROHF: hf_reader,
    params.METHOD.UHF: hf_reader,
}
