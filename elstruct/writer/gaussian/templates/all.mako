
MEMORY/COMMENT BLOCK (STRONGLY RECOMMENDED)
----------------------------
%Mem=${memory}GB
%NProcShared=${nprocs}
if ${checkpoint_name} is notempty:
%Chk=${checkpoint_name}
$ how to escape percent signs?
----------------------------


THEORETICAL METHOD BLOCK (REQUIRED) 
----------------------------
#N ${reference} ${method}/${basis}
% if ${method} == dft:
# Integral(Grid={intgrid})
% if ${scf_options} == notempty:
# ${scf_options}
Q: scf_options like SCF=(xqc) and/or NoSymmetry
----------------------------


JOB TYPE BLOCKS (CHOOSE ONE OR MORE)
++++++++++++++++++++++++++++

OPTIMIZATION BLOCK 
----------------------------
% if ${opt_options} == notempty:
# Opt=(${opt_methods})
% else
# Opt 
Q: can opt work as Opt=()?
----------------------------

TS OPTIMIZATION BLOCK 
----------------------------
% if ${opt_options} == notempty:
# Opt=(TS,CalcFC,${opt_methods})
% else
# Opt=(TS,CalcFC) 
----------------------------

GRADIENT BLOCK
----------------------------
# Force
----------------------------

HARMONIC FREQ BLOCK
----------------------------
# Freq
----------------------------

ANHARMONIC FREQ BLOCK
----------------------------
# Freq=(Anharmonic,VibRot,ReadAnharm)
----------------------------

IRC BLOCK 
----------------------------
% if ${irc_options} == notempty:
# IRC=(${irc_direction},${irc_options}
% else:
# IRC=(${irc_direction})
----------------------------

++++++++++++++++++++++++++++


MOLECULE/COMMENT BLOCK (REQUIRED)
----------------------------

${comment}

${charge} ${mult}
${geom}
---------------------------


SPECIAL OPTIONS BLOCK
---------------------------
${special_options}
---------------------------


