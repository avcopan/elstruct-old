"""
Library of functions to retrieve electronic energies
from a MRCC 2018 output file.

Energies currently supported:

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


# Series of functions to read the electronic energy

def rhf_uhf_reader(output_string):
    """ Retrieves the RHF or UHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the RHF energy
    hf_pattern = (
        '***FINAL HARTREE-FOCK ENERGY:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('[AU]')
    )

    # Obtain the RHF/UHF energy
    hf_energy = repar.pattern_parser_single_float(hf_pattern, output_string)

    return hf_energy


def rohf_reader(output_string):
    """ Retrieves the ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the ROHF energy
    rohf_pattern = (
        '***FINAL HARTREE-FOCK ENERGY:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('[AU]')
    )

    rohf_pattern_2 = (
        '***SEMICANONICAL ROHF ENERGY:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('[AU]')
    )

    # Obtain the ROHF energy
    rohf_energy = repar.pattern_parser_single_float(rohf_pattern, output_string)
    if rohf_energy is None:
        rohf_energy = repar.pattern_parser_single_float(rohf_pattern_2, output_string)

    return rohf_energy


def mp2_reader(output_string):
    """ Retrieves the MP2 energy.
        Returns as a float. Units of Hartrees.
    """

    mp2_pattern = (
        rep.escape('MP2 energy [au]:') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    mp2_pattern_2 = (
        rep.escape('Total MP2 energy [au]:') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    # Obtain the RHF-MP2 energy
    mp2_energy = repar.pattern_parser_single_float(mp2_pattern, output_string)
    if mp2_energy is None:
        mp2_energy = repar.pattern_parser_single_float(mp2_pattern_2, output_string)

    return mp2_energy


def ccsd_reader(output_string):
    """ Retrieves the CCSD energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_pattern = (
        rep.escape('Total CCSD energy [au]:') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    # Obtain the CCSD energy
    ccsd_energy = repar.pattern_parser_single_float(ccsd_pattern, output_string)

    return ccsd_energy


def ccsd_t_reader(output_string):
    """ Retrieves the CCSD(T) energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_t_pattern = (
        rep.escape('CCSD(T) total energy [au]:') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    # Obtain the CCSD(T) energy
    ccsd_t_energy = repar.pattern_parser_single_float(ccsd_t_pattern, output_string)

    return ccsd_t_energy


def ccsdt_reader(output_string):
    """ Retrieves the CCSDT energy.
        Returns as a float. Units of Hartrees.
    """

    ccsdt_pattern = (
        rep.escape('Total CCSDT energy [au]:') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    # Obtain the CCSDT(Q) energy
    ccsdt_energy = repar.pattern_parser_single_float(ccsdt_pattern, output_string)

    return ccsdt_energy


def ccsdt_q_reader(output_string):
    """ Retrieves the CCSDT(Q) energy.
        Returns as a float. Units of Hartrees.
    """

    ccsdt_q_pattern = (
        rep.escape('Total CCSDT(Q) energy [au]:') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    # Obtain the CCSDT(Q) energy
    ccsdt_q_energy = repar.pattern_parser_single_float(ccsdt_q_pattern, output_string)

    return ccsdt_q_energy


# Dictionary of functions to read the energies in the file

ENERGY_READERS = {
    params.METHOD.RHF: rhf_uhf_reader,
    params.METHOD.UHF: rhf_uhf_reader,
    params.METHOD.ROHF: rohf_reader,
    params.METHOD.RHF_MP2: mp2_reader,
    params.METHOD.RHF_CCSD: ccsd_reader,
    params.METHOD.RHF_CCSD_T: ccsd_t_reader,
    params.METHOD.RHF_CCSDT: ccsdt_reader,
    params.METHOD.RHF_CCSDT_Q: ccsdt_q_reader,
}
