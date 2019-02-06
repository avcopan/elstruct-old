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
            print('\n'+method)
            
            # Set paths to output file and file with reference energy
            directory_path = os.path.join(DATA_PATH, 'energy', prog, method)
            output_path = os.path.join(directory_path, 'output.dat')
            reference_path = os.path.join(directory_path, 'reference.energ')

            # Open output file and read in the energy with reader module
            with open(output_path) as output_file:
                output_string = output_file.read()
            energy = reader.energy(prog=prog, method=method,
                                   output_string=output_string)

            # Read in the reference energy for comparison using iohelp
            reference_energy = iohelp.read_energy(reference_path)

            # Compare energy to reference to see if they match
            assert numpy.allclose(energy, reference_energy, atol=1e-3)


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

                # Set paths to output file and file with reference freqs 
                directory_path = os.path.join(DATA_PATH, 'harmonic_frequencies', prog, coord, struct)
                output_path = os.path.join(directory_path, 'output.dat')
                reference_path = os.path.join(directory_path, 'reference.harmfreq')

                # Open output file and read in the freqs with reader module
                if os.path.exists(os.path.join(directory_path, 'output.dat')):
                    with open(output_path) as output_file:
                        output_string = output_file.read()
                    harm_freqs = reader.harmonic_frequencies(prog=prog, output_string=output_string)

                    # Read in the reference energy for comparison using iohelp
                    reference_harm_freqs = iohelp.read_harmonic_frequencies(reference_path)

                    # Compare freqs to reference to see if they match
                    assert numpy.allclose(harm_freqs, reference_harm_freqs)
                else:
                    continue    


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

                # Set paths to output file and file with reference ZPVE
                directory_path = os.path.join(DATA_PATH, 'harmonic_zero_point_vibrational_energy', prog, coord, struct)
                output_path = os.path.join(directory_path, 'output.dat')
                reference_path = os.path.join(directory_path, 'reference.harmzpve')

                # Open output file and read in the zpve with reader module
                if os.path.exists(os.path.join(directory_path, 'output.dat')):
                    with open(output_path) as output_file:
                        output_string = output_file.read()
                    harm_zpve = reader.harmonic_zero_point_vibrational_energy(
                        prog=prog, output_string=output_string)

                    # Read in the reference zpve for comparison using iohelp
                    reference_harm_zpve = iohelp.read_harmonic_zero_point_vibrational_energy(reference_path)

                    # Compare zpve to reference to see if they match
                    assert numpy.allclose(harm_zpve, reference_harm_zpve)
                else:
                    continue    


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
                reference_path = os.path.join(directory_path, 'reference.xyz')

                reference_cart_geom = iohelp.read_cartesian_geometry(reference_path)

                if os.path.exists(os.path.join(directory_path, 'output.dat')):
                    with open(output_path) as output_file:
                        output_string = output_file.read()

                    cart_geom = reader.optimized_cartesian_geometry(prog=prog, output_string=output_string)
                
                    ref_atm_syms, ref_atm_xyzs = zip(*reference_cart_geom)
                    atm_syms, atm_xyzs = zip(*cart_geom)

                    assert atm_syms == ref_atm_syms
                    assert numpy.allclose(atm_xyzs, ref_atm_xyzs)
                else:
                    continue


def test__cartesian_hessian():
    """ test reader.cartesian_hessian
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
                reference_path = os.path.join(directory_path, 'reference.carthess')

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

                    # Compute eigenvalues of Hessian
                    cart_hess_evals = numpy.linalg.eigvals(cart_hess)
                    print(cart_hess_evals)
                    # Read in the reference zpve for comparison using iohelp
                    #reference_cart_hess_evals = iohelp.read_harmonic_zero_point_vibrational_energy(reference_path)

                    # Compare hessian to reference to see if they match
                    #assert numpy.allclose(cart_hess_evals, reference_cart_hess_evals)
                else:
                   continue 


def test__cartesian_gradient():
    """ test reader.cartesian_gradient
    """
    # Make sure we're including these programs
    assert (set({'molpro2015', 'gaussian09', 'psi4', 'orca4'}) <=
            set(reader.cartesian_gradient_programs()))

    for prog in reader.cartesian_gradient_programs():
        print('\n'+prog)
        for coord in ('internal', 'cartesian'):
            print('\n'+coord)

            # Set paths to the program output file and file w/ reference energy
            directory_path = os.path.join(DATA_PATH, 'cartesian_gradient', prog, coord)
            output_path = os.path.join(directory_path, 'output.dat')
            reference_path = os.path.join(directory_path, 'reference.cartgrad')

            if os.path.exists(output_path):
                with open(output_path) as output_file:
                    output_string = output_file.read()
                cart_grad = reader.cartesian_gradient(
                    prog=prog, output_string=output_string)

                # Read in the reference zpve for comparison using iohelp
                reference_cart_grad = iohelp.read_cartesian_gradient(reference_path)

                # Compare hessian to reference to see if they match
                assert numpy.allclose(cart_grad, reference_cart_grad)
            else:
                continue


if __name__ == '__main__':
    #test__energy()
    #test__harmonic_frequencies()
    #test__harmonic_zero_point_vibrational_energy()
    #test__optimized_cartesian_geometry()
    test__cartesian_hessian()
    #test__cartesian_gradient()
