"""
Library of functions to retrieve electronic energies
from a Molpro 2015 output file.

Energies currently supported:

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


# Series of functions to read the electronic energy

def scf_reader(output_string):
    """ Retrieves the RHF, UHF, ROHF, or DFT energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the SCF energy
    scf_pattern = (
        'Total Energy' +
        rep.one_or_more(relib.WHITESPACE) +
        ':' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'Eh' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        'eV'
    )

    # Obtain the SCF energy
    scf_energy = repar.pattern_parser_single_float(scf_pattern, output_string)

    return scf_energy


def mp2_reader(output_string):
    """ Retrieves the MP2 energy.
        Returns as a float. Units of Hartrees.
    """

    mp2_pattern = (
        'MP2 TOTAL ENERGY:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'Eh'
    )

    # Obtain the MP2 energy
    mp2_energy = repar.pattern_parser_single_float(mp2_pattern, output_string)

    return mp2_energy


def ccsd_reader(output_string):
    """ Retrieves the CCSD energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_pattern = (
        rep.escape('E(TOT)') +
        rep.one_or_more(relib.WHITESPACE) +
        '...' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    ccsd_pattern_2 = (
        rep.escape('E(CCSD)') +
        rep.one_or_more(relib.WHITESPACE) +
        '...' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the CCSD energy
    ccsd_energy = repar.pattern_parser_single_float(ccsd_pattern, output_string)
    if ccsd_energy is None:
        ccsd_energy = repar.pattern_parser_single_float(ccsd_pattern_2, output_string)

    return ccsd_energy


def ccsd_t_reader(output_string):
    """ Retrieves the CCSD(T) energy energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_t_pattern = (
        rep.escape('E(CCSD(T))') +
        rep.one_or_more(relib.WHITESPACE) +
        '...' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the CCSD(T) energy
    ccsd_t_energy = repar.pattern_parser_single_float(ccsd_t_pattern, output_string)

    return ccsd_t_energy


# Dictionary of functions to read the energies in the files

ENERGY_READERS = {
    params.METHOD.RHF: scf_reader,
    params.METHOD.ROHF: scf_reader,
    params.METHOD.UHF: scf_reader,
    params.METHOD.RHF_MP2: mp2_reader,
    params.METHOD.RHF_CCSD: ccsd_reader,
    params.METHOD.RHF_CCSD_T: ccsd_t_reader,
}
# def general_e_reader(output_string):
#     """ Retrieves any energy: the initial, middle, and final
#         Returns as a float. Units of Hartrees.
#     """
#
#     general_e_pattern = (
#         'FINAL SINGLE POINT ENERGY' +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT)
#
#     )
#
#     return general_energy
