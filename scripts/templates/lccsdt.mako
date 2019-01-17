<%def name="getspin()"><%elec_spin = int(mult)-1%>set,spin=${elec_spin}</%def>
memory,1000,m
gthresh,energy=1.0d-10,orbital=1.0d-10

nosym
angstrom
Geometry = {
${coords}
}  

set,charge=0
${getspin()}

basis = cc-pVDZ
{df-rhf,maxit=300}
% if mult == 1:
{df-lccsd(t),maxit=150}
% else:
{df-luccsd(t),maxit=150}
% endif
eDZ = energy

basis = cc-pVTZ
{df-rhf,maxit=300}
% if mult == 1:
{df-lccsd(t),maxit=150}
% else:
{df-luccsd(t),maxit=150}
% endif
eTZ = energy

basis = cc-pVQZ
{df-rhf,maxit=300}
% if mult == 1:
{df-lccsd(t),maxit=150}
% else:
{df-luccsd(t),maxit=150}
% endif
eQZ = energy

basis = cc-pV5Z
{df-rhf,maxit=300}
% if mult == 1:
{df-lccsd(t),maxit=150}
% else:
{df-luccsd(t),maxit=150}
% endif
e5Z = energy

show,eDZ
show,eTZ
show,eQZ
show,e5Z

