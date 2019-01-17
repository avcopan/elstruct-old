"""
Library of functions to retrieve structural information from a Gaussian 09e output file

"""

__authors__ = "Kevin Moore, Andreas Copan"
__updated__ = "2019-01-15"

from ..rere import find as ref
from ..rere import pattern as rep
from ..rere import pattern_lib as relib
from ... import params


##### Series of functions to read structural information #####

##### Dictionary for strings to find the geometries in the files #####

STRUCTURE_READERS = {
}
#def gaussian_opt_zmat_params(lines):
#    
#    params = ''
#    if not 'Optimized Parameters' in lines:
#        return None
#    varis  = lines.split('Optimized Parameters')[1].split('---------------------------------------')
#    if 'Definition' in varis[0]:
#        varis = varis[2].split('\n')
#        for var in varis[1:-1]:
#            var = var.split()
#            params += ' '+  var[1] + '\t' + var[3] + '\n'
#    else:
#        varis = varis[1].split('\n')
#        for var in varis[1:-1]:
#            var = var.split()
#            params += ' '+  var[1] + '\t' + var[2] + '\n'
#    return params
#
#def gaussian_zmat(lines):
#
#    lines  = lines.split('Z-matrix:\n')
#    zmat   = lines[1].split('       Variables:')[0]
#    zmat  += 'Variables:\n'
#    zmat   = zmat.replace('Charge = ','')
#    zmat   = zmat.replace('Multiplicity =','')
#    optzmat = gaussian_opt_zmat_params(lines[1])
#    if optzmat == None:
#        return None
#    return zmat + optzmat
#
#def gaussian_xyz_foresk(lines):
#    atom = lines.split('Distance matrix')[-1].split('Symm')[0]
#    if len(atom.split('\n')) > 8:
#        atom = atom.split(' 6 ')[0] + ' 6 ' + atom.split(' 6 ')[1]
#        atom = atom.split('\n')[2:-2]
#    length = len(atom)
#    atoms  = []
#    for at in atom:
#        atoms.extend(at.split()[1])
#    xyz = 'Geometry ' + str(length) + ' Angstrom\n'
#    if 'Eckart' in lines:
#        lines = lines.split('Gaussian Orientation')[-1].split('Eckart')[0]
#        lines = lines.split('\n')[5:-2]
#        for i,line in enumerate(lines):
#            line = line.split()
#            xyz += atoms[i] + '  ' + line[2] + '  ' + line[3] + '  ' + line[4] + '\n'
#    else:
#        lines = lines.split('Coordinates (Angstroms)')[-1].split(' Distance matrix')[0]
#        lines = lines.split('\n')[3:-2]
#        for i,line in enumerate(lines):
#            line = line.split()
#            xyz +=  atoms[i] + '  ' + line[3] + '  ' + line[4] + '  ' + line[5] + '\n'
#    return xyz 
#    
#def gaussian_geo(lines):
#    atomnum = {'1':'H','6':'C','7':'N','8':'O'}
#    xyz = ''
#    try:
#        if 'Eckart' in lines:
#            lines = lines.split('Gaussian Orientation')[-1].split('Eckart')[0]
#            lines = lines.split('\n')[5:-2]
#            for i,line in enumerate(lines):
#                line = line.split()
#                xyz += atomnum[line[1]]+ '  ' + line[2] + '  ' + line[3] + '  ' + line[4] + '\n'
#        else:
#            lines = lines.split('Coordinates (Angstroms)')[-1].split(' Distance matrix')[0].split(' Rotation')[0].split('Symm')[0]
#            lines = lines.split('\n')[3:-2]
#            for i,line in enumerate(lines):
#                line = line.split()
#                xyz += ' ' + atomnum[line[1]] + '  ' + line[3] + '  ' + line[4] + '  ' + line[5] + '\n'
#    except:
#        logging.error('Cannot parse xyz')
#    return xyz
#   
#def gaussian_xyz(lines):
#    geo = gaussian_geo(lines) 
#    if geo:
#        n   = str(len(geo.splitlines()))
#        xyz = n + '\n\n' +  geo
#    else:
#        xyz = ''
#    return xyz
#
#def gaussian_rotconstscent(lines):
#    startkey = 'Effective Rotational Constants'
#    lines = lines.splitlines()
#    sline = io.get_line_number(startkey,lines=lines)
#    if sline < 0:
#        return ''
#    rotlines   =  lines[sline+4:sline+7]
#    constants = []
#    for line in rotlines:
#        constants.append(line.split()[1])
#    return constants
#
#def gaussian_rotconsts(lines):
#    rot = 'Rotational constants\s*\(GHZ\):\s*([\s,\d,\.,\-]*)'     
#    rot = re.findall(rot,lines)
#    if len(rot) > 0: 
#        rot = rot[-1].split()
#    ndof  = gaussian_nfreq(lines)
#    if ndof < 2:
#        rot = rot[1:]
#    if len(rot) > 0:
#         if abs(float(rot[0])) < 0.000001:
#             rot = rot[1:]
#    return rot
