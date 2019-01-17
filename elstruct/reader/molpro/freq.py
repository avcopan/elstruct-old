"""
Library of functions to retrieve frequency information from a Molpro 2015 output file.

Frequencies currently supported:
(1) Harmonic Vibrational Frequencies
(2) Harmonic Zero-Point Vibrational Energy

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read the frequency information #####

def harmonic_frequencies_reader(output_string):
    """ Reads the harmonic vibrational frequencies from the output file.
        Returns the frequencies as a list of floats in cm-1.
    """

    # Pattern to locate all frequencies in a string
    harm_vib_freq_pattern = (
        'Wavenumbers \[cm-1\]' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(
            rep.one_or_more(relib.FLOAT +
            rep.one_or_more(relib.WHITESPACE))
        )
    )

    # Obtain the frequencies for all degrees-of-freedom
    all_freqs = repar.list_float(harm_vib_freq_pattern, output_string)

    # Remove the zero frequencies
    vib_freqs = [freq for freq in all_freqs if freq != 0.0]

    return vib_freqs


# def harm_zpve_reader(output_string):
#     """ Reads the harmonic zero-point vibrational energy (ZPVE) from the output file.
#         Returns the ZPVE as a float; in Hartrees.
#     """
# 
#     # String pattern to retrieve the ZPVE
#     zpve_pattern = (
#         'Zero point energy:' +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         '\[H\]' +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.one_or_more(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         '\[1/CM\]' +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.one_or_more(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         '\[KJ/MOL\]'
#     )
# 
#     # Obtain the ZPVE
#     harm_zpve = repar.sing_float(zpve_pattern, output_string)
# 
#     return harm_zpve
