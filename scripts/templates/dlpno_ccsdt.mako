#${name}
% pal nprocs 8 end
% MaxCore 12500
! RHF DLPNO-CCSD(T) cc-pVDZ 
! AutoAux RIJCOSX GridX5   
! TightSCF TightPNO
%base"/scratch/kmoore/test1" 
* xyz 0 ${mult}
${geom}
*
$new_job
#${name}
% pal nprocs 8 end
% MaxCore 12500
! RHF DLPNO-CCSD(T) cc-pVTZ 
! AutoAux RIJCOSX GridX5   
! TightSCF TightPNO
%base"/scratch/kmoore/test1" 
* xyz 0 ${mult}
${geom}
*
$new_job
#${name}
% pal nprocs 8 end
% MaxCore 12500
! RHF DLPNO-CCSD(T) cc-pVQZ 
! AutoAux RIJCOSX GridX5   
! TightSCF TightPNO
%base"/scratch/kmoore/test1" 
* xyz 0 ${mult}
${geom}
*
$new_job
#${name}
% pal nprocs 8 end
% MaxCore 12500
! RHF DLPNO-CCSD(T) cc-pV5Z 
! AutoAux RIJCOSX GridX5   
! TightSCF TightPNO
%base"/scratch/kmoore/test1" 
* xyz 0 ${mult}
${geom}
*

