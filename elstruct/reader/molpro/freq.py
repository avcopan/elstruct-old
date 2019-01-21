"""
Library of functions to retrieve frequency information
from a Molpro 2018 output file.

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
    """ Reads the harmonic vibrational frequencies
        from the output file.
        Returns the frequencies as a list of floats in cm-1.
    """

    # Pattern to locate all frequencies in a string
    harm_vib_freq_pattern = (
        rep.escape('Wavenumbers [cm-1]') +
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
    all_freqs = repar.pattern_parser_list_mult_str(harm_vib_freq_pattern, output_string)

    # Remove the zero frequencies
    vib_freqs = tuple((freq for freq in all_freqs if freq != 0.0))

    return vib_freqs
