"""
Library of functions to retrieve electronic energies from a Molpro 2015 output file.

Energies currently supported:
(1) RHF, ROHF, and UHF
(2) RHF, ROHF, and UHF reference MP2, UMP2, RMP2, CCSD, UCCSD, RCCSD, CCSD(T), UCCSD(T), RCCSD(T)
(3) Custom, User-Defined Energies

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read the electronic energy #####

def rhf_reader(output_string):
    """ Retrieves the RHF or ROHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the RHF energy
    rhf_pattern = (
        '!RHF STATE' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'Energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the RHF energy
    rhf_energy = repar.sing_float(rhf_pattern, output_string)

    return rhf_energy

def uhf_reader(output_string):
    """ Retrieves the UHF energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the UHF energy
    uhf_pattern = (
        '!UHF STATE' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'Energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the UHF energy
    uhf_energy = repar.sing_float(uhf_pattern, output_string)

    return uhf_energy

def rhf_mp2_reader(output_string):
    """ Retrieves the RHF-MP2 or RHF-UMP2 energy.
        Returns as a float. Units of Hartrees.
    """

    mp2_pattern1 = (
        '!MP2 total energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    mp2_pattern2 = (
        'MP2 total energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    ump2_pattern = (
        '!RHF-UMP2 energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the RHF-MP2 or RHF-UMP2 energy
    mp2_energy = repar.sing_float(mp2_pattern1, output_string)
    if mp2_energy is None:
        mp2_energy = repar.sing_float(mp2_pattern2, output_string)
        if mp2_energy is None:
            mp2_energy = repar.sing_float(ump2_pattern, output_string)

    return mp2_energy

def uhf_ump2_reader(output_string):
    """ Retrieves the UHF-UMP2 energy.
        Returns as a float. Units of Hartrees.
    """

    ump2_pattern = (
        '!UMP2 STATE' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'Energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the UHF-MP2 energy
    ump2_energy = repar.sing_float(ump2_pattern, output_string)

    return ump2_energy

def rohf_rmp2_reader(output_string):
    """ Retrieves the ROHF-RMP2 energy.
        Returns as a float. Units of Hartrees.
    """

    # from single points
    rmp2_pattern1 = (
        '!RMP2 STATE' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        'Energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # from cc calcs
    rmp2_pattern2 = (
        '!RHF-RMP2 energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the ROHF-RMP2 energy
    rmp2_energy = repar.sing_float(rmp2_pattern1, output_string)
    if rmp2_energy is None:
        rmp2_energy = repar.sing_float(rmp2_pattern2, output_string)

    return rmp2_energy

def rhf_rohf_ccsd_uccsd_reader(output_string):
    """ Retrieves the RHF-CCSD, RHF-UCCSD, or ROHF-UCCSD energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_pattern1 = (
        '!CCSD total energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    ccsd_pattern2 = (
        'CCSD total energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    uccsd_pattern = (
        '!RHF-UCCSD energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the RHF-CCSD, RHF-UCCSD, ROHF-UCCSD energy
    ccsd_energy = repar.sing_float(ccsd_pattern1, output_string)
    if ccsd_energy is None:
        ccsd_energy = repar.sing_float(ccsd_pattern2, output_string)
        if ccsd_energy is None:
            ccsd_energy = repar.sing_float(uccsd_pattern, output_string)

    return ccsd_energy

def rohf_rccsd_reader(output_string):
    """ Retrieves the ROHF-RCCSD energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_pattern = (
        'CCSD total energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    rccsd_pattern = (
        '!RHF-RCCSD energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the ROHF-RCCSD energy
    ccsd_energy = repar.sing_float(ccsd_pattern, output_string)
    if ccsd_energy is None:
        ccsd_energy = repar.sing_float(rccsd_pattern, output_string)

    return ccsd_energy

def rhf_rohf_ccsd_t_uccsd_t_reader(output_string):
    """ Retrieves the RHF-CCSD(T), RHF-UCCSD(T), or ROHF-UCCSD(T) energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_t_pattern = (
        '!CCSD\(T\) total energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    uccsd_t_pattern = (
        '!RHF-UCCSD\(T\) energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the RHF-CCSD(T), RHF-UCCSD(T), or ROHF-UCCSD(T) energy
    ccsd_t_energy = repar.sing_float(ccsd_t_pattern, output_string)
    if ccsd_t_energy is None:
        ccsd_t_energy = repar.sing_float(uccsd_t_pattern, output_string)

    return ccsd_t_energy

def rohf_rccsd_t_reader(output_string):
    """ Retrieves the ROHF-RCCSD(T) energy.
        Returns as a float. Units of Hartrees.
    """

    ccsd_t_pattern = (
        'CCSD(T) total energy:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    rccsd_t_pattern = (
        '!RHF-RCCSD\(T\) energy' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the ROHF-RCCSD(T) energy
    ccsd_t_energy = repar.sing_float(ccsd_t_pattern, output_string)
    if ccsd_t_energy is None:
        ccsd_t_energy = repar.sing_float(rccsd_t_pattern, output_string)

    return ccsd_t_energy

def custom_e_reader(output_string):
    """ Retrieves the custom energy.
        Returns as a float. Units of Hartrees.
    """

    # Set the string pattern to find the RHF energy
    custom_e_pattern = (
        'SETTING E_' +
        rep.capturing(relib.WHITESPACE) +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the custom energy
    custom_energy = repar.sing_float(custom_e_pattern, output_string)

    return custom_energy


##### Dictionary of functions to read the energies in the files #####

ENERGY_READERS = {
    params.METHOD.RHF: rhf_reader,
    params.METHOD.ROHF: rhf_reader,
    params.METHOD.UHF: uhf_reader,
    params.METHOD.RHF_MP2: rhf_mp2_reader,
    params.METHOD.UHF_UMP2: uhf_ump2_reader,
    params.METHOD.ROHF_RMP2: rohf_rmp2_reader,
    params.METHOD.RHF_CCSD: rhf_rohf_ccsd_uccsd_reader,
    params.METHOD.ROHF_UCCSD: rhf_rohf_ccsd_uccsd_reader,
    params.METHOD.ROHF_RCCSD: rohf_rccsd_reader,
    params.METHOD.RHF_CCSD_T: rhf_rohf_ccsd_t_uccsd_t_reader,
    params.METHOD.ROHF_UCCSD_T: rhf_rohf_ccsd_t_uccsd_t_reader,
    params.METHOD.ROHF_RCCSD_T: rohf_rccsd_t_reader,
    # params.METHOD.CUSTOM: custom_e_reader,
}
