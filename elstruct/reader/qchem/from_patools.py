
def qchem_geo(lines):
    xyz = ''
    try:
        if 'OPTIMIZATION CONVERGED' in lines:
            lines = lines.split('OPTIMIZATION CONVERGED')[1]
            lines = lines.split('\n\n')[1]
            lines = lines.splitlines(True)[2:]
            for line in lines:
                line = line.split()
                xyz += ' ' + line[1] + '  ' + line[2] + '  ' + line[3] + '  ' + line[4] +'\n' 
    except:
        logging.error('Cannot parse xyz')
    return xyz

def qchem_xyz(lines):
    geo = qchem_geo(lines) 
    if geo:
        n   = str(len(geo.splitlines()))
        xyz = n + '\n\n' +  geo
    else:
        xyz = ''
    return xyz
   
def qchem_energy(lines):
    energy  = 'Final energy is\s*([\d,\.,-]*)' 
    energy  = re.findall(energy,lines)
    if len(energy) < 1:
        energy  = 'energy in the final basis set =\s*([\d,\.,-]*)'
        energy  = re.findall(energy,lines)
    return float(energy[-1])

def qchem_method(lines):
    method  = 'method\s*(\S*)' 
    method  = re.findall(method,lines)
    return  method[-1]

def qchem_basisset(lines):
    method  = 'Requested basis set is\s*(\S*)' 
    method  = re.findall(method,lines)
    return  method[-1].lower()

def qchem_freqs(lines):
    """
    Return harmonic frequencies.
    """
    kw = 'Frequency: (.+)'
    freqlines = re.findall(kw, lines)
    freqs = []
    for line in freqlines:
        freqs.extend(line.split())
    return freqs

def qchem_zpve(lines):

    zpve = 'Zero point vibrational energy:\s*([\d,\.,\-]*)'
    zpve = re.findall(zpve, lines)
    if len(zpve) > 0:
        return float(zpve[-1]) / ut.au2kcal
    return 0.0 

def qchem_calc(lines):
    if 'OPTIMIZATION COMPLETE' in lines:
        return 'geometry optimization'
    else:
        return ''
##############################################
############     EStokTP PARSER    ###########
##############################################

def EStokTP_freqs(lines):
    """
    Pulls the frequencies out from EStokTP me output file 
    INPUT:
    lines -    lines from EStokTP output file (reac1_fr.me or reac1_unpfr.me)
    OUTPUT:
    freqs    - frequencies obtained from output file
    """
    import numpy as np
 
    lines  = lines.strip('\n')
    lines  = lines.split('[1/cm]')[1].split('Zero')[0] 
    lines  = lines.split()
    nfreqs = lines[0]
    freqs  = lines[1:]
    freqs  = np.array(map(float, freqs))
    freqs  = np.sort(freqs)[::-1]
    return freqs.tolist()

###########################
#####  FOR GENERAL ########
############################

def method(lines):
    prog = get_prog(lines)
    if prog == 'gaussian':
        return gaussian_method(lines)
    if prog == 'molpro':
        return molpro_method(lines)
    print 'program not recognized as gaussian or molpro'
    return

def basisset(lines):
    prog = get_prog(lines)
    if prog == 'gaussian':
        return gaussian_basisset(lines)
    if prog == 'molpro':
        return molpro_basisset(lines)
    print 'program not recognized as gaussian or molpro'
    return

def energy(lines):
    prog = get_prog(lines)
    if prog == 'gaussian':
        return gaussian_energy(lines)
    if prog == 'molpro':
        return molpro_energy(lines)
    print 'program not recognized as gaussian or molpro'
    return

def zmat(lines):
    prog = get_prog(lines)
    if prog == 'gaussian':
        return gaussian_zmat(lines)
    if prog == 'molpro':
        return molpro_zmat(lines)
    print 'program not recognized as gaussian or molpro'
    return

def freqs(lines):
    prog = get_prog(lines)
    if prog == 'gaussian':
        return gaussian_freqs(lines)
    if prog == 'molpro':
        return molpro_freqs(lines)
    print 'program not recognized as gaussian or molpro'
    return

def zpve(lines):
    prog = get_prog(lines)
    zpve = 0.
    if prog == 'gaussian':
        zpve = gaussian_zpve(lines)
    elif prog == 'molpro':
        zpve = molpro_zpve(lines)
    else:
        'program not recognized as gaussian or molpro'
    return 0.0

def anzpve(lines):
    prog = get_prog(lines)
    if prog == 'gaussian':
        return gaussian_anzpve(lines)
    if prog == 'molpro':
       return #molpro_anzpve(lines)
    print 'program not recognized as gaussian or molpro'
    return 

def xyz(lines):
    prog = get_prog(lines)
    if prog == 'gaussian':
        return gaussian_xyz(lines)
    if prog == 'molpro':
        return molpro_xyz(lines)
    print 'program not recognized as gaussian or molpro'
    return

def geo(lines):
    prog = get_prog(lines)
    if prog == 'gaussian':
        return gaussian_geo(lines)
    if prog == 'molpro':
        return molpro_geo(lines)
    print 'program not recognized as gaussian or molpro'
    return

def rotconsts(lines):
    prog = get_prog(lines)
    if prog == 'gaussian':
        return gaussian_rotconsts(lines)
    if prog == 'molpro':
        return molpro_rotconsts(lines)
    print 'program not recognized as gaussian or molpro'
    return

def get_298(lines):
    deltaH298 = ' h298 final\s*([\d,\-,\.]*)'
    lines = lines.splitlines()
    tmp = ''
    for line in lines:
        if 'h298 final' in line:
            tmp = float(line.split()[-1])
    return tmp
    
