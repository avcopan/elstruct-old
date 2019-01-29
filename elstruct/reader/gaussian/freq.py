"""
Library of functions to retrieve frequency information
from a Gaussian 09e output file.

Frequencies currently supported:
(1) Harmonic Vibrational Frequencies
(2) Harmonic Zero-Point Vibrational Energy

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

from ..rere import parse as repar
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import phys_constants


# Series of functions to read the frequency information

def harmonic_frequencies_reader(output_string):
    """ Reads the harmonic vibrational frequencies from the output file.
        Returns the frequencies as a list of floats in cm-1.
    """
    
    # FIRST PATTERN FOR THE HARMONIC FREQUENCIES #

    # Frequency Line Pattern: Frequencies -- FLOAT  FLOAT  ... NEWLINE 
    harm_freq_pattern = (
        'Frequencies --' +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(
            rep.one_or_more(
                relib.FLOAT +
                rep.one_or_more(relib.WHITESPACE)
            )
        )
    )

    # SECOND PATTERN FOR THE HARMONIC FREQUENCIES #
    
    # # Second pattern for harm vib freqs
    harm_freq_block_begin_pattern = 'Fundamental Bands (DE w.r.t. Ground State)'
    harm_freq_block_end_pattern = 'Overtones (DE w.r.t. Ground State)'
    harm_freq_block = repar.block(harm_freq_block_begin_pattern,
                                  harm_freq_block_end_pattern,
                                  output_string)

    harm_freq_pattern_2 = (
        relib.INTEGER +
        rep.escape('(1)') +
        relib.WHITESPACE +
        rep.maybe(rep.one_or_more(relib.LOWERCASE_LETTER)) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT
    )

    # Obtain the frequencies for all degrees-of-freedom
    # Remove the zero frequencies
    harm_freqs = repar.harmonic_frequencies_pattern_parser(harm_freq_pattern, output_string)
    # if all_freqs is None:
    #     all_freqs = repar.pattern_parser(harm_freq_pattern_2, harm_freq_block)
    #     vib_freqs = tuple((freq for freq in all_freqs if freq != 0.0))
    # else:
    #     vib_freqs = tuple((freq for freq in all_freqs if freq != 0.0))

    return harm_freqs


def anharmonic_frequenciess_reader(output_string):
    """ Reads the anharmonic vibrational frequencies from the output file.
        Returns the frequencies as a list of floats in cm-1.
    """

    # Patterns to identify text block where the frequencies are located
    anharm_freq_block_begin_pattern = 'Fundamental Bands (DE w.r.t. Ground State)'
    anharm_freq_block_end_pattern = 'Overtones (DE w.r.t. Ground State)'

    # Obtain text block of containing the frequencies 
    anharm_freq_block = repar.block(anharm_freq_block_begin_pattern,
                                    anharm_freq_block_end_pattern,
                                    output_string)

    # Frequency Line Pattern: INT(1)  a  FLOAT  FLOAT  FLOAT  FLOAT  NEWLINE
    anharm_freq_pattern = (
        relib.INTEGER +
        rep.escape('(1)') +
        relib.WHITESPACE +
        rep.maybe(rep.one_or_more(relib.LOWERCASE_LETTER)) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT
    )

    # Obtain the frequencies for all degrees-of-freedom
    anharm_freqs = repar.harmonic_frequencies_pattern_parser(anharm_vib_freq_pattern, vib_freq_block)

    # Remove the zero frequencies
    anharm_freqs = tuple((freq for freq in all_freqs if freq != 0.0))

    return anharm_freqs


def anharm_zpve_reader(output_string):
    """ Reads the anharmonic zero-point vibrational energy (ZPVE)
        from the output file.
        Returns the ZPVE as a float; in Hartrees.
    """

    # FIRST PATTERN FOR THE ANHARMONIC ZPVE #
    
    anharm_zpve_pattern = (
        'ZPE(harm) = ' +
        relib.EXPONENTIAL_FLOAT_D +
        'KJ/mol' +
        rep.one_or_more(relib.WHITESPACE) +
        'ZPE(anh) = ' +
        rep.capturing(relib.EXPONENTIAL_FLOAT_D) +
        'KJ/mol'
    )
    
    # SECOND PATTERN FOR THE ANHARMONIC ZPVE #

    anharm_zpve_pattern_2 = (
        'Total Anharm' +
        rep.one_or_more(relib.WHITESPACE) +
        ':' +
        relib.WHITESPACE +
        'cm-1' +
        relib.WHITESPACE +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        relib.WHITESPACE +
        ';' +
        relib.WHITESPACE +
        'Kcal/mol' +
        relib.WHITESPACE +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT +
        relib.WHITESPACE +
        ';' +
        relib.WHITESPACE +
        'KJ/mol' +
        relib.WHITESPACE +
        '=' +
        rep.one_or_more(relib.WHITESPACE) +
        relib.FLOAT
    )
    
    # RETRIEVE THE ANHARMONIC ZPVE #

    anharm_zpve = repar.anharm_zpve_pattern_parser(anharm_zpve_pattern, output_string)
    if anharm_zpve is None:
        anharm_zpve = repar.anharm_zpve_pattern_parser(anharm_zpve_pattern_2, output_string) * phys_constants.CM_TO_HART

    return anharm_zpve


def anharmonicity_matrix_reader(output_string):
    """ Get the Anharmonicity X Matrix
    """

    # Patterns to identify text block where anharmonicity matrix is located
    anharm_matrix_block_begin_pattern = 'Total Anharmonic X Matrix (in cm^-1)'
    anharm_matrix_block_end_pattern = 'Anharmonic Zero Point Energy'

    # Obtain text block of containing the anharmonicity matrix
    anharm_matrix_block = repar.block(anharm_matrix_block_begin_pattern,
                                      anharm_matrix_block_end_pattern,
                                      output_string)

    # Anharm Line Pattern: INT  EXP_D  EXP_D  ...  NEWLINE
    anharm_matrix_pattern = (
        relib.INTEGER +
        relib.WHITESPACE +
        rep.capturing(
            rep.one_or_more(relib.EXPONENTIAL_FLOAT_D + relib.WHITESPACE)
        )
    )

    # Retrieve the anharmonicity matrix
    anharm_matrix = repar.anharm_matrix_pattern_parser(anharm_matrix_pattern, anharm_matrix_block)

    return anharm_matrix


def vibro_rot_alpha_matrix_reader(output_string):
    """ get matrix
    """

    # Patterns to identify text block where vib-rot matrix is located
    vib_rot_matrix_block_begin_pattern = 'Vibro-Rot alpha Matrix (in cm^-1)'
    vib_rot_matrix_block_end_pattern = 'Vibro-Rot alpha Matrix (in MHz)'

    # Obtain text block of containing the vib-rot matrix
    vib_rot_matrix_block = repar.block(vib_rot_matrix_block_begin_pattern,
                                       vib_rot_matrix_block_end_pattern,
                                       output_string)

    # Vib-Rot Matrix Pattern: Q(INT)  FLOAT  FLOAT  FLOAT  NEWLINE
    vib_rot_matrix_pattern = (
        rep.escape('Q(') +
        relib.WHITESPACE +
        relib.INTEGER +
        rep.escape(')') +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.FLOAT)
    )

    # Retrieve the Vib-Rot matrix
    vib_rot_matrix = repar.vib_rot_matrix_pattern_parser(vib_rot_matrix_pattern, vib_rot_matrix_block)

    return vib_rot_matrix


def centrifugal_distortion_constants_reader(output_string):
    """ get centrifugal distortion constants
    """

    # Patterns to identify text block where cent dist constants are located
    cent_dist_const_block_begin_pattern = 'Quartic Centrifugal Distortion Constants Tau Prime'
    cent_dist_const_block_end_pattern = 'Asymmetric Top Reduction'

    # Obtain text block of containing the cent dist constants
    cent_dist_const_block = repar.block(cent_dist_const_block_begin_pattern,
                                        cent_dist_const_block_end_pattern,
                                        output_string)

    # Cent Dist Const Pattern: TauP aaaa  EXP_D  EXP_D  NEWLINE
    cent_dist_const_pattern = (
        'TauP' +
        relib.WHITESPACE +
        rep.one_or_more(relib.LOWERCASE_LETTER) +
        rep.one_or_more(relib.WHITESPACE) +
        rep.capturing(relib.EXPONENTIAL_FLOAT_D) +
        rep.one_or_more(relib.WHITESPACE) +
        relib.EXPONENTIAL_FLOAT_D
    )

    # Retieve the centrifugal distortion constants
    cent_dist_const = repar.cent_dist_const_pattern_parser(cent_dist_const_pattern, cent_dist_const_block)

    return cent_dist_const
