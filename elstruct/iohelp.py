""" Functions for writing different types of output
"""
import numpy
from .params import FILE_EXTENSION
from ._dot_xyz import from_geometry as _dot_xyz_from_geometry
from ._dot_xyz import to_geometry as _dot_xyz_to_geometry


def _write_value(file_path, val):
    with open(file_path, 'w') as file_obj:
        file_obj.write(str(val))


def _read_float(file_path):
    with open(file_path, 'r') as file_obj:
        val_str = file_obj.read()
    val = float(val_str)
    return val


def _add_extension(file_name, ext):
    if not str.endswith(file_name, ext):
        file_name += ext
    return file_name


def write_energy(file_name, energy):
    """ write the energy to a file
    """
    file_path = _add_extension(file_name, FILE_EXTENSION.ENERGY)
    _write_value(file_path, energy)


def read_energy(file_name):
    """ read the energy from a file
    """
    return _read_float(file_name)


def write_harmonic_frequencies(file_name, harm_freqs):
    """ write the harmonic frequencies to a file
    """
    file_path = _add_extension(file_name, FILE_EXTENSION.HARMONIC_FREQUENCIES)
    numpy.savetxt(file_path, harm_freqs, fmt='%10.5f')


def read_harmonic_frequencies(file_name):
    """ read the harmonic frequencies from a file
    """
    return numpy.loadtxt(file_name)


def write_harmonic_zero_point_vibrational_energy(file_name, harm_zpve):
    """ write the harmonic ZPVE to a file
    """
    file_path = _add_extension(
        file_name, FILE_EXTENSION.HARMONIC_ZERO_POINT_VIBRATIONAL_ENERGY)
    _write_value(file_path, harm_zpve)


def read_harmonic_zero_point_vibrational_energy(file_name):
    """ read the harmonic ZPVE from a file
    """
    return _read_float(file_name)


def write_cartesian_geometry(file_name, cart_geom):
    """ write the cartesian geometry to a file
    """
    file_path = _add_extension(file_name, FILE_EXTENSION.CARTESIAN_GEOMETRY)
    file_str = _dot_xyz_from_geometry(cart_geom)
    _write_value(file_path, file_str)


def read_cartesian_geometry(file_name):
    with open(file_name) as file_obj:
        file_str = file_obj.read()
    cart_geom = _dot_xyz_to_geometry(file_str)
    return cart_geom
