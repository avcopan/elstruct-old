"""
Modules to run electronic structure codes on Blues and Bebop nodes
"""

import importlib
from ..params import NODES


__authors__ = "Kevin Moore and Andreas Copan"
__updated__ = "2019-01-21"


PACKAGE = 'elstruct.runner'


def blues(prog, nodes,
          njobs=1, ncores_per_node=1,
          input_name=None, output_name=None,
          scratch='/scratch/$USER',
          auto_submit=True, background=False):
    """ Submit job to Blues node.
    """

    module = importlib.import_module('.blues', PACKAGE)

    module.submit(prog, nodes,
                  njobs, ncores_per_node,
                  input_name, output_name,
                  scratch,
                  auto_submit, background)

    return None


def bebop(prog, account,
          partition='bdwall',
          nnodes=1, njobs=1,
          ncores_per_node=1,
          walltime='2:00:00',
          jobname='run',
          input_name=None, output_name=None,
          scratch='/scratch/$USER',
          auto_submit=True, background=False):
    """ Submit job to Bebop node.
    """

    module = importlib.import_module('.bebop', PACKAGE)
   
    module.submit(prog, account,
                  partition,
                  nnodes, njobs,
                  ncores_per_node,
                  walltime,
                  jobname,
                  input_name, output_name,
                  scratch,
                  auto_submit, background)

    return None
