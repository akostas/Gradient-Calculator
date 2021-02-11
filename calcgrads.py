# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 17:44:10 2021

@author: Konstantinos Angelou
"""
import pandas as pd
import numpy as np

def get_digits(str1):
    '''
    Function to acquire digits for each column 
    For Sim4Life files

    Parameters
    ----------
    str1 : string
        Rows that contain the column numbers (among others).

    Returns
    -------
    c : list
        Numbers of columns.

    '''
    c = []
    for i in str1:
        if i.isdigit():
            c.append(i)
    return c



def readData(fname, initrows=20, separ='\t'):
    '''
    Function to read the file when it is Sim4Life file.

    Parameters
    ----------
    fname : string
        input filename.
    initrows : int, optional
        Initial rows that need to be deleted. The default is 20.
    separ : string, optional
        Separator between columns. The default is '\t'.

    Returns
    -------
    data : pandas.DataFrame
        Input data.

    '''
    # Read the first 20 lines to get the column labels    
    with open(fname, encoding='utf-8') as myfile:
        topfile = [next(myfile) for x in range(initrows)]
    
    # Remove { for top and } from bottom
    topfile = topfile[1:-1] 
    
    # Acquire the headers names (based on Sim4Life file format)
    heads = {}
    for line in range(len(topfile)):
        tmp = (topfile[line].strip('\n')).strip('#\t')
        topfile[line] = tmp
        fc = tmp.split(': ')[0]
        sc = tmp.split(': ')[1]
        if 'Field Quantity Units' in fc:
            unit = sc.strip('\"')
        if 'Column' in tmp:       
            if 'Quantity' in fc:
                # Find the number of columns
                ds = get_digits(fc)
                # Find the name of columns
                sc = sc.strip('"')
                print(sc)
                if len(ds)>1:
                    meg = sc.split(' ')
                    meg1 = meg[0].split('/')[0]                  
                    meg2 = meg[0].split('/')[1]
                    megs = ['{}-{}'.format(meg1,meg[1]), '{}-{}'.format(meg2,meg[1])]
                else:
                    megs = [sc]
                for i,j in zip(ds, megs):
                    heads[i] = j
    
    headers = list(heads.values())
    
    # Read the magnetic-field file    
    data = pd.read_csv(fname, sep=separ, encoding='utf-8', dtype=np.float64, na_values=0.0, skiprows=initrows, names=headers, usecols=range(len(headers)))
    data = data.fillna(0.0)
    
    # Im values are 0, so delete them
    for name in headers:
        if 'Im' in name:
            data.drop(name, inplace=True, axis=1)
    
    return data


def grad_B_(data):
    '''
    Calculate the gradients when there are 4 columns (only the absolute value
    of the vector is provided).

    Parameters
    ----------
    data : pandas.DataFrame
        Contains the magnetic field (input data).

    Returns
    -------
    grad : pandas.DataFrame
        Contains the gradients of the magnetic field.

    '''
    # Calculate the gradient on the 1st dimension
    data.sort_values(by=[data.columns[2], data.columns[1], data.columns[0]], inplace=True)
    gbx = np.gradient(data[data.columns[3]], data[data.columns[0]], edge_order=2)
    dataI = list(data.index)
    # Sort based on the index of the rows
    gbxI = sorted(list(zip(dataI, gbx)), key=lambda l:l[0], reverse=False)
    
    # Calculate the gradient on the 2nd dimension
    data.sort_values(by=[data.columns[2], data.columns[0], data.columns[1]], inplace=True)
    gby = np.gradient(data[data.columns[3]], data[data.columns[1]], edge_order=2)
    dataI = list(data.index)
    # Sort based on the index of the rows
    gbyI = sorted(list(zip(dataI, gby)), key=lambda l:l[0], reverse=False)
    
    # Calculate the gradient on the 3rd dimension
    data.sort_values(by=[data.columns[1], data.columns[0], data.columns[2]], inplace=True)
    gbz = np.gradient(data[data.columns[3]], data[data.columns[2]], edge_order=2)
    dataI = list(data.index)
    # Sort based on the index of the rows
    gbzI = sorted(list(zip(dataI, gbz)), key=lambda l:l[0], reverse=False)  

    # Create the gradients database headers
    gheaders = [data.columns[0], data.columns[1], data.columns[2], 
                'g{}{}'.format(data.columns[3], data.columns[0]), 
                'g{}{}'.format(data.columns[3], data.columns[1]), 
                'g{}{}'.format(data.columns[3], data.columns[2]) ]
    
    # Create the gradients database
    grad = pd.DataFrame(columns=gheaders)
    
    data.sort_index(inplace=True)
    
    # Get the values of the 3 dimensions from the input data
    grad[data.columns[0]] = data[data.columns[0]].copy()
    grad[data.columns[1]] = data[data.columns[1]].copy()
    grad[data.columns[2]] = data[data.columns[2]].copy()
    
    # Fill the gradients DataFrame
    ml = [gbxI, gbyI, gbzI]
    for num, i in enumerate(list(grad.columns)[3:]):
        grad[i] = [row[1] for row in ml[num]]
    
    # Calculate the absolute value of the gradient
    grad['g{}'.format(data.columns[3])] = np.sqrt(grad[gheaders[3]]**2 + grad[gheaders[4]]**2 + grad[gheaders[5]]**2)
    return grad

def grad_dir(data):
    '''
    Calculate the gradients when there are 6 columns (values for each 
    direction).

    Parameters
    ----------
    data : pandas.DataFrame
        Contains the magnetic field (input data).

    Returns
    -------
    grad : pandas.DataFrame
        Contains the gradients of the magnetic field.

    '''
    # Assign the headers names to variables for better handling
    x = data.columns[0]
    y = data.columns[1]
    z = data.columns[2]
    bx = data.columns[3]
    by = data.columns[4]
    bz = data.columns[5]
    b = '|B|'
    
    # Calculate |B|
    data[b] = np.sqrt(data[bx]**2 + data[by]**2 + data[bz]**2)   
    
    # Calculate the gradient on the 1st dimension
    data.sort_values(by=[z, y, x], inplace=True)
    gbxx = np.gradient(data[bx], data[x], edge_order=2)
    gbyx = np.gradient(data[by], data[x], edge_order=2)
    gbzx = np.gradient(data[bz], data[x], edge_order=2)
    gbx = np.gradient(data[b], data[x], edge_order=2)
    dataI = list(data.index)
    # Sort based on the index of the rows
    gbxxI = sorted(list(zip(dataI, gbxx)), key=lambda l:l[0], reverse=False)
    gbyxI = sorted(list(zip(dataI, gbyx)), key=lambda l:l[0], reverse=False)
    gbzxI = sorted(list(zip(dataI, gbzx)), key=lambda l:l[0], reverse=False)
    
    gbxI = sorted(list(zip(dataI, gbx)), key=lambda l:l[0], reverse=False)
    
    # Calculate the gradient on the 2nd dimension
    data.sort_values(by=[z, x, y], inplace=True)
    gbxy = np.gradient(data[bx], data[y], edge_order=2)
    gbyy = np.gradient(data[by], data[y], edge_order=2)
    gbzy = np.gradient(data[bz], data[y], edge_order=2)
    gby = np.gradient(data[b], data[y], edge_order=2)
    dataI = list(data.index)
    # Sort based on the index of the rows
    gbxyI = sorted(list(zip(dataI, gbxy)), key=lambda l:l[0], reverse=False)
    gbyyI = sorted(list(zip(dataI, gbyy)), key=lambda l:l[0], reverse=False)
    gbzyI = sorted(list(zip(dataI, gbzy)), key=lambda l:l[0], reverse=False)
    
    gbyI = sorted(list(zip(dataI, gby)), key=lambda l:l[0], reverse=False)
    
    # Calculate the gradient on the 3rd dimension
    data.sort_values(by=[y, x, z], inplace=True)
    gbxz = np.gradient(data[bx], data[z], edge_order=2)
    gbyz = np.gradient(data[by], data[z], edge_order=2)
    gbzz = np.gradient(data[bz], data[z], edge_order=2)
    gbz = np.gradient(data[b], data[z], edge_order=2)
    dataI = list(data.index)
    # Sort based on the index of the rows
    gbxzI = sorted(list(zip(dataI, gbxz)), key=lambda l:l[0], reverse=False)
    gbyzI = sorted(list(zip(dataI, gbyz)), key=lambda l:l[0], reverse=False)
    gbzzI = sorted(list(zip(dataI, gbzz)), key=lambda l:l[0], reverse=False)
    
    gbzI = sorted(list(zip(dataI, gbz)), key=lambda l:l[0], reverse=False)

    # Create the gradients database headers
    gheaders = [x, y, z]
    for i in list(data.columns)[3:]:
        for j in [x, y, z]:
            gheaders.append('g{}{}'.format(i.replace('Re-', ''), j))

    # Create the gradients database
    grad = pd.DataFrame(columns=gheaders)

    data.sort_index(inplace=True)
    
    # Get the values of the 3 dimensions from the input data
    grad[x] = data[x].copy()
    grad[y] = data[y].copy()
    grad[z] = data[z].copy()

    # Fill the gradients DataFrame
    ml = [gbxxI, gbxyI, gbxzI, gbyxI, gbyyI, gbyzI, gbzxI, gbzyI, gbzzI, gbxI, gbyI, gbzI]
    for num, i in enumerate(list(grad.columns)[3:]):
        grad[i] = [row[1] for row in ml[num]]

    return grad

def Grads(data):
    '''
    Choose the proper function to calculate the gradients.

    Parameters
    ----------
    data : pandas.DataFrame
        Contains the input data.

    Returns
    -------
    pandas.DataFrame
        Contains the gradients data.

    '''
    if len(data.columns)==4:
        grad = grad_B_(data)
    elif len(data.columns)==6:
        grad = grad_dir(data)
    else:
        return -1
    return grad