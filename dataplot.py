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
    fname = filename.split('.')[:-1]
    fig.savefig('{}.{}'.format(fname, cformat), format=cformat, dpi=300, bbox_inches='tight')


#dmsions = ['x', 'y', 'z']

'''
data['gb2'] = np.sqrt( (data['gbxx']+data['gbyx']+data['gbzx'])**2 + (data['gbxy']+data['gbyy']+data['gbzy'])**2 + (data['gbxz']+data['gbyz']+data['gbzz'])**2 )

data['gbx'] = np.sqrt( data['gbxx']**2 + data['gbyx']**2 + data['gbzx']**2 )
data['gby'] = np.sqrt( data['gbxy']**2 + data['gbyy']**2 + data['gbzy']**2 )
data['gbz'] = np.sqrt( data['gbxz']**2 + data['gbyz']**2 + data['gbzz']**2 )
data['gbzz2'] = np.sqrt(data['gbzz']**2)
data['gbxx2'] = np.sqrt(data['gbxx']**2)
data['gbyy2'] = np.sqrt(data['gbyy']**2)

grads = ['gbxx2', 'gbyy2']

grads = ['gb2', 'gbx', 'gby', 'gbz', 'gbzz2', 'gbxx2', 'gbyy2']
'''
'''
expl = {}
expl['gb2'] = r'$\vec{G}=\sqrt{\left( \frac{\partial B_x}{\partial x} + \frac{\partial B_y}{\partial x} + \frac{\partial B_z}{\partial x}\right)^2 +\left( \frac{\partial B_x}{\partial y} + \frac{\partial B_y}{\partial y} + \frac{\partial B_z}{\partial y}\right)^2 +\left( \frac{\partial B_x}{\partial z} + \frac{\partial B_y}{\partial z} + \frac{\partial B_z}{\partial z}\right)^2}$'
expl['gbx'] = r'$\sqrt{\left( \frac{\partial B_x}{\partial x} + \frac{\partial B_y}{\partial x} + \frac{\partial B_z}{\partial x}\right)^2}$'
expl['gby'] = r'$\sqrt{\left( \frac{\partial B_x}{\partial y} + \frac{\partial B_y}{\partial y} + \frac{\partial B_z}{\partial y}\right)^2}$'
expl['gbz'] = r'$\sqrt{\left( \frac{\partial B_x}{\partial z} + \frac{\partial B_y}{\partial z} + \frac{\partial B_z}{\partial z}\right)^2}$'
expl['gbxx2'] = r'$\sqrt{\left( \frac{\partial B_x}{\partial x}\right)^2}$'
expl['gbyy2'] = r'$\sqrt{\left( \frac{\partial B_y}{\partial y}\right)^2}$'
expl['gbzz2'] = r'$\sqrt{\left( \frac{\partial B_z}{\partial z}\right)^2}$'
'''
        
# Create a 2D image -> select x-, y- axis and the third axis that will 
# provide the proper color (B, gradient, Eddy)
# x='x'
# y='z'
# gB='Vec'       

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
    



