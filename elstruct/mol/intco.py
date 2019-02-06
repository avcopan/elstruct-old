""" functions operating on internal coordinates
"""
import numpy
from ._linalg import unit_direction
from ._linalg import unit_perpendicular


def cartesian_coordinates(dist, ang, tors, xyz1, xyz2, xyz3):
    """ determine an atom's cartesian coordinates from its distance, angle, and torsion
    angle to three other atoms
    """
    loc_frame_xyz = local_frame_position(dist, ang, tors)
    loc_frame_basis = local_frame(xyz1, xyz2, xyz3)
    xyz = numpy.add(xyz1, numpy.dot(loc_frame_xyz, loc_frame_basis))
    return tuple(xyz)


def local_frame_position(dist, ang, tors):
    """ position by internal coordinates in the local axis frame
    """
    x_comp = dist * numpy.sin(ang) * numpy.sin(tors)
    y_comp = dist * numpy.sin(ang) * numpy.cos(tors)
    z_comp = dist * numpy.cos(ang)
    return (x_comp, y_comp, z_comp)


def local_frame(xyz1, xyz2, xyz3):
    """ local axes for defining bond, angle, torsion from support atoms
    """
    uxyz12 = unit_direction(xyz1, xyz2)
    uxyz23 = unit_direction(xyz2, xyz3)
    uxyz123_perp = unit_perpendicular(uxyz12, uxyz23)

    z_ax = tuple(uxyz12)
    y_ax = tuple(unit_perpendicular(uxyz123_perp, z_ax))
    x_ax = tuple(unit_perpendicular(y_ax, z_ax))
    return (x_ax, y_ax, z_ax)
