"""
Library of functions to retrieve frequency information
from a Orca 4.0 output file.

Frequencies currently supported:
(1) Harmonic Vibrational Frequencies
(2) Harmonic Zero-Point Vibrational Energy

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

    # Patterns to identify text block where the frequencies are located
    harm_freqs_begin_pattern = 'VIBRATIONAL FREQUENCIES'
    harm_freqs_end_pattern = 'NORMAL MODES'

    # Obtain text block containing the frequencies
    harm_freqs_block = repar.block(harm_freqs_begin_pattern,
                                   harm_freqs_end_pattern,
                                   output_string)

    # Frequency Line Pattern: INT:  FLOAT  cm**-1
    harm_freqs_pattern = (
        rep.one_or_more(relib.INTEGER) +
        ':' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        relib.WHITESPACE +
        rep.escape('cm**-1')
    )

    # Obtain the frequencies for all degrees-of-freedom
    harm_freqs = repar.harmonic_frequencies_pattern_parser_2(harm_freqs_pattern, harm_freqs_block)

    return harm_freqs
