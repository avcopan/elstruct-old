"""
Library of functions to retrieve structural information
from a Gaussian 09e output file

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-18"

# from ..rere import parse as repar
# from ..rere import pattern as rep
# from ..rere import pattern_lib as relib
# from ... import phys_constants
#
#
# # Series of functions to read structural information
#
# def optimized_cartesian_geometry_reader(output_string):
#     """ Retrieves the optimized geometry in Cartesian xyz coordinates.
#         Units of Angstrom.
#     """
#
#     # Pattern to idetify text block of where optimized geometry is located
#     opt_geom_xyz_begin_pattern = 'Standard orientation:'
#     opt_geom_xyz_end_pattern = 'Rotational constants (GHZ):' + rep.one_or_more(relib.WHITESPACE+relib.FLOAT)
#
#     # Obtain text block of containing the optimized geometry in xyz coordinates
#     opt_geom_xyz_block = repar.block(opt_geom_xyz_begin_pattern,
#                                      opt_geom_xyz_end_pattern,
#                                      output_string)
#
#     # Pattern for the xyz coordinate of each atom
#     opt_geom_xyz_pattern = (
#         relib.INTEGER +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.INTEGER) +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.INTEGER +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT)
#     )
#
#     cart_geom_atom_num = repar.pattern_parser_cartesian_geometry(
#         opt_geom_xyz_pattern, opt_geom_xyz_block)
#
#     # Convert from Bohrs to Angstroms
#     cart_geom = tuple((phys_constants.ATOM_NUM[num], (x, y, z))
#                       for num, coord in cart_geom_atom_num
#                       for x, y, z in coord)
#
#     return cart_geom
#
#
# def internal_coord_geom(output_string):
#     """ internal coord.
#     """
#
#     # zmat
#     begin = 'Symbolic Z-matrix'
#     end = 'Initial Paramters'
#
#     #coord
#     begin = 'Variables'
#     end = 'Initial Paramters'
#
#     coord_pattern = (
#         rep.one_or_more(relib.ANY_CHAR) +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT
#     )
#
#     # opt coord
#     begin = '-- Stationary point found.'
#     end = 'GradGradGrad'
#
#     opt_coord_pattern = (
#         '!' +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.one_or_more(relib.ANY_CHAR) +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         '-DE/DX =' +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         '!'
#     )
#
#     return internal_coord_geom
#
#
# def equil_rot_constant_reader(output_string):
#     """ Retrieves the equilibrium rotational constant of the optimized geometry.
#         Units of cm-1.
#     """
#
#     equil_rot_const_pattern = (
#         rep.escape('Rotational constants (GHZ):') +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT)
#     )
#
#     # Obtain equil_const string
#     all_rot_consts = repar.pattern_parser_list_single_str(equil_rot_const_pattern, output_string)
#
#     # Remove any instances of 0.0000s as well as duplicates
#     rot_const_ghz = tuple((const for const in all_rot_consts if const != 0.0))
#
#     # Convert from GHz to cm-1
#     equil_rot_const = tuple((const * phys_constants.GHZ_TO_CM
#                             for const in rot_const_ghz))
#
#     return equil_rot_const
#
# def effective_rot_constants(output_string):
#     """ get effective constants the B(A)
#     """
#
#     begin = (
#         rep.escape('Be in cm^-1') +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.escape('B(A) in cm^-1') +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.escape('B(A) in MHz') +
#         rep.one_or_more(relib.WHITESPACE)
#     )
#     end = 'Nielsen Centrigugal Distorsion Constants'
#
#     pattern = (
#         relib.LOWERCASE_LETTER +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT +
#         rep.one_or_more(relib.WHITESPACE) +
#         rep.capturing(relib.FLOAT) +
#         rep.one_or_more(relib.WHITESPACE) +
#         relib.FLOAT
#     )
#
#     return eff_rot_consts
#
# # def gaussian_opt_zmat_params(lines):
# #
# #    params = ''
# #    if not 'Optimized Parameters' in lines:
# #        return None
# #    varis  = lines.split('Optimized Parameters')[1].split('---------------------------------------')
# #    if 'Definition' in varis[0]:
# #        varis = varis[2].split('\n')
# #        for var in varis[1:-1]:
# #            var = var.split()
# #            params += ' '+  var[1] + '\t' + var[3] + '\n'
# #    else:
# #        varis = varis[1].split('\n')
# #        for var in varis[1:-1]:
# #            var = var.split()
# #            params += ' '+  var[1] + '\t' + var[2] + '\n'
# #    return params
# #
# #def gaussian_zmat(lines):
# #
# #    lines  = lines.split('Z-matrix:\n')
# #    zmat   = lines[1].split('       Variables:')[0]
# #    zmat  += 'Variables:\n'
# #    zmat   = zmat.replace('Charge = ','')
# #    zmat   = zmat.replace('Multiplicity =','')
# #    optzmat = gaussian_opt_zmat_params(lines[1])
# #    if optzmat == None:
# #        return None
# #    return zmat + optzmat
# #
# #def gaussian_xyz_foresk(lines):
# #    atom = lines.split('Distance matrix')[-1].split('Symm')[0]
# #    if len(atom.split('\n')) > 8:
# #        atom = atom.split(' 6 ')[0] + ' 6 ' + atom.split(' 6 ')[1]
# #        atom = atom.split('\n')[2:-2]
# #    length = len(atom)
# #    atoms  = []
# #    for at in atom:
# #        atoms.extend(at.split()[1])
# #    xyz = 'Geometry ' + str(length) + ' Angstrom\n'
# #    if 'Eckart' in lines:
# #        lines = lines.split('Gaussian Orientation')[-1].split('Eckart')[0]
# #        lines = lines.split('\n')[5:-2]
# #        for i,line in enumerate(lines):
# #            line = line.split()
# #            xyz += atoms[i] + '  ' + line[2] + '  ' + line[3] + '  ' + line[4] + '\n'
# #    else:
# #        lines = lines.split('Coordinates (Angstroms)')[-1].split(' Distance matrix')[0]
# #        lines = lines.split('\n')[3:-2]
# #        for i,line in enumerate(lines):
# #            line = line.split()
# #            xyz +=  atoms[i] + '  ' + line[3] + '  ' + line[4] + '  ' + line[5] + '\n'
# #    return xyz
