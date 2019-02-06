
MEMORY/COMMENT BLOCK (STRONGLY RECOMMENDED)
----------------------------
%Mem=${memory}GB
%NProcShared=${nprocs}
----------------------------


THEORETICAL METHOD BLOCK (REQUIRED) 
----------------------------
#N ${reference} ${method}/${basis}
% if ${method} == dft:
# Integral(Grid={intgrid})
----------------------------


JOB TYPE BLOCKS (CHOOSE ONE OR MORE)
++++++++++++++++++++++++++++

OPTIMIZATION BLOCK 
----------------------------
# Opt 
----------------------------

TS OPTIMIZATION BLOCK 
----------------------------
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
# Freq=(Anharmonic,VibRot,ReadAnharm
----------------------------

IRC BLOCK 
----------------------------
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

