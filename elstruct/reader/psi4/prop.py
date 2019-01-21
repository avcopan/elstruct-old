"""
Library of functions to retrieve molecular properties
from a Psi4 1.0 output file.

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

def dipole_moment_reader(output_string):
    """ Reads the SCF permanent dipole moment from the output file.
        Returns the constants as a list of strings; in Debye.
        TODO: For any method???
    """

    dipole_mom_pattern = (
        rep.escape('Dipole Moment: [D]') +
        rep.one_or_more(relib.WHITESPACE) +
        'X:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        'Y:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        'Z:' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        'Total:' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT
    )

    # Obtain the SCF dipole moment
    dipole_mom = repar.pattern_parser_list_single_str(dipole_mom_pattern, output_string)

    return dipole_mom


# Dictionary of functions to read molecular properties in the files

PROPERTY_READERS = {
    params.METHOD.RHF: dipole_moment_reader,
    params.METHOD.UHF: dipole_moment_reader,
    params.METHOD.ROHF: dipole_moment_reader,
    params.METHOD.DFT: dipole_moment_reader,
}
