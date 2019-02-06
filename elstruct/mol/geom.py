""" functions operating on cartesian geometries
"""
import numpy
from ._linalg import unit_direction
from ._linalg import unit_perpendicular


def internal_coordinates(geo, intco_key_lst):
    """ internal coordinates by key
    """
    intco_dct = {}
    atm_idxs = range(len(geo))
    for intco_key in intco_key_lst:
        assert all(atm_idx in atm_idxs for atm_idx in intco_key)
        if len(intco_key) == 2:
            intco_dct[intco_key] = bond_distance(geo, *intco_key)
        elif len(intco_key) == 3:
            intco_dct[intco_key] = bond_angle(geo, *intco_key)
        elif len(intco_key) == 4:
            intco_dct[intco_key] = torsion_angle(geo, *intco_key)
        else:
            obj_str = repr(intco_key)
            raise ValueError("Invalid coordinate key {:s}".format(obj_str))
    return intco_dct


def bond_distance(geo, idx1, idx2):
    """ bond distance
    """
    _, xyzs = zip(*geo)
    xyz1, xyz2 = map(xyzs.__getitem__, (idx1, idx2))
    dxyz12 = numpy.subtract(xyz2, xyz1)
    dist12 = numpy.linalg.norm(dxyz12)
    return dist12


def bond_angle(geo, idx1, idx2, idx3):
    """ bond angle
    """
    _, xyzs = zip(*geo)
    xyz1, xyz2, xyz3 = map(xyzs.__getitem__, (idx1, idx2, idx3))
    uxyz21 = unit_direction(xyz2, xyz1)
    uxyz23 = unit_direction(xyz2, xyz3)
    ang = numpy.arccos(numpy.dot(uxyz21, uxyz23))
    return ang * 180. / numpy.pi


def torsion_angle(geo, idx1, idx2, idx3, idx4):
    """ torsion angle
    """
    _, xyzs = zip(*geo)
    xyz1, xyz2, xyz3, xyz4 = map(xyzs.__getitem__, (idx1, idx2, idx3, idx4))
    uxyz21 = unit_direction(xyz2, xyz1)
    uxyz23 = unit_direction(xyz2, xyz3)
    uxyz32 = unit_direction(xyz3, xyz2)
    uxyz34 = unit_direction(xyz3, xyz4)
    uxyz123_perp = unit_perpendicular(uxyz21, uxyz23)
    uxyz234_perp = unit_perpendicular(uxyz32, uxyz34)
    tors = numpy.arccos(numpy.dot(uxyz123_perp, uxyz234_perp))
    return tors * 180. / numpy.pi
