"""
Modules to write input files for electronic structure codes
"""

import importlib
from ..params import PROGRAM


__authors__ = "Kevin Moore and Andreas Copan"
__updated__ = "2019-01-21"


PACKAGE = 'elstruct.writer'
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
    """ get the list of programs implementing hamonic frequency readers
    """

    energy_progs = _programs_with_attribute('single_point_energy_writer')

    return energy_progs


def energy(prog, input_file_name,
           method, basis,
           coords, coord_sys,
           charge, mult,
           memory=8, nprocs=1,
           comment='Single Point Energy'
           ):
    """ Writes an input file for a single-point energy computation.
    """

    assert prog in energy_programs()

    module = _import_module(prog)
    ENERGY_JOB_STR = module.single_point_energy_writer(
        prog, input_file_name,
        method, basis,
        coords, coord_sys,
        charge, mult,
        memory, nprocs,
        comment)

    return ENERGY_JOB_STR 


def opt_and_freq_programs():
    """ get the list of programs implementing hamonic frequency readers
    """

    energy_progs = _programs_with_attribute('opt_and_harm_freq_writer')

    return energy_progs


def opt_and_harm_freq(prog, input_file_name,
                      method, basis,
                      coords, coord_sys,
                      charge, mult,
                      memory=8, nprocs=1,
                      comment='Single Point Energy'
                      ):
    """ Writes an input file for a single-point energy computation.
    """

    assert prog in opt_and_freq_programs()

    module = _import_module(prog)
    OPT_FREQ_JOB_STR = module.opt_and_harm_freq_writer(
        prog, input_file_name,
        method, basis,
        coords, coord_sys,
        charge, mult,
        memory, nprocs,
        comment)

    return OPT_FREQ_JOB_STR 


