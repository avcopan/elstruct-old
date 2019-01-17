"""
Modules to read information from electronic structure codes
"""
import importlib
from ..params import PROGRAM
from ..phys_constants import CM_TO_HART

PACKAGE = 'elstruct.reader'
PROGRAM_MODULE_NAMES = {
    PROGRAM.MOLPRO: 'molpro',
    PROGRAM.MOLPRO_MPPX: 'molpro',
}


def _import_module(prog):
    """ import the module for a specific program
    """
    assert prog in PROGRAM_MODULE_NAMES.keys()
    module_name = PROGRAM_MODULE_NAMES[prog]
    module = importlib.import_module('.'+module_name, PACKAGE)
    return module


def _programs_with_attribute(attr):
    """ get a list of modules with a given attribute
    """
    progs = []
    for prog in PROGRAM_MODULE_NAMES.keys():
        module = _import_module(prog)
        if hasattr(module, attr):
            progs.append(prog)
    return progs


def energy_programs():
    """ get the list of programs implementing energy readers
    """
    energy_progs = _programs_with_attribute('ENERGY_READERS')
    return energy_progs


def energy_program_methods(prog):
    """ get the list of energy reader methods for a given program
    """
    assert prog in energy_programs()
    module = _import_module(prog)
    energy_prog_methods = tuple(module.ENERGY_READERS.keys())
    return energy_prog_methods


def energy(prog, method, output_string):
    """ Retrieves the desired electronic energy.
    """
    assert prog in energy_programs()
    assert method in energy_program_methods(prog)
    module = _import_module(prog)
    energy = module.ENERGY_READERS[method](output_string)
    return energy


def harmonic_frequencies_programs():
    """ get the list of programs implementing hamonic frequency readers
    """
    freq_progs = _programs_with_attribute('harmonic_frequencies_reader')
    return freq_progs


def harmonic_frequencies(prog, output_string):
    """ Reads the harmonic vibrational frequencies from the output file.
        Returns the frequencies as a list of floats in cm-1.
    """
    assert prog in harmonic_frequencies_programs()
    module = _import_module(prog)
    freqs = module.harmonic_frequencies_reader(output_string)
    return freqs


def harmonic_zero_point_vibrational_energy_programs():
    """ get the list of programs implementing hamonic zero point vibrational energies
    """
    return harmonic_frequencies_programs()


def harmonic_zero_point_vibrational_energy(prog, output_string):
    """ Reads the harmonic zero-point vibrational energy (ZPVE) from the output file.
        Returns the ZPVE as a float; in Hartrees.'
    """
    freqs = harmonic_frequencies(prog=prog, output_string=output_string)
    zpve = sum(freqs) / 2. * CM_TO_HART
    return zpve



def optimized_cartesian_geometry_programs():
    """ get the list of programs implementing optimized cartesian geometry readers
    """
    geom_progs = _programs_with_attribute('optimized_cartesian_geometry_reader')
    return geom_progs


def optimized_cartesian_geometry(prog, output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """
    assert prog in optimized_cartesian_geometry_programs()
    module = _import_module(prog)
    cart_geom = module.optimized_cartesian_geometry_reader(output_string)
    return cart_geom


#def frequency(freq, output_string):
#    """ Retrieves the desired frequency information.
#    """
#
#    assert freq in FREQUENCY_READERS.keys()
#
#    frequency = FREQUENCY_READERS[freq](output_string)
#
#    return frequency

#def structure(struct, output_string):
#    """ Retrieves the desired structural infromation.
#    """
#
#    assert struct in STRUCTURE_READERS.keys()
#
#    struct = STRUCTURE_READERS[struct](output_string)
#
#    return struct
#def surface(surf, output_string):
#    """ Retrieves the desired information regarding the potential energy surface.
#    """
#
#    surf_info = SURFACE_READERS[surf](output_string)
#
#    return surface_info
#def mol_property(prop, output_string):
#    """ Retrieves the desired molecular property.
#    """
#
#    mol_property = PROPERTY_READERS[prop](output_string)
#
#    return mol_property
#def status(output_string):
#    """ Returns the status of a job.
#    """
#
#    # Check if the job completed or if any error messages were printed
#    job_complete = complete_msg_reader(output_string)
#    job_error_str = error_msg_reader(output_string)
#
#    job_status = [complete_status, job_error_str]
#
#    return job_status
