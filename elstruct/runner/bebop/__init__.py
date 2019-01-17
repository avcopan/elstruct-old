""" function to submit input file all electronic structure codes to Bebop queue
"""

import os
import subprocess
from mako.template import Template
from ... import params


# Obtain the path to the directory containing the templates
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')

# Dictionary containing the names of the template files
TEMPLATE_FILES = {
    params.PROGRAM.CFOUR: 'cfour2.mako',
    params.PROGRAM.GAUSSIAN: 'psi4.mako',
    params.PROGRAM.MOLPRO: 'molpro2015.mako',
    params.PROGRAM.MOLPRO_MPPX: 'molpro2015-mppx.mako',
    params.PROGRAM.MRCC: 'mrcc2018.mako',
    params.PROGRAM.NWCHEM: 'nwchem6.mako',
    params.PROGRAM.ORCA: 'orca4.mako',
    params.PROGRAM.PSI4: 'psi4.mako',
}


def submit(program, account, partition='bdwall', nnodes=1, njobs=1, ncores_per_node=1,
           walltime='2:00:00', jobname='run', input_name=None, output_name=None,
           scratch='/scratch/$USER', auto_submit=True, background=False):
    ''' Function writes a Bebop job submission script by filling in various templates for
        electronic structure programs and then submits the job.
    '''

    # Checks if requested program is in list of supported template files
    if program not in TEMPLATE_FILES.keys():
        raise ValueError('Program requested is not currently supported')

    # Dictionary containing all potential variables to be fed into the template
    fill_vals = {
        'program': program,
        'account': account,
        'partition': partition,
        'nnodes': nnodes,
        'njobs': njobs,
        'ncores_per_node': ncores_per_node,
        'walltime': walltime,
        'jobname': jobname,
        'input': input_name,
        'output': output_name,
        'scratch': scratch,
        'auto_submit': ('yes' if auto_submit else 'no'),
        'background': ('yes' if background else 'no'),
    }

    # Check if input file exists
    #if os.path.exists('./'+input_name) == False:
    #    raise ValueError('Input file does not exist in current submission directory')

    # Check njobs > 2 and set appropriate variables and flag errors
    if njobs > 1 and nnodes > 1:
        raise ValueError("Multiple job runs only allowed for a SINGLE NODE")
    if njobs > 1 and program != "molpro2015":
        raise ValueError("njobs > 1 only supported for molpro2015 calculations")

    # Determine the TOTAL number of cores for calling MPI; if needed
    fill_vals["ncores_total"] = nnodes * ncores_per_node

    # Sets the name of the input flle and outfile based on the user request
    if fill_vals["input"] is None and fill_vals["output"] is None:
        fill_vals["input"] = 'input.dat'
        fill_vals["output"] = 'output.dat'
    elif fill_vals["input"] is not None and fill_vals["output"] is None:
        fill_vals["output"] = os.path.splitext(fill_vals["input"])[0] + '.out'
    elif fill_vals["input"] is None and fill_vals["output"] is not None:
        fill_vals["input"] = 'input.dat'

    # Obtain the name of the template corresponding to the requested electronic structure job
    template_file_name = TEMPLATE_FILES[program]
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    # Create template object with the user-requested options
    substituted_template = Template(filename=template_file_path).render(**fill_vals)

    # Write the submission script in the working directory
    job_submission_file = 'run_'+program+'_bebop.sh'
    with open(job_submission_file, 'w') as submissionfile:
        submissionfile.write(substituted_template)

    # Immediately submit the job if the submit option set to true
    if auto_submit:
        subprocess.check_call(['sbatch', job_submission_file])
      #print('Job submitted to Bebop partition: '+partition+'\n')
