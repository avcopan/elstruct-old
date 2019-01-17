""" input file writers for MRCC
"""

import os
from mako.template import Template
from ...util import xyz_string
from ... import params

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = os.path.join(DIR_PATH, 'templates')

TEMPLATE_FILES = {
    params.METHOD.RHF: 'rhf-energy.mako',
}


def energy(theory, basis, labels, coords, charge=0, mult=1, niter=100,
           thresh_log=12, coord_sys='xyz', memory=8, nprocs=8,
           comment='Single Point Energy'):
    """ Writes a single-point energy input file for MRCC 2018.
    """


    assert theory in TEMPLATE_FILES.keys()

    geom_str = xyz_string(labels, coords)
    fill_vals = {
        'charge': charge,
        'mult': mult,
        'geom': geom_str,
        'basis': basis,
        'thresh_log': thresh_log,
        'niter': niter,
        'memory': memory,
        'nprocs': nprocs,
        'coord_sys': coord_sys,
        'comment': comment}

    template_file_name = TEMPLATE_FILES[theory]
    template_file_path = os.path.join(TEMPLATE_PATH, template_file_name)

    input_str = Template(filename=template_file_path).render(**fill_vals)
    return input_str
