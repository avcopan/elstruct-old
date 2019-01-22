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
from ... import params
from elstruct._dot_xyz import from_geometry

# Variables to set the names and paths to job-file templates

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')


# Format user options to place into the input file

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


# Write input file by filling in Mako template with user-options

def template_filler(template_name, **fill_vals):
    """ Fills in the template file with
    """

    # Set the path of the template file
    template_file = os.path.join(TEMPLATE_PATH, template_name)

    # Write a string consisting of template filled with the dictionary vals
    filled_string = Template(filename=template_file).render(**fill_vals)

    return filled_string


def single_point_energy_writer(prog, input_file_name,
                               method, basis,
                               coords, coord_sys,
                               charge, mult,
                               memory, nprocs,
                               comment='Single Point Energy'):
    """ Writes an input file for a single-point energy computation.
    """

    # Format level of theory to place into template
    scf_method, corr_method = get_method(method)

    # Format geometry to place into template
    geom_init = from_geometry(coords)
    geom = "\n".join(geom_init.split("\n")[2:-1])

    # Set/Augment variables to place into template
    spin = mult - 1
    memory = int(memory * (1000.0 / 8.0))

    # Establish a dictionary to fill in the template
    energy_vals = {
        'corr_method': corr_method,
        'scf_method': scf_method,
        'basis': basis,
        'geom': geom,
        'coord_sys': coord_sys,
        'charge': charge,
        'spin': spin,
        'memory': memory,
        'comment': comment
    }

    # Obtain a string with substituted template
    template_name = 'single_point_energy.mako'
    energy_string = template_filler(template_name, **energy_vals)

    return energy_string

 
def opt_and_harm_freq_writer(prog, input_file_name,
                             method, basis,
                             coords, coord_sys,
                             charge, mult,
                             memory, nprocs,
                             comment='Single Point Energy'):
    """ Writes an input file for a single-point energy computation.
    """

    # Format level of theory to place into template
    scf_method, corr_method = get_method(method)

    # Format geometry to place into template
    geom_init = from_geometry(coords)
    geom = "\n".join(geom_init.split("\n")[2:-1])

    # Set/Augment variables to place into template
    spin = mult - 1
    memory = int(memory * (1000.0 / 8.0))

    # Establish a dictionary to fill in the template
    energy_vals = {
        'corr_method': corr_method,
        'scf_method': scf_method,
        'basis': basis,
        'geom': geom,
        'coord_sys': coord_sys,
        'charge': charge,
        'spin': spin,
        'memory': memory,
        'comment': comment
    }

    # Obtain a string with substituted template
    template_name = 'opt_and_harm_freq.mako'
    opt_and_freq_string = template_filler(template_name, **energy_vals)

    return opt_and_freq_string
# def optimization_writer():
#     """ Writes input file for a geometry optimization.
#     """
#
#     return opt_string
#
#
# def harm_freq_writer():
#     """ Writes input file for a harmonic vibrational-frequency computation.
#     """
#
#     return harm_freq_string
#
#
# def opt_and_harm_freq_writer():
#     """ Writes input file for a combined geometry-optimization and
#         harmonic vibrational-frequency computation.
#     """
#
#     return opt_and_harm_freq_string
#
#
# def custom_job_writer():
#     """ Writes input file for custom job with special user-defined inputs.
#     """
#
#     return custom_job_string
