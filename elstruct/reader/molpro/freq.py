"""
Library of functions to retrieve frequency information
from a Molpro 2018 output file.

Frequencies currently supported:
(1) Harmonic Vibrational Frequencies
(2) Harmonic Zero-Point Vibrational Energy

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-30"

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
                rep.one_or_more(relib.WHITESPACE)
            )
        )
    )

    # Obtain the frequencies for all degrees-of-freedom
    harm_freqs = repar.harmonic_frequencies_pattern_parser(
        harm_vib_freq_pattern, output_string)

    # Obtain the imaginary frequencies
    im_freq_block_begin_pattern = 'Imaginary Vibration'
    # + rep.one_or_more(relib.WHITESPACE) + 'Wavenumber'
    im_freq_block_end_pattern = 'Low Vibration'
    # + rep.one_or_more(relib.WHITESPACE) + 'Wavenumber'
    im_freq_block = repar.block(
        im_freq_block_begin_pattern,
        im_freq_block_end_pattern,
        output_string)

    # Check if the imaginary frequency block exists, if so read freqs
    if im_freq_block is not None:
        im_freq_pattern = (
            relib.INTEGER +
            rep.one_or_more(relib.WHITESPACE) +
            rep.capturing(relib.FLOAT)
        )
        im_freqs = repar.harmonic_frequencies_pattern_parser(
            im_freq_pattern, im_freq_block)

        # Relabel frequency if it is imaginary
        harm_freqs_final = []
        for freq in harm_freqs:
            if freq in im_freqs:
                freq = -1.0 * freq
                harm_freqs_final.insert(0, freq)
            else:
                harm_freqs_final.append(freq)
    else:
        harm_freqs_final = harm_freqs

    return harm_freqs_final
