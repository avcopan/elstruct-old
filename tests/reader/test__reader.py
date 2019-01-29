""" Test readers
"""
import os
import numpy
from elstruct import iohelp
from elstruct import reader

DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


def test__energy():
    """ Test the reader.energy function for each method for each program.
        (1) Reads the final energy from the output file and
        (2) Compares it to the reference energy value
    """

    # Make sure we're including these programs
    assert (set({'molpro2015', 'gaussian09'}) <=
            set(reader.energy_programs()))

    # Loop through each energy dir, read the energy, compare to reference
    for prog in reader.energy_programs():
        print('\n'+prog)
        for method in reader.energy_program_methods(prog):
            # Set paths to the program output file and file w/ reference energy
            directory_path = os.path.join(DATA_PATH, 'energy', prog, method)
            output_path = os.path.join(directory_path, 'output.dat')
            # reference_path = os.path.join(directory_path, 'reference.energ')

            # Open the program output file and read in the energy with reader
            with open(output_path) as output_file:
                output_string = output_file.read()
            energy = reader.energy(prog=prog, method=method,
                                   output_string=output_string)

            # Read in the reference energy for comparison using iohelp
            # reference_energy = iohelp.read_energy(reference_path)

            print(method)
            print(energy)
            # print(reference_energy)

            # Compare energy to reference to see if they match
            # assert numpy.allclose(energy, reference_energy, atol=1e-3)


def test__harmonic_frequencies():
    """ Test the reader.harmonic_frequenies function for each program.
        (1) Reads all of the harmonic frequencies from the output file and
        (2) Compares them to the reference frequencies list
    """

    # Make sure we're including these programs
    assert (set({'molpro2015', 'gaussian09', 'psi4', 'orca4'}) <=
            set(reader.harmonic_frequencies_programs()))

    # Loop through each freq dir, read the energy, compare to reference
    for prog in reader.harmonic_frequencies_programs():
        print('\n'+prog)
        for coord in ('internal', 'cartesian'):
            print('\n'+coord)
            for struct in ('min', 'ts'):
                print(struct)

                # Set paths to the program output file and file w/ reference energy
                directory_path = os.path.join(DATA_PATH, 'harmonic_frequencies', prog, coord, struct)
                output_path = os.path.join(directory_path, 'output.dat')
                # reference_path = os.path.join(directory_path, 'reference.harmfreq')

                # Open the program output file and read in the freqs with reader
                if os.path.exists(os.path.join(directory_path, 'output.dat')):
                    with open(output_path) as output_file:
                        output_string = output_file.read()
                    harm_freqs = reader.harmonic_frequencies(prog=prog, output_string=output_string)

                    # Read in the reference energy for comparison using iohelp
                    # reference_harm_freqs = iohelp.read_harmonic_frequencies(reference_path)

                    print(harm_freqs)

                    # Compare freqs to reference to see if they match
                    # assert numpy.allclose(harm_freqs, reference_harm_freqs)
                else:
                    print('No Job')

def test__harmonic_zero_point_vibrational_energy():
    """ test reader.harmonic_zero_point_vibrational_energy
    """
    # make sure we're including these programs
    assert (set({'molpro2015', 'gaussian09', 'psi4', 'orca4'}) <=
            set(reader.harmonic_zero_point_vibrational_energy_programs()))

    for prog in reader.harmonic_zero_point_vibrational_energy_programs():
        print('\n'+prog)
        for coord in ('internal', 'cartesian'):
            print('\n'+coord)
            for struct in ('min', 'ts'):
                print(struct)

                # Set paths to the program output file and file w/ reference energy
                directory_path = os.path.join(DATA_PATH, 'harmonic_zero_point_vibrational_energy', prog, coord, struct)
                output_path = os.path.join(directory_path, 'output.dat')
                # reference_path = os.path.join(directory_path, 'reference.harmzpve')

                # Open the program output file and read in the zpve with reader
                if os.path.exists(os.path.join(directory_path, 'output.dat')):
                    with open(output_path) as output_file:
                        output_string = output_file.read()
                    harm_zpve = reader.harmonic_zero_point_vibrational_energy(
                        prog=prog, output_string=output_string)

                    # Read in the reference zpve for comparison using iohelp
                    # reference_harm_zpve = iohelp.read_harmonic_zero_point_vibrational_energy(reference_path)

                    print(harm_zpve)

                    # Compare zpve to reference to see if they match
                    # assert numpy.allclose(harm_zpve, reference_harm_zpve)
                else:
                    print('No Job')


