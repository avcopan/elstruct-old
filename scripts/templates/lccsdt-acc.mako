<%def name="getspin()"><%elec_spin = int(mult)-1%>set,spin=${elec_spin}</%def>
memory,2000,m
gthresh,energy=1.0d-10,orbital=1.0d-10

nosym
noorient
angstrom
Geometry = {
${coords}
}  

set,charge=0
${getspin()}

basis = aug-cc-pVDZ
{df-rhf,maxit=300}
{locali,loc_method=pipek,
 pipek,method=1,delete=1}
% if mult == 1:
{df-lccsd(t),thrbp=0.92,maxit=150}
% else:
{df-luccsd(t),thrbp=0.92,maxit=150}
% endif
eDZ = energy

basis = aug-cc-pVTZ
{df-rhf,maxit=300}
{locali,loc_method=pipek,
 pipek,method=1,delete=2}
% if mult == 1:
{df-lccsd(t),thrbp=0.92,maxit=150}
% else:
{df-luccsd(t),thrbp=0.92,maxit=150}
% endif
eTZ = energy

basis = aug-cc-pVQZ
{df-rhf,maxit=300}
{locali,loc_method=pipek,
 pipek,method=1,delete=2}
% if mult == 1:
{df-lccsd(t),thrbp=0.92,maxit=150}
% else:
{df-luccsd(t),thrbp=0.92,maxit=150}
% endif
eQZ = energy

basis = aug-cc-pV5Z
{df-rhf,maxit=300}
{locali,loc_method=pipek,
 pipek,method=1,delete=2}
% if mult == 1:
{df-lccsd(t),thrbp=0.92,maxit=150}
% else:
{df-luccsd(t),thrbp=0.92,maxit=150}
% endif
e5Z = energy

show,eDZ
show,eTZ
show,eQZ
show,e5Z

