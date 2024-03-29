"""
Set of dicts to change lines
"""

# CFOUR
OLD_LINES_CFOUR = {
    'rhf': ['CALC=HF', 'rhf'],
    'uhf': ['CALC=HF', 'uhf'],
    'rohf': ['CALC=HF', 'rohf']
}
NEW_LINES_CFOUR = {
    'rhf': [
        ['CALC=MP2\n', 'rhf-mp2'],
        ['CALC=CCSD\nCC_PROG=ECC\nABCDTYPE=AOBASIS\n', 'rhf-ccsd'],
        ['CALC=CCSD(T)\nCC_PROG=ECC\nABCDTYPE=AOBASIS\n', '"rhf-ccsd_t"'],
        ['CALC=CCSDT\nCC_PROG=NCC\nABCDTYPE=AOBASIS\n', 'rhf-ccsdt'],
        ['CALC=CCSDT(Q)\nCC_PROG=NCC\nABCDTYPE=AOBASIS\n', 'rhf-ccsdt_q']
    ],
    'uhf': [
        ['CALC=MP2\n', 'uhf-mp2'],
        ['CALC=CCSD\nCC_PROG=ECC\nABCDTYPE=AOBASIS\n', 'uhf-ccsd'],
        ['CALC=CCSD(T)\nCC_PROG=ECC\nABCDTYPE=AOBASIS\n', 'uhf-ccsd_t']
    ],
    'rohf': [
        ['CALC=MP2\n', 'rohf-mp2'],
        ['CALC=CCSD\nCC_PROG=VCC\nABCDTYPE=AOBASIS\n', 'rohf-ccsd'],
        ['CALC=CCSD(T)\nCC_PROG=VCC\nABCDTYPE=AOBASIS\n', 'rohf-ccsd_t']
    ]
}

# GAUSSIAN
OLD_LINES_GAUSSIAN = {
    'rhf': ['# RHF/cc-pVDZ', 'rhf'],
    'uhf': ['# UHF/cc-pVDZ', 'uhf'],
    'rohf': ['# ROHF/cc-pVDZ', 'rohf']
}
NEW_LINES_GAUSSIAN = {
    'rhf': [
        ['# RHF MP2/cc-pVDZ\n', 'rhf-mp2'],
        ['# RHF CCSD/cc-pVDZ\n', 'rhf-ccsd'],
        ['# RHF CCSD(T)/cc-pVDZ\n', 'rhf-ccsd_t'],
        ['# B2PLYPD3/cc-pVDZ\n', 'b2plypd3'],
        ['# B3LYP/cc-pVDZ\n', 'b3lyp'],
        ['# M062X/cc-pVDZ\n', 'm062x'],
        ['# wB97X-D/cc-pVDZ\n', 'wb97xd']
    ],
    'uhf': [
        ['# UHF MP2/cc-pVDZ\n', 'uhf-mp2'],
        ['# UHF CCSD/cc-pVDZ\n', 'uhf-ccsd'],
        ['# UHF CCSD(T)/cc-pVDZ\n', 'uhf-ccsd_t'],
    ],
    'rohf': [
        ['# ROHF MP2/cc-pVDZ\n', 'rohf-mp2'],
        ['# ROHF CCSD/cc-pVDZ\n', 'rohf-ccsd'],
        ['# ROHF CCSD(T)/cc-pVDZ\n', 'rohf-ccsd_t'],
    ]
}

# MOLPRO and MOLPRO-MPPX
OLD_LINES_MOLPRO = {
    'rhf': ['{rhf}', 'rhf'],
    'uhf': ['{uhf}', 'uhf'],
    'rohf': ['{rhf}', 'rohf']
}
NEW_LINES_MOLPRO = {
    'rhf': [
        ['{rhf}\n{mp2}\n', 'rhf-mp2'],
        ['{rhf}\n{ccsd}\n', 'rhf-ccsd'],
        ['{rhf}\n{ccsd(t)}\n', 'rhf-ccsd_t']
    ],
    'uhf': [
        ['{uhf}\n{ump2}\n', 'uhf-ump2']
    ],
    'rohf': [
        ['{rhf}\n{rmp2}\n', 'rohf-rmp2'],
        ['{rhf}\n{rccsd}\n', 'rohf-rccsd'],
        ['{rhf}\n{rccsd(t)}\n', 'rohf-rccsd_t'],
        ['{rhf}\n{uccsd}\n', 'rohf-uccsd'],
        ['{rhf}\n{uccsd(t)}\n', 'rohf-uccsd_t']
    ]
}

# MRCC
OLD_LINES_MRCC = {
    'rhf': ['calc=HF', 'rhf'],
    'uhf': ['calc=HF', 'uhf'],
    'rohf': ['calc=HF', 'rohf']
}
NEW_LINES_MRCC = {
    'rhf': [
        ['calc=MP2\n', 'rhf-mp2'],
        ['calc=CCSD\nccprog=ccsd\n', 'rhf-ccsd'],
        ['calc=CCSD(T)\nccprog=ccsd\n', 'rhf-ccsd_t'],
        ['calc=CCSDT\nccprog=mrcc\n', 'rhf-ccsdt'],
        ['calc=CCSDT(Q)\nccprog=mrcc\n', 'rhf-ccsdt_q'],
    ],
    'uhf': [
        ['calc=MP2\n', 'uhf-mp2'],
        ['calc=CCSD\nccprog=ccsd\n', 'uhf-ccsd'],
        ['calc=CCSD(T)\nccprog=ccsd\n', 'uhf-ccsd_t'],
        ['calc=CCSDT\nccprog=mrcc\n', 'uhf-ccsdt'],
        ['calc=CCSDT(Q)\nccprog=mrcc\n', 'uhf-ccsdt_q'],
    ],
    'rohf': [
        ['calc=MP2\n', 'rohf-mp2'],
        ['calc=CCSD\nccprog=ccsd\n', 'rohf-ccsd'],
        ['calc=CCSD(T)\nccprog=ccsd\n', 'rohf-ccsd_t'],
        ['calc=CCSDT\nccprog=mrcc\n', 'rohf-ccsdt'],
        ['calc=CCSDT(Q)\nccprog=mrcc\n', 'rohf-ccsdt_q'],
    ]
}


# ORCA
OLD_LINES_ORCA = {
    'rhf': ['! RHF', 'rhf'],
    'uhf': ['! UHF', 'uhf'],
    'rohf': ['! ROHF', 'rohf']
}
NEW_LINES_ORCA = {
    'rhf': [
        ['! RHF MP2\n', 'rhf-mp2'],
        ['! RHF CCSD\n', 'rhf-ccsd'],
        ['! RHF CCSD(T)\n', 'rhf-ccsd_t']
    ],
    'uhf': [
        ['! UHF MP2\n', 'uhf-mp2'],
        ['! UHF CCSD\n', 'uhf-ccsd'],
        ['! UHF CCSD(T)\n', 'uhf-ccsd_t']
    ],
    'rohf': [
        ['! ROHF MP2\n', 'rohf-mp2'],
        ['! ROHF CCSD\n', 'rohf-ccsd'],
        ['! ROHF CCSD(T)\n', 'rohf-ccsd_t']
    ]
}


# PSI4
OLD_LINES_PSI4 = {
    'rhf':  ["energy('scf')", 'rhf'],
    'uhf':  ["energy('scf')", 'uhf'],
    'rohf': ["energy('scf')", 'rohf']
}
NEW_LINES_PSI4 = {
}
