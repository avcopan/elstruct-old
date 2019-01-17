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
from ...util import xyz_string
from ... import params


#### Variables to set the names and paths to job-file templates #####

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')

TEMPLATE_NAMES = {
    params.JOBTYPE.SINGLE_POINT_ENERGY: 'single_point_energy.mako'
    params.JOBTYPE.OPTIMIZATION: 'optimization.mako'
    params.JOBTYPE.HARM_VIB_FREQ: 'harm_vib_freq.mako'
    params.JOBTYPE.OPT_AND_HARM_FREQ: 'opt_and_harm_freq.mako'
    params.JOBTYPE.CUSTOM_JOB: 'custom.mako'
}


##### Series of functions to read the electronic energy #####

def template_filler(job_type, **fill_vals): 

    # Set the path of the template file 
    template_file = os.path.join(TEMPLATE_PATH, TEMPLATE_FILES[job_type])

    # Write a string consisting of the template file filled with the dictionary vals
    filled_string = Template(filename=template_file).render(**fill_vals)

    return filled_string

def sp_energy_writer():
    """ Writes an input file for a single-point energy computation.
    """ 

    # Augment the options to go into the template
    spin = mult - 1

    # Potential values to set
    #memory = int(memory * (1000.0 / 8.0))
    #'thresh_log': thresh_log,
    #'niter': niter,

    # Parse method to set level of theory

    # Establish a dictionary to fill in the template
    sp_energy_vals = {
        'geom': geom_str,
        'charge': charge,
        'spin': spin,
        'post_scf_method': post_scf_method,
        'scf_method': scf_method,
        'basis': basis,
        'comment': comment}
    }

    # Obtain a string with the filled file
    sp_energy_string = template_filler(job_type, **sp_energy_vals) 

    return sp_energy_string

def optimization_writer():
    """ Writes an input file for a geometry optimization.
    """ 
    
    return opt_string

def harm_freq_writer():
    """ Writes an input file for a harmonic vibrational-frequency computation.
    """ 

    return harm_freq_string

def opt_and_harm_freq_writer():
    """ Writes an input file for a combined geometry-optimization and 
        harmonic vibrational-frequency computation.
    """ 

    return opt_and_harm_freq_string

def custom_job_writer():
    """ Writes an input file for a custom job with special user-defined inputs .
    """ 

    return custom_job_string


##### Dictionary of functions to write the files for the user-desired job #####

JOB_WRITERS = {
    params.JOBTYPE.SINGLE_POINT_ENERGY: sp_energy_writer,
    params.JOBTYPE.OPTIMIZATION: optimization_writer,
    params.JOBTYPE.HARM_VIB_FREQ: harm_freq_writer,
    params.JOBTYPE.OPT_AND_HARM_FREQ: opt_and_harm_freq_writer,
    params.JOBTYPE.CUSTOM_JOB: custom_job_writer
}


##### Write function called by external scripts #####

def write_file(job_file_name, job_type, **job_params):
    """ Writes an input file for a Molpro 2015 job.
    """

    assert job_type in JOB_WRITERS.keys()

    # Obtain the string by accessing the appropriate function in the JOB_WRITERS dict
    job_string = JOB_WRITERS[job_type](job_type, **job_params)

    # Write the job file
    with open(job_file_name, 'w') as job_file:
        inputfile.write(job_string)

    return None
