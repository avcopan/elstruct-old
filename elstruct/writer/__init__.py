"""
Modules to write input files for electronic structure codes
"""

import importlib
from ..params import PROGRAM


__authors__ = "Kevin Moore and Andreas Copan"
__updated__ = "2019-01-21"


PACKAGE = 'elstruct.writer'
PROGRAM_MODULE_NAMES = {
    PROGRAM.GAUSSIAN: 'gaussian',
    PROGRAM.MOLPRO: 'molpro'
}


# FUNCTIONS TO IMPORT AND CHECK FOR WRITER MODULES #

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


# FUNCTIONS TO WRITE SINGLE POINT ENERGY JOBS #

def energy_programs():
    """ get the list of programs implementing hamonic frequency readers
    """

    energy_progs = _programs_with_attribute('energy_writer')

    return energy_progs


def energy(prog,
           method, basis,
           coords, coord_sys,
           charge, mult,
           memory=8, nprocs=1,
           comment='Single Point Energy',
           scf_options='None', corr_options='None'
           ):
    """ Writes an input file for a single-point energy computation.
    """

    assert prog in energy_programs()

    module = _import_module(prog)
    ENERGY_JOB_STR = module.single_point_energy_writer(
        method, basis,
        coords, coord_sys,
        charge, mult,
        memory, nprocs,
        comment,
        scf_options, corr_options)

    return ENERGY_JOB_STR


# FUNCTIONS TO WRITE OPTIMIZATION AND HARMONIC FREQUENCY JOBS #

def opt_and_freq_programs():
    """ get the list of programs implementing hamonic frequency readers
    """

    energy_progs = _programs_with_attribute('opt_and_harm_freq_writer')

    return energy_progs


def opt_and_harm_freq(prog,
                      method, basis,
                      coords, coord_sys,
                      charge, mult,
                      memory=8, nprocs=1,
                      comment='Optimization and Harmonic Frequency',
                      scf_options='None', corr_options='None',
                      opt_options='None', freq_options='None'
                      ):
    """ Writes an input file for an optimization 
        and harmonic frequency computation.
    """

    assert prog in opt_and_freq_programs()

    module = _import_module(prog)
    OPT_FREQ_JOB_STR = module.opt_and_harm_freq_writer(
        method, basis,
        coords, coord_sys,
        charge, mult,
        memory, nprocs,
        comment,
        scf_options, corr_options,
        opt_options, freq_options)

    return OPT_FREQ_JOB_STR
