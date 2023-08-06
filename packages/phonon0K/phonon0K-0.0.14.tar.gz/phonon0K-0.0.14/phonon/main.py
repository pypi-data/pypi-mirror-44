#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 18:21:44 2018

@author: Gabriele Coiana
"""
import numpy as np
import sys

from phonon import params
from phonon import dynam
from phonon import plot
from phonon import bz
from phonon import cell

# =============================================================================
# Parameters
a = params.get_parameters()[0]
mba, mti, mo = params.get_parameters()[1:4]
N1,N2,N3 = params.get_parameters()[4:7]
kinput = params.get_parameters()[7::][0]
interp = params.get_parameters()[8]
savefreq = params.get_parameters()[9]

N1N2N3 = N1*N2*N3 # Number of cells
N = N1*N2*N3*5    # Number of atoms
# =============================================================================
print('\nPho-NON-py')
print()
print('\nCalculating the k points...')
ks, ks_scaled, kk = bz.getk(N1,N2,N3,kinput)
print('Ok babe, Im gonna take all of these kpoints (scaled):\n',ks_scaled)


print('\nComputing the stiffness matrix...')
K = dynam.K(N1N2N3)
print('\tK is equilibrated to within ',np.max(np.abs(np.sum(K,axis=1))))

print('\nCalculating dynamical matrixes...')
FREQ = []
EIGVEC = []
mode = str(sys.argv[1])
for kpoint in ks:
    D = dynam.D(kpoint,K,N1,N2,N3,mba,mti,mo,mode)
    
    ll = np.matrix(D)
    print('\t',str(kpoint),' Hermitian: ',np.allclose(ll,ll.getH(),rtol=0.01,atol=0.01))
    
    eigvals, eigvec = np.linalg.eig(D)
    idx = eigvals.argsort()[::-1]   
    eigvals = eigvals[idx]  
    eigvec = eigvec[:,idx]
    freq = (np.sqrt(eigvals)/(2*np.pi))
    FREQ.append(freq)
    EIGVEC.append(eigvec)
print()


FREQ = np.array(FREQ).T

if(savefreq):
    np.savetxt('frequencies',np.column_stack([FREQ.real,FREQ.imag]))
    np.savetxt('frequencies_niceview',FREQ, fmt='%-1.2d')
    for i in range(len(EIGVEC)):
        with open('eigvectors','ab') as f: 
            np.savetxt(f,np.column_stack([EIGVEC[i].real, EIGVEC[i].imag]))



plot.plot(ks_scaled,kk, FREQ,interp)
























