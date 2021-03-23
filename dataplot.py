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
    '''
    Function to create a grid required for the plotting

    Parameters
    ----------
    data : pandas.DataFrame
        the data that we need to plot.
    x : string
        name of the x axis.
    y : string
        name of the y axis.
    gB : string
        name of the Z axis.
    scale : string, optional
        linear or logarithmic. The default is 'linear'.

    Returns
    -------
    np.array
        Returns 3 np.arrays. One for x, one for y and one for Z axis.

    '''
    def r2(f, p=0.001):
        '''
        Function to reduce decimal points, without rounding.

        Parameters
        ----------
        f : float
            the number to reduce.
        p : fload, optional
            Indicates the decimal point that we need. The default is 0.001.

        Returns
        -------
        float
            The new number with the desired decimal points.

        '''
        if f>0:
            return f - f%p
        elif f<0:
            return f + abs(f)%p
        else:
            return 0.0
        
    # Check the length of the series and reduce it by reducing the decimal 
    # number of the coordinates
    if len(set(data[x]))>500 or len(set(data[y]))>500:
        for i in range(3):
            data[data.columns[i]] = data[data.columns[i]].apply(r2)
    # Remove the duplicates that occur from the decimal reduction
    data.drop_duplicates(subset=[data.columns[i] for i in range(3)], keep='first', inplace=True)         
    # Z values container
    newZ = []
    # Iterate over y axis
    for j in sorted(list(set(data[y]))):
        arrayz = []
        # Iterate over x axis
        for i in sorted(list(set(data[x]))):
            # Get the value if it exists, else set the value zero
            try:
                value = list(data[ (data[x]==i) & (data[y]==j)][gB])[0]
            except:
                value = 0.0
            # Get the value in the desired scale (linear or logarithmic)
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


def createPlot(fig, ax, uaxis, gB, cslice, data, scale='linear'):
    '''
    Function to plot the data.

    Parameters
    ----------
    fig : figure
        DESCRIPTION.
    ax : axis
        DESCRIPTION.
    uaxis : string
        the names of the x and y axis.
    gB : string
        name of z axis.
    cslice : integer
        the slice of z axis that we want to plot.
    data : pandas.DataFrame
        the data that we want to plot.
    scale : string, optional
        linear or logarithmic. The default is 'linear'.

    Returns
    -------
    None.

    '''

    # Identify the 3rd dimension, whose slice we get
    tmpDimList = [str(data.columns[0]), str(data.columns[1]), str(data.columns[2])]
    x = uaxis.split('-')[0]
    y = uaxis.split('-')[1]
    tmpDimList.remove(x)
    tmpDimList.remove(y)

    data.sort_values(by=[tmpDimList[0], y, x], inplace=True)

    # Select the incision plane and take the unique values
    stableZ = tmpDimList[0]
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
    ax.set_xlabel('{}'.format(x), fontsize=26)
    ax.set_ylabel('{}'.format(y), fontsize=26)
    if scale=='linear':
        fig.colorbar(psm, ax=ax).set_label(label='{}'.format(gB), size=20)
    else:
        fig.colorbar(psm, ax=ax).set_label(label='{}'.format(gB), size=20)
    fig.tight_layout()
    



