""" common parameters
"""

__authors__ = "Kevin Moore and Andreas Copan"
__updated__ = "2019-01-11"


class METHOD():
    """ Ab initio electronic structure methods
    """
    # Hartree-Fock methods #
    RHF = 'rhf'
    UHF = 'uhf'
    ROHF = 'rohf'
    # Single-reference correlated methods #
    RHF_MP2 = 'rhf-mp2'
    UHF_UMP2 = 'uhf-ump2'
    ROHF_RMP2 = 'rohf-rmp2'
    RHF_CCSD = 'rhf-ccsd'
    ROHF_UCCSD = 'rohf-uccsd'
    ROHF_RCCSD = 'rohf-rccsd'
    RHF_CCSD_T = 'rhf-ccsd(t)'
    ROHF_UCCSD_T = 'rohf-uccsd(t)'
    ROHF_RCCSD_T = 'rohf-rccsd(t)'
    # Custom, user-defined method #
    CUSTOM = 'custom'
    OPT = 'opt'

class STRUCTURE():
    """ Types of molecular structure
    """
    # Geometry #
    OPT_GEOM_XYZ = 'opt_geom_xyz'
    OPT_GEOM_INT = 'opt_geom_internal'
    INIT_GEOM_XYZ = 'init_geom_xyz'
    INIT_GEOM_INT = 'init_geom_internal'
    # Rotational Constants #
    EQUIL_ROT_CONST = 'equil_rot_constant'

class FREQUENCY():
    """ Frequency Information
    """    
    HARM_FREQ = 'harm_freq'
    ANHARM_FREQ = 'anharm_freq'
    HARM_ZPVE = 'harm_zpve'
    ANHARM_ZPVE = 'anharm_zpve'
    ANHARM_MATRIX = 'anharm_matrix'
    CENTRIG_DIST_CONST = 'centrig_dist_const'
    VIBROT_MATRIX = 'vibrot_matrix'
    
class SURFACE():
    """ Information about the Potential Energy Surface
    """
    GRADIENT_XYZ = 'grad_xyz'
    GRADIENT_INT = 'grad_internal'
    HESSIAN_XYZ = 'hessian_xyz'
    HESSIAN_INT = 'hessian_int'

class PROPERTY():
    """ Molecular Properties of interest
    """
    DIPOLE_MOM = 'dipole_moment'

class JOBTYPE():
    """ Various job types
    """
    SINGLE_POINT_ENERGY = 'sp_energy'
    OPTIMIZATION = 'opt'
    HARM_VIB_FREQ = 'harm_vib_freq'
    ANHARM_VIB_FREQ = 'anharm_vib_freq'
    OPT_AND_HARM_FREQ = 'opt_and_freq'
    CUSTOM_JOB = 'custom_job'

class PROGRAM():
    """ Programs to be called
    """
    CFOUR = 'cfour2'
    GAUSSIAN = 'gaussian09'
    MOLPRO = 'molpro2015'
    MOLPRO_MPPX = 'molpro2015-mppx'
    MRCC = 'mrcc2018'
    NWCHEM = 'nwchem6'
    ORCA = 'orca4'
    PSI4 = 'psi4'
    QCHEM = 'qchem'

class FILE_EXTENSION():
    """ Data file extensions
    """
    ENERGY = '.energ'
    HARMONIC_FREQUENCIES = '.harmfreq'
    HARMONIC_ZERO_POINT_VIBRATIONAL_ENERGY = '.harmzpve'
    CARTESIAN_GEOMETRY = '.xyz'
