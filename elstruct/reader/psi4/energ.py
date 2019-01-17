"""
Library of functions to retrieve electronic energies from a Molpro 2015 output file.

Energies currently supported:

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-16"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read the electronic energy #####

def rhf_reader(output_string):
    """ Retrieves the RHF energy.
        Returns as a float. Units of Hartrees.
    """
    # Set the string pattern to find the RHF energy
    rhf_pattern = (
        '@RHF Final Energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
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

    return uhf_energy

def rohf_reader(output_string):
    """ Retrieves the ROHF energy.
        Returns as a float. Units of Hartrees.
    """
    # Set the string pattern to find the RHF energy
    rohf_pattern = (
        '@ORHF Final Energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
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

    ccsd_pattern = (
        'Total CCSD energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    return ccsd_energy

def ccsd_t_reader(output_string):
    """ Retrieves the CCSD(T) energy with any HF reference. 
        Returns as a float. Units of Hartrees.
    """

    # Check if same in higer correlation
    ccsd_t_pattern = (
        '* CCSD(T) total energy' +
        rep.one_or_more(relib.WHITESPACE) +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    return ccsd_t_energy

##### Dictionary of functions to read the energies in the files #####

ENERGY_READERS = {
}
