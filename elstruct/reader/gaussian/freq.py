"""
Library of functions to retrieve frequency information
from a Gaussian 09e output file.

Frequencies currently supported:
(1) Harmonic Vibrational Frequencies
(2) Harmonic Zero-Point Vibrational Energy

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

# from ..rere import parse as repar
# from ..rere import pattern as rep
# from ..rere import pattern_lib as relib
# from ... import phys_constants
#
#
# # Series of functions to read the frequency information
#
# def harm_vib_freqs_reader(output_string):
#     """ Reads the harmonic vibrational frequencies from the output file.
#         Returns the frequencies as a list of floats in cm-1.
#     """
#
#     harm_vib_freq_pattern = (
#         'Frequencies --' +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(
#             rep.one_or_more(
#                 relib.FLOAT +
#                 rep.maybe('i') +
#                 rep.one_or_more(relib.WHITESPACE)
#             )
#         )
#     )
#
#     # Obtain the frequencies for all degrees-of-freedom
#     all_freqs = repar.pattern_parser_list_mult_str(harm_vib_freq_pattern, output_string)
#
#     # Remove the zero frequencies
#     vib_freqs = tuple((freq for freq in all_freqs if freq != 0.0))
#
#     # second pattern
#
#     begin_pattern = 'Fundamental Bands (DE w.r.t. Ground State)'
#     end_pattern = 'Overtones (DE w.r.t. Ground State)'
#
#     harm_vib_freq_pattern_2 = (
#         relib.INTEGER +
#         rep.escape('(1)') +
#         relib.WHITESPACE +
#         rep.maybe(rep.one_or_more(relib.LOWERCASE_LETTER)) +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT
#     )
#
#     return vib_freqs
#
#
# def anharm_vib_freqs_reader(output_string):
#     """ Reads the anharmonic vibrational frequencies from the output file.
#         Returns the frequencies as a list of floats in cm-1.
#     """
#
#     begin_pattern = 'Fundamental Bands (DE w.r.t. Ground State)'
#     end_pattern = 'Overtones (DE w.r.t. Ground State)'
#
#     anharm_vib_freq_pattern = (
#         relib.INTEGER +
#         rep.escape('(1)') +
#         relib.WHITESPACE +
#         rep.maybe(rep.one_or_more(relib.LOWERCASE_LETTER)) +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT
#     )
#
#     return vib_freqs
#
#
# def anharm_zpve_reader(output_string):
#     """ Reads the anharmonic zero-point vibrational energy (ZPVE)
#         from the output file.
#         Returns the ZPVE as a float; in Hartrees.
#     """
#
#     anharm_zpve_pattern = (
#         'ZPE(harm) = ' +
#         relib.EXPONENTIAL_FLOAT_D +
#         'KJ/mol' +
#         rep.one_or_more(relib.WHITESPACE) +
#         'ZPE(anh) = ' +
#         rep.capturing(relib.EXPONENTIAL_FLOAT_D) +
#         'KJ/mol'
#     )
#
#     anharm_zpve_pattern_2 = (
#         'Total Anharm' +
#         rep.one_or_more(relib.WHITESPACE) +
#         ':' +
#         relib.WHITESPACE +
#         'cm-1' +
#         relib.WHITESPACE +
#         '=' +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         relib.WHITESPACE +
#         ';' +
#         relib.WHITESPACE +
#         'Kcal/mol' +
#         relib.WHITESPACE +
#         '=' +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         relib.WHITESPACE +
#         ';' +
#         relib.WHITESPACE +
#         'KJ/mol' +
#         relib.WHITESPACE +
#         '=' +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT
#     )
#
#     anharm_zpve = repar.pattern_parser_single_float(anharm_zpve_pattern, output_string)
#     if anharm_zpve is None:
#         anharm_zpve = repar.pattern_parser_single_float(anharm_zpve_pattern_2, output_string) * phys_constants.CM_TO_HART
#
#
#     return anharm_zpve
#
#
# def anharmonicy_matrix(output_string):
#     """ Get the Anharmonicity X Matrix
#     """
#
#     begin_pattern = 'Total Anharmonic X Matrix (in cm^-1)'
#     end_pattern = 'Anharmonic Zero Point Energy'
#
#     pattern = (
#         relib.INTEGER +
#         relib.WHITESPACE +
#         rep.capturing(
#             rep.one_or_more(relib.EXPONENTIAL_FLOAT_D + relib.WHITESPACE)
#         )
#     )
#
#     return X_matrix
#
#
# def vibro_rot_alpha_matrix(output_string):
#     """ get matrix
#     """
#
#     begin_pattern = 'Vibro-Rot alpha Matrix (in cm^-1)'
#     end_pattern = 'Vibro-Rot alpha Matrix (in MHz)'
#
#     pattern = (
#         rep.escape('Q(') +
#         relib.WHITESPACE +
#         relib.INTEGER +
#         rep.escape(')') +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT)
#     )
#
#     return Vib_Rot_Alpha_Matrix
#
#
# def centrifugal_distortion_constants(output_string):
#     """ get centrifugal distortion constants
#     """
#
#     startkey = 'Quartic Centrifugal Distortion Constants Tau Prime'
#     endkey   = 'Asymmetric Top Reduction'
#
#     pattern = (
#         'TauP' +
#         relib.WHITESPACE +
#         rep.one_or_more(relib.LOWERCASE_LETTER) +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.EXPONENTIAL_FLOAT_D) +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.EXPONENTIAL_FLOAT_D
#     )
#
#     return cent_dist_matrix
