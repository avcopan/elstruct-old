"""
Library of functions to retrieve molecular properties
from a CFour 2.0 output file.

Properties currently supported:
(1) Dipole Moment

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


# Series of functions to read molecular properties

def scf_reader(output_string):
    """ Reads the SCF Permanent Dipole moment from the output file.
        Returns the constants as a list of strings; in Debye.
    """

    # scf pattern
    dipole_mom_pattern = (
        '@DRVPRP-I, Properties computed from the SCF density matrix follow.' +
        'Components of electric dipole moment' +
        'X =' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        'Y =' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        'Z =' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # scf pattern 2
    dipole_mom_begin_pattern = 'Total dipole moment'
    dipole_mom_end_pattern = (
        'Conversion factor used: 1 a.u. =' +
        rep.one_or_more(relib.WHITESPACE) +
        '2.54174691 Debye'
    )

    dipole_mom_block = repar.block(dipole_mom_begin_pattern,
                                   dipole_mom_end_pattern,
                                   output_string)

    dipole_mom_pattern_2 = (
        relib.ANY_CHAR +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the SCF dipole moment
    dipole_mom = repar.pattern_parser_list_single_str(dipole_mom_pattern, output_string)
    if dipole_mom is None:
        dipole_mom = repar.pattern_parser_list_single_str(dipole_mom_pattern_2, dipole_mom_block)

    return dipole_mom


def corr_reader(output_string):
    """ Reads the correlated permanent dipole moment from the output file.
        Returns the constants as a list of strings; in Debye.
    """

    # correlated
    dipole_mom_pattern = (
        '@DRVPRP-I,' +
        'Properties computed from the correlated density matrix follow.' +
        'Components of electric dipole moment' +
        'X =' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        'Y =' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        'Z =' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Obtain the SCF dipole moment
    dipole_mom = repar.pattern_parser_list_single_str(dipole_mom_pattern, output_string)

    return dipole_mom


# Dictionary of functions to read molecular properties in the files

PROPERTY_READERS = {
    params.METHOD.RHF: scf_reader,
    params.METHOD.UHF: scf_reader,
    params.METHOD.ROHF: scf_reader,
    params.METHOD.RHF_MP2: corr_reader,
}
