#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 11:33:31 2019

@author: gabriele
"""
from matplotlib import animation
import numpy as np
import sys

import plot
import cell
import params

def animate(frame_BaTiO3,plotBa,plotTi,plotO):
    plotBa.collections = []
    plotTi.collections = []
    plotO.collections = []
    frame_Ba, frame_Ti, frame_O = frame_BaTiO3[0:3],frame_BaTiO3[3:6],frame_BaTiO3[6::]
    plotBa._offsets3d = ([frame_Ba[0]],[frame_Ba[1]],[frame_Ba[2]])
    plotTi._offsets3d = ([frame_Ti[0]],[frame_Ti[1]],[frame_Ti[2]])
    plotO._offsets3d = (frame_O[0:3],frame_O[3:6],frame_O[6::])
    return

a = params.get_parameters()[0]
eigvec = np.loadtxt('eigvectors')
eigfreq = np.loadtxt('frequencies')
EIGVEC_real = []
EIGVEC_imag = []
for i in range(0,len(eigvec),15):
    EIGVEC_real.append(eigvec[i:i+15,0:15])
    EIGVEC_imag.append(eigvec[i:i+15,15::])


k = sys.argv[1]
j = sys.argv[2]

freq = eigfreq[j,k]
eigvec_toplot = EIGVEC_real[k][j]




t = np.arange(0,2*np.pi,0.1*np.pi)
time_function = 1*np.sin(t)
BaTiO3_0 = cell.BaTiO3(a)
BaTiO3_0.supercell(1,1,1)
Ba_0, Ti_0, O1_0, O2_0, O3_0 = BaTiO3_0.Ba, BaTiO3_0.Ti, BaTiO3_0.O1, BaTiO3_0.O2, BaTiO3_0.O3
O_0 = np.hstack((O1_0,O2_0,O3_0))

Ba = np.repeat(Ba_0,len(time_function),axis=0) + (eigvec_toplot[0:3].reshape(3,1)*time_function).T
Ti = np.repeat(Ti_0,len(time_function),axis=0) + (eigvec_toplot[3:6].reshape(3,1)*time_function).T
O = np.repeat(O_0,len(time_function),axis=0) + (eigvec_toplot[6::].reshape(9,1)*time_function).T
BaTiO3 = np.hstack((Ba,Ti,O))

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
plotBa = ax.scatter(Ba[0,0],Ba[0,1],Ba[0,2],s=137*50)
plotTi = ax.scatter(Ti[0,0],Ti[0,1],Ti[0,2],s=47*50)
plotO = ax.scatter(O[0,0:3],O[0,3:6],O[0,6::],s=15*50)

ani = animation.FuncAnimation(fig,animate,frames=BaTiO3,fargs=(plotBa,plotTi,plotO))




