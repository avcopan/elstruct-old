"""
Modules to read information from electronic structure codes
"""

import importlib
from ..params import PROGRAM
from ..phys_constants import CM_TO_HART


__authors__ = "Kevin Moore and Andreas Copan"
__updated__ = "2019-01-21"


PACKAGE = 'elstruct.reader'
PROGRAM_MODULE_NAMES = {
    PROGRAM.GAUSSIAN: 'gaussian',
    PROGRAM.MOLPRO: 'molpro',
    # PROGRAM.MOLPRO_MPPX: 'molpro',
    PROGRAM.ORCA: 'orca',
    PROGRAM.PSI4: 'psi4',
}


# FUNCTIONS TO IMPORT AND CHECK FOR READER MODULES #

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


# FUNCTIONS TO RETRIEVE ELECTRONIC ENERGIES #


# Assess the functionality of the energy module for each program #

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


# Function called to retrieve the energy #

def energy(prog, method, output_string):
    """ Retrieves the desired electronic energy.
    """
    
    assert prog in energy_programs()
    assert method in energy_program_methods(prog)
    module = _import_module(prog)
    energy_val = module.ENERGY_READERS[method](output_string)

    return energy_val


# FUNCTIONS TO RETRIEVE THE HARMONIC FREQUENCIES AND ZPVE #


# Assess the functionality of the frequency module for each program #

def harmonic_frequencies_programs():
    """ get the list of programs implementing hamonic frequency readers
    """
    
    freq_progs = _programs_with_attribute('harmonic_frequencies_reader')

    return freq_progs


def harmonic_zero_point_vibrational_energy_programs():
    """ get the list of programs implementing
        hamonic zero point vibrational energies
    """

    zpve_progs = harmonic_frequencies_programs()

    return zpve_progs 


# Functions called to retrieve the frequencies and ZPVE #

def harmonic_frequencies(prog, output_string):
    """ Reads the harmonic vibrational frequencies from the output file.
        Returns the frequencies as a list of floats in cm-1.
    """

    assert prog in harmonic_frequencies_programs()
    module = _import_module(prog)
    freqs = module.harmonic_frequencies_reader(output_string)

    return freqs


def harmonic_zero_point_vibrational_energy(prog, output_string):
    """ Reads the harmonic zero-point vibrational energy (ZPVE)
        from the output file.
        Returns the ZPVE as a float; in Hartrees.'
    """

    freqs = harmonic_frequencies(prog=prog, output_string=output_string)
    
    zpve = sum(freq for freq in freqs if freq > 0.0) / 2. * CM_TO_HART

    return zpve


# FUNCTIONS TO RETRIEVE MOLECULAR GEOMETRIES #


# Assess the functionality of the structure module for each program #

def optimized_cartesian_geometry_programs():
    """ get the list of programs implementing optimized cartesian geometry readers
    """
    geom_progs = _programs_with_attribute(
        'optimized_cartesian_geometry_reader')

    return geom_progs


def init_internal_geometry_programs():
    """ get the list of programs implementing init internal geometry readers
    """
    geom_progs = _programs_with_attribute(
        'init_internal_geometry_reader')

    return geom_progs


# Functions called to retrieve the geometries #

def optimized_cartesian_geometry(prog, output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """
    assert prog in optimized_cartesian_geometry_programs()
    module = _import_module(prog)
    cart_geom = module.optimized_cartesian_geometry_reader(output_string)

    return cart_geom


def init_internal_geometry(prog, output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """
    assert prog in init_internal_geometry_programs()
    module = _import_module(prog)
    int_geom = module.init_internal_geometry_reader(output_string)

    return int_geom


# FUNCTIONS TO RETRIEVE HESSIAN #


def cartesian_hessian_programs():
    """ get the list of programs implementing cartesian Hessian readers
    """
    hess_progs = _programs_with_attribute(
        'cartesian_hessian_reader')

    return hess_progs


def internal_hessian_programs():
    """ get the list of programs implementing internal Hessian readers
    """
    hess_progs = _programs_with_attribute(
        'internal_hessian_reader')

    return hess_progs


# Functions called to retrieve the Hessian #

def cartesian_hessian(prog, output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """
    assert prog in cartesian_hessian_programs()
    module = _import_module(prog)
    cart_hess = module.cartesian_hessian_reader(output_string)

    return cart_hess


def internal_hessian(prog, output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """
    assert prog in internal_hessian_programs()
    module = _import_module(prog)
    int_hess = module.internal_hessian_reader(output_string)

    return int_hess


# FUNCTIONS TO RETRIEVE GRADIENT #


def cartesian_gradient_programs():
    """ get the list of programs implementing cartesian Hessian readers
    """
    grad_progs = _programs_with_attribute(
        'cartesian_gradient_reader')

    return grad_progs


def internal_gradient_programs():
    """ get the list of programs implementing internal Hessian readers
    """
    grad_progs = _programs_with_attribute(
        'internal_gradient_reader')

    return grad_progs


# Functions called to retrieve the gradient #

def cartesian_gradient(prog, output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """
    assert prog in cartesian_gradient_programs()
    module = _import_module(prog)
    cart_grad = module.cartesian_gradient_reader(output_string)

    return cart_grad


def internal_gradient(prog, output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """
    assert prog in internal_hessian_programs()
    module = _import_module(prog)
    int_grad = module.internal_hessian_reader(output_string)

    return int_grad


# FUNCTIONS TO RETRIEVE IRC INFORMATION #


def irc_geometries_programs():
    """ get the list of programs implementing cartesian Hessian readers
    """
    irc_progs = _programs_with_attribute(
        'irc_geometries_reader')

    return irc_progs


# Functions called to retrieve the irc #


def irc_geometries_reader(prog, output_string):
    """ Retrieves the optimized geometry in Cartesian xyz coordinates.
        Units of Angstrom.
    """
    assert prog in irc_geometries_programs()
    module = _import_module(prog)
    irc_geoms = module.irc_geometries_reader(output_string)

    return irc_geoms
