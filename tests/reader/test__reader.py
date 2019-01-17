""" Test readers
"""
import os
import numpy
from elstruct import iohelp
from elstruct import reader

DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


def test__energy():
    """ test reader.energy
    """
    # make sure we're including these programs
    assert (set({'molpro2015', 'molpro2015-mppx'}) <=
            set(reader.energy_programs()))

    for prog in reader.energy_programs():
        for method in reader.energy_program_methods(prog):
            directory_path = os.path.join(DATA_PATH, 'energy', prog, method)
            output_path = os.path.join(directory_path, 'output.dat')
            reference_path = os.path.join(directory_path, 'reference.energ')

            with open(output_path) as output_file:
                output_string = output_file.read()

            reference_energy = iohelp.read_energy(reference_path)
            energy = reader.energy(prog=prog, method=method, output_string=output_string)
            assert numpy.allclose(energy, reference_energy)


def test__harmonic_frequencies():
    """ test reader.harmonic_frequencies
    """
    # make sure we're including these programs
    assert (set({'molpro2015', 'molpro2015-mppx'}) <=
            set(reader.harmonic_frequencies_programs()))

    for prog in reader.harmonic_frequencies_programs():
        directory_path = os.path.join(DATA_PATH, 'harmonic_frequencies', prog)

        reference_path = os.path.join(directory_path, 'reference.harmfreq')
        reference_harm_freqs = iohelp.read_harmonic_frequencies(reference_path)

        output_path = os.path.join(directory_path, 'output.dat')
        with open(output_path) as output_file:
            output_string = output_file.read()

        harm_freqs = reader.harmonic_frequencies(prog=prog, output_string=output_string)

        assert numpy.allclose(harm_freqs, reference_harm_freqs)


def test__harmonic_zero_point_vibrational_energy():
    """ test reader.harmonic_zero_point_vibrational_energy
    """
    # make sure we're including these programs
    assert (set({'molpro2015', 'molpro2015-mppx'}) <=
            set(reader.harmonic_zero_point_vibrational_energy_programs()))

    for prog in reader.harmonic_zero_point_vibrational_energy_programs():
        directory_path = os.path.join(DATA_PATH, 'harmonic_zero_point_vibrational_energy', prog)

        reference_path = os.path.join(directory_path, 'reference.harmzpve')
        reference_harm_zpve = iohelp.read_harmonic_zero_point_vibrational_energy(reference_path)

        output_path = os.path.join(directory_path, 'output.dat')
        with open(output_path) as output_file:
            output_string = output_file.read()

        harm_zpve = reader.harmonic_zero_point_vibrational_energy(
                prog=prog, output_string=output_string)

        assert numpy.allclose(harm_zpve, reference_harm_zpve)


def test__optimized_cartesian_geometry():
    """ test reader.optimized_cartesian_geometry
    """
    # make sure we're including these programs
    assert (set({'molpro2015', 'molpro2015-mppx'}) <=
            set(reader.optimized_cartesian_geometry_programs()))

    for prog in reader.optimized_cartesian_geometry_programs():
        directory_path = os.path.join(DATA_PATH, 'optimized_cartesian_geometry', prog)
        reference_path = os.path.join(directory_path, 'reference.xyz')

        reference_cart_geom = iohelp.read_cartesian_geometry(reference_path)

        output_path = os.path.join(directory_path, 'output.dat')
        with open(output_path) as output_file:
            output_string = output_file.read()

        cart_geom = reader.optimized_cartesian_geometry(prog=prog, output_string=output_string)

        ref_atm_syms, ref_atm_xyzs = zip(*reference_cart_geom)
        atm_syms, atm_xyzs = zip(*cart_geom)

        assert atm_syms == ref_atm_syms
        assert numpy.allclose(atm_xyzs, ref_atm_xyzs)


if __name__ == '__main__':
    test__energy()
    test__harmonic_frequencies()
    test__harmonic_zero_point_vibrational_energy()
    test__optimized_cartesian_geometry()
