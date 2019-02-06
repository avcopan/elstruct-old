
MEMORY/COMMENT BLOCK (STRONGLY RECOMMENDED)
----------------------------
# ${comment}

memory ${memory} GB
----------------------------


MOLECULE BLOCK (REQUIRED)
----------------------------
molecule{
${charge} ${mult}
${geom}
units angstrom
}
----------------------------


THEORETICAL METHOD BLOCK (REQUIRED) 
----------------------------
set basis ${basis}
set reference ${reference}
set scf_type pk

----------------------------


JOB TYPE BLOCKS (CHOOSE ONE OR MORE)
++++++++++++++++++++++++++++

ENERGY BLOCK
----------------------------
energy('${method}')
----------------------------

OPTIMIZATION BLOCK 
----------------------------
optimize('${method}')
----------------------------

TS OPTIMIZATION BLOCK 
----------------------------
set opt_type ts
optimize('${method}')
----------------------------

GRADIENT BLOCK
----------------------------
G, wfn = gradient('${method}', return_wfn=True)
wfn.gradient().print_out()
----------------------------

HARMONIC FREQ BLOCK
----------------------------
E, wfn = frequencies('${method}', return_wfn=True)
wfn2.hessian().print_out()
----------------------------

++++++++++++++++++++++++++++


SPECIAL OPTIONS BLOCK
---------------------------
${special_options}
---------------------------


