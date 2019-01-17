"""
Library of functions to retrieve frequency information from a Psi4 1.0 output file.

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import parse as repar
from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read the frequency information #####

def harm_vib_freqs_reader(output_string):
    """ Reads the harmonic vibrational frequencies from the output file.
        Returns the frequencies as a list of floats in cm-1.
    """

    # Pattern to locate all frequencies in a string
    harm_vib_freq_pattern = (
        'Freq \[cm^-1\]' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(
            rep.one_or_more(relib.FLOAT +
            rep.one_or_more(relib.WHITESPACE))
        )
    )


def harm_zpve_reader(output_string):
    """ Reads the harmonic zero-point vibrational energy (ZPVE) from the output file.
        Returns the ZPVE as a float; in Hartrees.
    """

    # String pattern to retrieve the ZPVE
    zpve_pattern = (
        'Vibrational ZPE' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        '\[kcal/mol\]' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        '\[kJ/mol\]' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        '\[Eh\]'
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        '\[cm^-1\]'
    )

    # Obtain the ZPVE
    harm_zpve = repar.sing_float_string(zpve_pattern, output_string)

    return harm_zpve


##### Dictionary of functions to read frequency information in the files #####

FREQUENCY_READERS = {
    params.FREQUENCY.HARM_FREQ : harm_vib_freqs_reader,
    params.FREQUENCY.HARM_ZPVE : harm_zpve_reader
}
