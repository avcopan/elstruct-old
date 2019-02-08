%Mem=${memory}GB
%NProcShared=${nprocs}
if ${checkpoint_name} is notempty:
%Chk=${checkpoint_name}
$ how to escape percent signs?

#N ${reference} ${method}/${basis}
% if ${method} == dft:
# Integral(Grid={intgrid})
% if ${scf_options} == notempty:
# ${scf_options}
Q: scf_options like SCF=(xqc) and/or NoSymmetry

${comment}

${charge} ${mult}
${geom}

${special_options}

