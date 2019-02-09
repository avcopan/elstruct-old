""" interface to the writers for each program
"""
from .. import params as par


def geometry_molecule_specifier(geo, charge=0, mult=None, head=None,
                                foot=None):
    """ molecule descriptor, cartesian coordinates
    """
    # automatically guess the high-spin multiplicity, if None
    task = (
        par.TASK.MOLECULE.KEY,
        {
            par.TASK.MOLECULE.GEOM_KEY: geo,
            par.TASK.MOLECULE.CHAR_KEY: charge,
            par.TASK.MOLECULE.MULT_KEY: mult,
            par.TASK.MOLECULE.HEAD_KEY: head,
            par.TASK.MOLECULE.FOOT_KEY: foot
        }
    )
    return task


def zmatrix_molecule_specifier(zma, charge=0, mult=None, head=None, foot=None):
    """ molecule descriptor, internal coordinates
    """
    # automatically guess the high-spin multiplicity, if None
    task = (
        par.TASK.MOLECULE.KEY,
        {
            par.TASK.MOLECULE.ZMAT_KEY: zma,
            par.TASK.MOLECULE.CHAR_KEY: charge,
            par.TASK.MOLECULE.MULT_KEY: mult,
            par.TASK.MOLECULE.HEAD_KEY: head,
            par.TASK.MOLECULE.FOOT_KEY: foot
        }
    )
    return task
