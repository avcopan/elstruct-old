"""
Library of innput file writers for Molpro 2015

Jobs currently supported:
(1) Single-point energy computation;
(2) geometry optimization;
(3) harmonic vibrational frequency computation;
(4) compined optimization and harmonic frequency computation; and
(5) custom job with special, user-defined options

"""

__authors__ = "Kevin Moore and Andreas Copan"
__updated__ = "2019-01-11"

import os
from mako.template import Template
from elstruct._dot_xyz import from_geometry


# SET PATH TO THE TEMPLATE FILES #

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')


# FUNCTIONS TO FORMAT VALUES APPROPRIATE FOR MOLPRO FILES #

def get_method(method):
    """ Parse method to set level of theory
    """

    if any(scf in method for scf in ('rhf-', 'uhf-', 'rohf-')):
        scf_method = method.split('-')[0]
        corr_method = method.split('-')[1]
    else:
        scf_method = method
        corr_method = 'none'

    return scf_method, corr_method


def get_geom(coords, coord_sys):
    """
    Writes a geometry file
    """

    # Read the geometry from the file
    geom_init = from_geometry(coords)

    # Format geometry to place into template
    if coord_sys == 'xyz':
        geom = "\n".join(geom_init.split("\n")[2:-1])
    elif coord_sys == 'int':
        geom = 'BOOO'
    else:
        geom = 'More BOO'

    return geom


def get_spin(mult):
    """
    Converts multiplicity to spin (2S) used by Molpro
    """

    spin = mult - 1

    return spin


def get_memory(memory_gb):
    """
    Converts memory in GB to MegaWords
    """

    memory_mw = int(memory_gb * (1000.0 / 8.0))

    return memory_mw


# FUNCTION TO BUILD DICTIONARIES USED TO FILL THE TEMPLATES #

def get_energy_vals_dict(method, basis,
                         coords, coord_sys,
                         charge, mult,
                         memory, comment):
    """
    Get the values to build an energy job which is the beginning of all jobs
    """

    # Obtain various quantities to place into the template
    scf_method, corr_method = get_method(method)
    geom = get_geom(coords, coord_sys)
    spin = get_spin(mult)
    memory_mw = get_memory(memory)

    energy_vals = {
        'corr_method': corr_method,
        'scf_method': scf_method,
        'basis': basis,
        'geom': geom,
        'coord_sys': coord_sys,
        'charge': charge,
        'spin': spin,
        'memory': memory_mw,
        'comment': comment
    }

    return energy_vals


# FUNCTION TO FILL THE TEMPLATE WITH ALL THE DESIRED VALUES #

def template_filler(template_name, **fill_vals):
    """ Fills in the template file with
    """

    # Set the path of the template file
    template_file = os.path.join(TEMPLATE_PATH, template_name)

    # Write a string consisting of template filled with the dictionary vals
    filled_string = Template(filename=template_file).render(**fill_vals)

    return filled_string


# FUNCTIONS TO WRITE STRINGS FOR EACH MOLPRO JOB TYPE #

def energy_writer(method, basis,
                  coords, coord_sys,
                  charge, mult,
                  memory, nprocs,
                  comment):
    """ Writes an input file for a single-point energy computation.
    """

    # Establish a dictionary to fill in the template
    energy_vals = get_energy_vals_dict(method, basis,
                                       coords, coord_sys,
                                       charge, mult,
                                       memory, comment)

    # Obtain a string with substituted template
    template_name = 'energy.mako'
    energy_string = template_filler(template_name, **energy_vals)

    return energy_string


def opt_and_harm_freq_writer(method, basis,
                             coords, coord_sys,
                             charge, mult,
                             memory, nprocs,
                             comment):
    """ Writes an input file for a single-point energy computation.
    """

    # Establish a dictionary to fill in the template
    energy_vals = get_energy_vals_dict(method, basis,
                                       coords, coord_sys,
                                       charge, mult,
                                       memory, comment)

    # Obtain a string with substituted template
    template_name = 'opt_and_harm_freq.mako'
    opt_and_freq_string = template_filler(template_name, **energy_vals)

    return opt_and_freq_string
