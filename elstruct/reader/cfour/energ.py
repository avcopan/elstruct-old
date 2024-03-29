"""
Library of functions to retrieve electronic energies
from a CFour 2.0 output file.

Energies currently supported:
(1) RHF, UHF, and ROHF
(2) RHF, UHF, ROHF based MP2, CCSD. CCSD(T)

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

    # Set the string pattern to find the RHF/UHF energy
    rhf_uhf_pattern = (
        'E(SCF)=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        'D' +
        rep.one_or_more(relib.INTEGER)
    )

    # Obtain the RHF or UHF energy
    rhf_energy = repar.energy_pattern_parser(rhf_uhf_pattern, output_string)

    return rhf_energy


def rohf_reader(output_string):
    """ Retrieves the ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the UHF energy
    rohf_pattern = (
        'E(ROHF)=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        'D' +
        rep.one_or_more(relib.INTEGER)
    )

    # Obtain the ROHF energy
    rohf_energy = repar.energy_pattern_parser(rohf_pattern, output_string)

    return rohf_energy


def mp2_reader(output_string):
    """ Retrieves the RHF-MP2 or UHF-MP2 energy.
        Returns as a float. Units of Hartrees.
    """

    mp2_pattern = (
        'MP2 energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the MP2 energy
    mp2_energy = repar.energy_pattern_parser(mp2_pattern, output_string)

    return mp2_energy


def ccsd_reader(output_string):
    """ Retrieves the RHF-CCSD or UHF-CCSD energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_pattern = (
        'CCSD energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    # Obtain the CCSD energy
    ccsd_energy = repar.energy_pattern_parser(ccsd_pattern, output_string)

    return ccsd_energy


def ccsd_t_reader(output_string):
    """ Retrieves the RHF-CCSD(T) or UHF-CCSD(T) energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_t_pattern = (
        rep.escape('CCSD(T) energy') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
    )

    # Obtain the CCSD(T) energy
    ccsd_t_energy = repar.energy_pattern_parser(ccsd_t_pattern, output_string)

    return ccsd_t_energy


# Dictionary of functions to read the energies in the files

ENERGY_READERS = {
    params.METHOD.RHF: rhf_uhf_reader,
    params.METHOD.RHF_MP2: mp2_reader,
    params.METHOD.RHF_CCSD: ccsd_reader,
    params.METHOD.RHF_CCSD_T: ccsd_t_reader,
    params.METHOD.UHF: rhf_uhf_reader,
    params.METHOD.UHF_MP2: mp2_reader,
    params.METHOD.UHF_CCSD: ccsd_reader,
    params.METHOD.UHF_CCSD_T: ccsd_t_reader,
    params.METHOD.ROHF: rohf_reader,
    params.METHOD.ROHF_MP2: mp2_reader,
    params.METHOD.ROHF_CCSD: ccsd_reader,
    params.METHOD.ROHF_CCSD_T: ccsd_t_reader
}
