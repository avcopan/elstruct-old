# ${comment}

memory ${memory} GB

molecule{
${charge} ${mult}
${geom}
units angstrom
}

set basis ${basis}
set d_convergence ${thresh_log}
set maxiter ${niter}
set scf_type pk

%if mult == 1:
set reference rhf
%else:
set reference rohf
%endif

energy('scf')
