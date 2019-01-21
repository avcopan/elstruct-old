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

def rhf_reader(output_string):
    """ Retrieves the RHF energy.
        Returns as a float. Units of Hartrees.
    """
    # Set the string pattern to find the RHF energy
    rhf_pattern = (
        '@RHF Final Energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    scf_pattern = (
        'SCF energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '(wfn)' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    scf_pattern_2 = (
        'Reference energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '(file' +
        relib.INTEGER +
        ')' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the RHF energy
    rhf_energy = repar.pattern_parser_single_float(rhf_pattern, output_string)
    if rhf_energy is None:
        rhf_energy = repar.pattern_parser_single_float(scf_pattern, output_string)
        if rhf_energy is None:
            rhf_energy = repar.pattern_parser_single_float(scf_pattern_2, output_string)

    return rhf_energy


def uhf_reader(output_string):
    """ Retrieves the UHF energy.
        Returns as a float. Units of Hartrees.
    """
    # Set the string pattern to find the RHF energy
    uhf_pattern = (
        '@UHF Final Energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    scf_pattern = (
        'SCF energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '(wfn)' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    scf_pattern_2 = (
        'Reference energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '(file' +
        relib.INTEGER +
        ')' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the UHF energy
    uhf_energy = repar.pattern_parser_single_float(uhf_pattern, output_string)
    if uhf_energy is None:
        uhf_energy = repar.pattern_parser_single_float(scf_pattern, output_string)
        if uhf_energy is None:
            uhf_energy = repar.pattern_parser_single_float(scf_pattern_2, output_string)

    return uhf_energy


def rohf_reader(output_string):
    """ Retrieves the ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the RHF energy
    rohf_pattern = (
        '@ROHF Final Energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    scf_pattern = (
        'SCF energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '(wfn)' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    scf_pattern_2 = (
        'Reference energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '(file' +
        relib.INTEGER +
        ')' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the ROHF energy
    rohf_energy = repar.pattern_parser_single_float(rohf_pattern, output_string)
    if rohf_energy is None:
        rohf_energy = repar.pattern_parser_single_float(scf_pattern, output_string)
        if rohf_energy is None:
            rohf_energy = repar.pattern_parser_single_float(scf_pattern_2, output_string)

    return rohf_energy


def dft_reader(output_string):
    """ Retrieves a DFT energy, regardless of the Kohn-Sham reference.
        Returns as a float. Units of Hartrees.
    """

    rks_pattern = (
        '@RKS Final Energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    uks_pattern = (
        '@UKS Final Energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    roks_pattern = (
        '@ROKS Final Energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    scf_pattern = (
        'SCF energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '(wfn)' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    scf_pattern_2 = (
        'Reference energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '(file' +
        relib.INTEGER +
        ')' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the DFT energy
    dft_energy = repar.pattern_parser_single_float(rks_pattern, output_string)
    if dft_energy is None:
        dft_energy = repar.pattern_parser_single_float(uks_pattern, output_string)
        if dft_energy is None:
            dft_energy = repar.pattern_parser_single_float(roks_pattern, output_string)
            if dft_energy is None:
                dft_energy = repar.pattern_parser_single_float(scf_pattern, output_string)
                if dft_energy is None:
                    dft_energy = repar.pattern_parser_single_float(scf_pattern_2, output_string)

    return dft_energy


def mp2_reader(output_string):
    """ Retrieves the MP2 energy with any HF reference.
        Returns as a float. Units of Hartrees.
    """

    # Check if same in higer correlation
    mp2_pattern = (
        '* MP2 total energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the MP2 energy
    mp2_energy = repar.pattern_parser_single_float(mp2_pattern, output_string)

    return mp2_energy


def ccsd_reader(output_string):
    """ Retrieves the CCSD energy with any HF reference.
        Returns as a float. Units of Hartrees.
    """

    # Check if same in higer correlation
    ccsd_pattern = (
        '* CCSD total energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    ccsd_pattern_2 = (
        'Total CCSD energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the CCSD energy
    ccsd_energy = repar.pattern_parser_single_float(ccsd_pattern, output_string)
    if ccsd_energy is None:
        ccsd_energy = repar.pattern_parser_single_float(ccsd_pattern_2, output_string)

    return ccsd_energy


def ccsd_t_reader(output_string):
    """ Retrieves the CCSD(T) energy with any HF reference.
        Returns as a float. Units of Hartrees.
    """

    # Check if same in higer correlation
    ccsd_t_pattern = (
        rep.escape('* CCSD(T) total energy') +
        rep.one_or_more(relib.WHITESPACE) +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the CCSD(T) energy
    ccsd_t_energy = repar.pattern_parser_single_float(ccsd_t_pattern, output_string)

    return ccsd_t_energy


# Dictionary of functions to read the energies in the files

ENERGY_READERS = {
    params.METHOD.RHF: rhf_reader,
    params.METHOD.UHF: uhf_reader,
    params.METHOD.ROHF: rohf_reader,
    # params.METHOD.DFT: dft_reader,
    # params.METHOD.RHF_MP2: mp2_reader,
    # params.METHOD.RHF_CCSD: ccsd_reader,
    # params.METHOD.RHF_CCSD_T: ccsd_t_reader,
}
