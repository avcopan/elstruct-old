"""
Library of functions to retrieve frequency information
from a Psi4 1.0 output file.

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib


# Series of functions to read the frequency information

def harmonic_frequencies_reader(output_string):
    """ Reads the harmonic vibrational frequencies from the output file.
        Returns the frequencies as a list of floats in cm-1.
    """

    # Frequency Line Pattern: Freq [cm^-1]  FLOAT  FLOAT  ... NEWLINE 
    harm_vib_freq_pattern = (
        rep.escape('Freq [cm^-1]') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(
            rep.one_or_more(
                relib.FLOAT +
                rep.maybe('i') +
                rep.one_or_more(relib.WHITESPACE)
            )
        )
    )

    # Obtain the frequencies for all degrees-of-freedom
    harm_freqs = repar.harmonic_frequencies_pattern_parser(harm_vib_freq_pattern, output_string)

    return harm_freqs