def test__optimized_cartesian_geometry():
    """ test reader.optimized_cartesian_geometry
    """
    # Make sure we're including these programs
    assert (set({'molpro2015', 'gaussian09', 'psi4', 'orca4'}) <=
            set(reader.optimized_cartesian_geometry_programs()))

    for prog in reader.optimized_cartesian_geometry_programs():
        print('\n'+prog)
        for coord in ('internal', 'cartesian'):
            print('\n'+coord)
            for struct in ('min', 'ts'):
                print(struct)
                directory_path = os.path.join(DATA_PATH, 'optimized_cartesian_geometry', prog, coord, struct)
                output_path = os.path.join(directory_path, 'output.dat')
                # reference_path = os.path.join(directory_path, 'reference.xyz')

                # reference_cart_geom = iohelp.read_cartesian_geometry(reference_path)

                if os.path.exists(os.path.join(directory_path, 'output.dat')):
                    with open(output_path) as output_file:
                        output_string = output_file.read()

                    cart_geom = reader.optimized_cartesian_geometry(prog=prog, output_string=output_string)
                
                    print(cart_geom)

                    # ref_atm_syms, ref_atm_xyzs = zip(*reference_cart_geom)
                    atm_syms, atm_xyzs = zip(*cart_geom)

                    # assert atm_syms == ref_atm_syms
                    # assert numpy.allclose(atm_xyzs, ref_atm_xyzs)
                else:
                    print('No Job')

# def test__init_internal_geometry():
#     """ test reader.init_internal_geometry
#     """
#     # make sure we're including these programs
#     assert (set({'molpro2015', 'molpro2015-mppx'}) <=
#             set(reader.optimized_cartesian_geometry_programs()))
#
#     for prog in reader.optimized_cartesian_geometry_programs():
#         directory_path = os.path.join(DATA_PATH, 'init_internal_geometry', prog)
#         # reference_path = os.path.join(directory_path, 'reference.xyz')
#
#         # reference_cart_geom = iohelp.read_cartesian_geometry(reference_path)
#
#         output_path = os.path.join(directory_path, 'output.dat')
#         with open(output_path) as output_file:
#             output_string = output_file.read()
#
#         int_geom = reader.init_internal_geometry(prog=prog, output_string=output_string)
#
#         # ref_atm_syms, ref_atm_xyzs = zip(*reference_cart_geom)
#         # atm_syms, atm_xyzs = zip(*cart_geom)
#
#         # assert atm_syms == ref_atm_syms
#         # assert numpy.allclose(atm_xyzs, ref_atm_xyzs)
#         print(int_geom)


def test__cartesian_hessian():
    """ test reader.harmonic_zero_point_vibrational_energy
    """
    # Make sure we're including these programs
    assert (set({'molpro2015', 'gaussian09', 'psi4', 'orca4'}) <=
            set(reader.cartesian_hessian_programs()))

    for prog in reader.cartesian_hessian_programs():
        print('\n'+prog)
        for coord in ('internal', 'cartesian'):
            print('\n'+coord)
            for struct in ('min', 'ts'):
                print(struct)

                # Set paths to the program output file and file w/ reference energy
                directory_path = os.path.join(DATA_PATH, 'cartesian_hessian', prog, coord, struct)
                output_path = os.path.join(directory_path, 'output.dat')
                # reference_path = os.path.join(directory_path, 'reference.harmzpve')

                # Open the program output file and read in the zpve with reader
                if prog == 'orca4':
                    output_path = os.path.join(directory_path, 'Job_Data/input.hess')
                else:    
                    output_path = os.path.join(directory_path, 'output.dat')

                if os.path.exists(output_path):
                    with open(output_path) as output_file:
                        output_string = output_file.read()
                    cart_hess = reader.cartesian_hessian(
                        prog=prog, output_string=output_string)

                    # Read in the reference zpve for comparison using iohelp
                    # reference_harm_zpve = iohelp.read_harmonic_zero_point_vibrational_energy(reference_path)

                    for x in cart_hess:
                        print(x)

                    # Compare hessian to reference to see if they match
                    # assert numpy.allclose(harm_zpve, reference_harm_zpve)
                else:
                    print('No Job')


if __name__ == '__main__':
    # test__energy()
    # test__harmonic_frequencies()
    # test__harmonic_zero_point_vibrational_energy()
    test__optimized_cartesian_geometry()
    # test__init_internal_geometry()
    # test__cartesian_hessian()
