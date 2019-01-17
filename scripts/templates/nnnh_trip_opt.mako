memory,1000,m
gthresh,energy=1.0d-10,orbital=1.0d-10

symmetry,z
angstrom
Geometry = {
N
N 1 r1
N 2 r2 1 a1
H 3 r3 2 a2 1 d1
}

! Parameters scanned in Grid; Constrained in Opt
r2  =  ${dist}           ! N-O Distance
a1  =  ${angle}          ! N-N-O Angle                    
! Optimized
r1  =  ${optdist}        ! N1-N2 Distance
r3  =  ${optdist2}       ! N3-H Distance
a2  =  ${optangle}       ! N2-N3-H Angle
! Constrain dihedral
d1  = 180.0

basis=aug-cc-pVDZ
{hf,maxit=1000
  wf,22,1,2,0}

do i=1,3
 w(i)=1d0
enddo
E1=0d0
E0=1d2

rs2cproc={
  do j=1,30 
    {multi,maxit=40;close,5;noextra;failsafe;
      wf,22,2,2;state,1;weight,w(1);
      wf,22,1,0;state,2;weight,w(2);
      wf,22,2,0;state,2;weight,w(3)}
    merg=energy
    E0=merg(1)

    if(abs(E0-E1).lt.1d-6) then
      j=30
    endif
    E1=E0
 
    B=1d0/(3.04d0*0.0367502d0)
    do i=1,3
      w(i)=(2d0/(exp(-B*(merg(i)-E0))+exp(B*(merg(i)-E0))))**2
    enddo
  enddo

{rs2c,shift=0.25;close,5;maxiter,100000,100000;wf,22,1,2,0}
rs2cenergy=energy

}

{optg,gradient=1.d-4,proc=rs2cproc,variable=rs2cenergy
 active,r1,r3,a2}

{rs2c,shift=0.25;close,5;maxiter,100000,100000;wf,22,1,0,0}
esing = energy


