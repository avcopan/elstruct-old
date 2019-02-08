
MEMORY/COMMENT BLOCK (STRONGLY RECOMMENDED)
----------------------------
***,${comment}
memory,${memory},m
----------------------------


MOLECULE BLOCK (REQUIRED)
----------------------------
angstrom
geometry = {
${geom}
}

set,spin=${spin}
set,charge=${charge}
----------------------------


THEORETICAL METHOD BLOCK (REQUIRED) 
----------------------------
basis=${basis}

{${scf_method},${scf_options}
${scf_directives}
}

% if corr_method != 'none':
{${corr_method}, ${corr_options}
${corr_directives}
}
% endif
----------------------------


JOB TYPE BLOCKS (CHOOSE ONE OR MORE)
++++++++++++++++++++++++++++

OPTIMIZATION BLOCK 
----------------------------
{optg,${opt_options}
}
----------------------------

TS OPTIMIZATION BLOCK 
----------------------------
{optg,root=2,${opt_options}
}
----------------------------

GRADIENT BLOCK
----------------------------
{force}
----------------------------

HARMONIC FREQ BLOCK
----------------------------
{freq, ${freq_options}
 print,hessian
}
----------------------------

++++++++++++++++++++++++++++

SPECIAL OPTIONS BLOCK
----------------------------
${special_options}
----------------------------



