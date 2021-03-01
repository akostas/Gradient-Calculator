# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 10:39:41 2021

@author: Konstantinos Angelou
"""

import pandas as pd
import numpy as np
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.pyplot as plt

def createGrid(data, x, y, gB, scale='linear'):
    newZ = []
    for j in sorted(list(set(data[y]))):
        arrayz = []
        for i in sorted(list(set(data[x]))):
            value = list(data[ (data[x]==i) & (data[y]==j)][gB])[0]           
            if scale=='linear':
                arrayz.append(value)
            else:
                maxval = max(np.sqrt(data[gB]**2))
                tmp = 20*np.log10(np.abs(value)/maxval)
                arrayz.append(tmp)
        newZ.append(arrayz)
    mx, my = np.meshgrid(sorted(list(set(data[x]))), sorted(list(set(data[y]))))
    X, Y, Z =  mx, my, np.array(newZ)
    return X, Y, Z

def saveFig(fig, filename):
    cformat = filename.split('.')[-1]
    fname = ".".join(filename.split('.')[:-1])
    fig.savefig('{}.{}'.format(fname, cformat), format=cformat, dpi=300, bbox_inches='tight')


def createPlot(fig, ax, uaxis, gB, cslice, data, scale='linear'):
 
    tmp = ['x', 'y', 'z']
    x = uaxis.split('-')[0]
    y = uaxis.split('-')[1]
    
    tmp.remove(x)
    tmp.remove(y)
    # Select the incision plane and take the unique values
    stableZ = tmp[0]
    tmplist = sorted(list(set(data[stableZ])))
    # Select a specific slice of the incision plane (here is the middle one)
    data2 = data[data[stableZ]==tmplist[cslice]]
    
    # Create the meshgrid
    X, Y, Z =  createGrid(data2, x, y, gB, scale)
    
    mins, maxs = [], []
    for j in Z:
        mins.append(min(j))
        maxs.append(max(j))
      
    # Set upper and lower limits for coloring
    llimitdb = min(mins)
    ulimitdb = max(maxs)
    
    # Create a colormap
    mycmap = plt.cm.CMRmap
    cmaplist = [mycmap(i) for i in range(mycmap.N)]
    newcmap = cm.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, mycmap.N)
    # Define the different colors (max=256)
    bounds = np.linspace(llimitdb, ulimitdb, 79)
    norm = cm.colors.BoundaryNorm(bounds, mycmap.N)
    
    # Plot
    psm = ax.pcolormesh(X,Y,Z,  cmap=newcmap, norm=norm, shading='auto')
    ax.set_facecolor('xkcd:black')
    ax.set_xlabel('{}(m)'.format(x), fontsize=26)
    ax.set_ylabel('{}(m)'.format(y), fontsize=26)
    if scale=='linear':
        fig.colorbar(psm, ax=ax).set_label(label='{}(T/m)'.format(gB), size=20)
    else:
        fig.colorbar(psm, ax=ax).set_label(label='{}(db)'.format(gB), size=20)
    fig.tight_layout()
    



