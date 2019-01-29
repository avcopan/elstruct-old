"""
Library of functions to retrieve electronic energies
from a Gaussian 09e output file.

Energies currently supported:
(1) RHF, ROHF, and UHF
(2) RHF, ROHF, and UHF reference
    MP2, UMP2, RMP2, CCSD, UCCSD, RCCSD, CCSD(T), UCCSD(T), RCCSD(T)
(3) Custom, User-Defined Energies

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


# Series of functions to read the electronic energy

def rhf_reader(output_string):
    """ Retrieves the RHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the RHF energy
    rhf_pattern1 = (
        'SCF Done:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('E(RHF) =') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'A.U. after' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.INTEGER +
        'cycles'
    )

    rhf_pattern2 = '\\\\HF=' + rep.capturing(relib.FLOAT)

    # Obtain the RHF energy
    rhf_energy = repar.energy_pattern_parser(rhf_pattern1, output_string)
    if rhf_energy is None:
        rhf_energy = repar.energy_pattern_parser(rhf_pattern2, output_string)

    return rhf_energy


def uhf_reader(output_string):
    """ Retrieves the UHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the RHF energy
    uhf_pattern1 = (
        'SCF Done:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('E(UHF) =') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'A.U. after' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.INTEGER +
        'cycles'
    )

    uhf_pattern2 = '\\\\HF=' + rep.capturing(relib.FLOAT)

    # Obtain the RHF energy
    uhf_energy = repar.energy_pattern_parser(uhf_pattern1, output_string)
    if uhf_energy is None:
        uhf_energy = repar.energy_pattern_parser(uhf_pattern2, output_string)

    return uhf_energy


def rohf_reader(output_string):
    """ Retrieves the ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the RHF energy
    rohf_pattern1 = (
        'SCF Done:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('E(ROHF) =') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'A.U. after' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.INTEGER +
        'cycles'
    )

    rohf_pattern2 = '\\\\HF=' + rep.capturing(relib.FLOAT)

    # Obtain the RHF energy
    rohf_energy = repar.energy_pattern_parser(rohf_pattern1, output_string)
    if rohf_energy is None:
        rohf_energy = repar.energy_pattern_parser(rohf_pattern2, output_string)

    return rohf_energy


def mp2_reader(output_string):
    """ Retrieves the RHF_MP2, ROHF_MP2, UHF_MP2 energy.
        Returns as a float. Units of Hartrees.
    """

    mp2_pattern1 = (
        'E2 =' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.EXPONENTIAL_FLOAT_D +
        relib.WHITESPACE +
        'EUMP2 =' +
        rep.capturing(relib.EXPONENTIAL_FLOAT_D)
    )

    mp2_pattern2 = '\\\\MP2=' + rep.capturing(relib.FLOAT)

    # Obtain the RHF_MP2 or RHF-UMP2 energy
    mp2_energy = repar.energy_pattern_parser(mp2_pattern1, output_string)
    if mp2_energy is None:
        mp2_energy = repar.energy_pattern_parser(mp2_pattern2, output_string)

    return mp2_energy


def ccsd_reader(output_string):
    """ Retrieves the RHF_CCSD, ROHF_CCSD, UHF_CCSD energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_pattern1 = (
        'DE(Corr)=' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        'E(CORR)=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'Delta=' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.EXPONENTIAL_FLOAT_D
    )

    ccsd_pattern2 = '\\\\CCSD=' + rep.capturing(relib.FLOAT)

    # Obtain the RHF_MP2, UHF_MP2, ROHF_MP2 energy
    ccsd_energy = repar.energy_pattern_parser(ccsd_pattern1, output_string)
    if ccsd_energy is None:
        ccsd_energy = repar.energy_pattern_parser(ccsd_pattern2, output_string)

    return ccsd_energy


def ccsd_t_reader(output_string):
    """ Retrieves the RHF_CCSD, ROHF_CCSD, UHF_CCSD energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_t_pattern1 = (
        'CCSD(T)= ' +
        rep.capturing(relib.EXPONENTIAL_FLOAT_D)
    )

    ccsd_t_pattern2 = rep.escape('\\\\CCSD(T)=') + rep.capturing(relib.FLOAT)

    # Obtain the RHF_CCSD(T), UHF_CCSD(T), ROHF_CCSD(T) energy
    ccsd_t_energy = repar.energy_pattern_parser(ccsd_t_pattern1, output_string)
    if ccsd_t_energy is None:
        ccsd_t_energy = repar.energy_pattern_parser(ccsd_t_pattern2, output_string)

    return ccsd_t_energy


def dft_reader(output_string):
    """ Reads from (hopefully) any DFT functional.
    """

    # patterns
    dbl_hybrid_func_pattern = (
        'E2(' +
        rep.one_or_more(relib.NONWHITESPACE) +
        ') =' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.EXPONENTIAL_FLOAT_D +
        relib.WHITESPACE +
        'E(' +
        rep.one_or_more(relib.NONWHITESPACE) +
        ') =' +
        rep.capturing(relib.EXPONENTIAL_FLOAT_D)
    )

    other_func_pattern = (
        'SCF Done:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.escape('E(') + 
        rep.one_or_more(relib.NONWHITESPACE) +
        rep.escape(') =') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'A.U. after' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.INTEGER +
        'cycles'
    )

    # Check if it is a double hybrid functional, if so read that
    dft_energy = repar.energy_pattern_parser(dbl_hybrid_func_pattern, output_string)
    if dft_energy is None:
        dft_energy = repar.energy_pattern_parser(other_func_pattern, output_string)

    return dft_energy


# Dictionary of functions to read the energies in the files

ENERGY_READERS = {
    params.METHOD.RHF: rhf_reader,
    params.METHOD.RHF_MP2: mp2_reader,
    params.METHOD.RHF_CCSD: ccsd_reader,
    params.METHOD.RHF_CCSD_T: ccsd_t_reader,
    params.METHOD.UHF: rhf_reader,
    params.METHOD.UHF_MP2: mp2_reader,
    params.METHOD.UHF_CCSD: ccsd_reader,
    params.METHOD.UHF_CCSD_T: ccsd_t_reader,
    params.METHOD.ROHF: rhf_reader,
    params.METHOD.ROHF_MP2: mp2_reader,
    params.METHOD.ROHF_CCSD: ccsd_reader,
    params.METHOD.ROHF_CCSD_T: ccsd_t_reader,
    # params.METHOD.DFT: dft_reader,
}
