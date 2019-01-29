"""
Library of functions to retrieve frequency information
from a CFour 2.0 output file.

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

    harm_vib_begin_pattern = 'Cartesian force constants:'
    harm_vib_end_pattern = 'Zero-point energy:'

    harm_vib_block = repar.block(harm_vib_begin_pattern,
                                 harm_vib_end_pattern,
                                 output_string)

    harm_vib_freq_pattern = (
        relib.INTEGER +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT + rep.maybe('i'))
    )

    # Obtain the frequencies for all degrees-of-freedom
    all_freqs = repar.harmonic_frequencies_pattern_parser(harm_vib_freq_pattern, harm_vib_block)

    # Remove the zero frequencies
    vib_freqs = tuple((freq for freq in all_freqs if freq != 0.0))

    return vib_freqs
