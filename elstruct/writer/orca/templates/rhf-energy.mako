# ${comment}

% pal nprocs ${nprocs} end
% MaxCore ${memory} 

! RHF 
! ${basis}

% scf
MaxIter ${niter}
end 

* ${coord_sys} ${charge} ${mult}
${geom}
*

