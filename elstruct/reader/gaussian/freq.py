"""
Library of functions to retrieve frequency information from a Gaussian 09e output file.

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

def harm_vib_freqs_reader(output_string):
    """ Reads the harmonic vibrational frequencies from the output file.
        Returns the frequencies as a list of floats in cm-1.
    """

    harm_vib_freq_pattern = (
        'Frequencies --' +
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

    freqs = []
    lines = lines.splitlines()
    key = 'Fundamental Bands (DE w.r.t. Ground State)'
    iline = io.get_line_number(key,lines=lines)
    if iline > 0:
        for i in range(nfreq):
            iline += 1
            line = lines[iline]
            cols = line.split()
            freqs.append(cols[-5])


    return vib_freqs

def harm_zpve_reader(output_string):
    """ Reads the harmonic zero-point vibrational energy (ZPVE) from the output file.
        Returns the ZPVE as a float; in Hartrees.
    """

    harm_zpve_pattern_1 = (
        'Zero-point correction=' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.one_or_more(relib.FLOAT)
        '(Hartree/Particle)'
    )

    return harm_zpve

def anharm_zpve_reader(output_string):
    """ Reads the anharmonic zero-point vibrational energy (ZPVE) from the output file.
        Returns the ZPVE as a float; in Hartrees.
    """

    anharm_zpve_pattern = (
        'ZPE(harm) =' +
        FLOAT +
        D-02 +
        'KJ/mol' +
        'ZPE(anh) =' +
        FLOAT +
        D-02 +
        'KJ/mol'
    )

    return anharm_zpve


##### Dictionary of functions to read frequency information in the files #####

FREQUENCY_READERS = {
    params.FREQUENCY.HARM_FREQ : harm_vib_freqs_reader,
    params.FREQUENCY.HARM_ZPVE : harm_zpve_reader
    params.FREQUENCY.ANHARM_ZPVE : anharm_zpve_reader
}
#def gaussian_rotdists (lines):
#    startkey = 'Quartic Centrifugal Distortion Constants Tau Prime'
#    endkey   = 'Asymmetric Top Reduction'
#    lines = lines.splitlines()
#    sline = io.get_line_number(startkey,lines=lines)
#    if sline < 0:
#        return ''
#    lines  = lines[sline+3:sline+9]
#    distlines = []
#    for line in lines:
#        splitline = line.split()
#        if splitline[0] == 'TauP': 
#           distlines.append('\t'.join(splitline[1:3]))
#        else:
#           break
#    constants   = '\n'.join(distlines).replace('D','e')
#    return constants
#
#def gaussian_vibrot(lines):
#    startkey = 'Vibro-Rot alpha Matrix (in cm^-1)'
#    ndof  = gaussian_nfreq(lines)
#    lines = lines.splitlines()
#    sline = io.get_line_number(startkey,lines=lines)
#    if sline < 0:
#        return ''
#    lines =  lines[sline+3:sline+3+ndof]
#    for i in range(len(lines)):
#       if ')' in lines[i]:
#           lines[i] = lines[i].split(')')[1]
#       if ndof < 2:
#          lines[i] = '\t'.join(lines[i].split()[:-1])
#    mat   = '\n'.join(lines).split('---------------')[0]
#    return mat
