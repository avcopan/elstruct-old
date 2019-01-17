***,${comment}

memory,${memory},m
gthresh,orbital=1.d-${thresh_log}

angstrom
Geometry = {
${geom}
}

basis=${basis}
set,spin=${spin}
set,charge=${charge}

{rhf,maxit=${niter}}

%if spin == 0:
{ccsd,maxit=${niter}}
%else:
{uccsd,maxit=${niter}}
%endif
