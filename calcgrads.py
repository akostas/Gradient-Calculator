# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 17:44:10 2021

@author: Konstantinos
"""
import pandas as pd
import numpy as np

def get_digits(str1):
    c = []
    for i in str1:
        if i.isdigit():
            c.append(i)
    return c



def readData(fname, initrows=20, separ='\t'):
    # Read the first 20 lines to get the column labels
    #fname = 'ExportedFieldData-B-Quasi-Static-1kHz.txt'
    
    with open(fname, encoding='utf-8') as myfile:
        topfile = [next(myfile) for x in range(initrows)]
    
    topfile = topfile[1:-1] # Remove { for top and } from bottom
    
    heads = {}
    for line in range(len(topfile)):
        tmp = (topfile[line].strip('\n')).strip('#\t')
        topfile[line] = tmp
        fc = tmp.split(': ')[0]
        sc = tmp.split(': ')[1]
        #unit = ''
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

#dbak = data.copy() # Keep a copy of the database
#data = dbak.copy()

def grad_B_(data):
        
    data.sort_values(by=[data.columns[2], data.columns[1], data.columns[0]], inplace=True)
    gbx = np.gradient(data[data.columns[3]], data[data.columns[0]], edge_order=2)
    dataI = list(data.index)
    
    gbxI = sorted(list(zip(dataI, gbx)), key=lambda l:l[0], reverse=False)
    
    
    # Calculate gradients along the y axis
    data.sort_values(by=[data.columns[2], data.columns[0], data.columns[1]], inplace=True)
    gby = np.gradient(data[data.columns[3]], data[data.columns[1]], edge_order=2)
    dataI = list(data.index)
    
    gbyI = sorted(list(zip(dataI, gby)), key=lambda l:l[0], reverse=False)
    
    # Calculate gradients along the z axis
    data.sort_values(by=[data.columns[1], data.columns[0], data.columns[2]], inplace=True)
    gbz = np.gradient(data[data.columns[3]], data[data.columns[2]], edge_order=2)
    dataI = list(data.index)
    
    gbzI = sorted(list(zip(dataI, gbz)), key=lambda l:l[0], reverse=False)  


    # Create the gradients database headers
    gheaders = [data.columns[0], data.columns[1], data.columns[2], \
                'g{}{}'.format(data.columns[3], data.columns[0]), \
                'g{}{}'.format(data.columns[3], data.columns[1]), \
                'g{}{}'.format(data.columns[3], data.columns[2]) ]
    
    # Create the gradients database
    grad = pd.DataFrame(columns=gheaders)
    
    data.sort_index(inplace=True)
    
    grad[data.columns[0]] = data[data.columns[0]].copy()
    grad[data.columns[1]] = data[data.columns[1]].copy()
    grad[data.columns[2]] = data[data.columns[2]].copy()
    
    ml = [gbxI, gbyI, gbzI]
    for num, i in enumerate(list(grad.columns)[3:]):
        grad[i] = [row[1] for row in ml[num]]
    
    
    grad['g{}'.format(data.columns[3])] = np.sqrt(grad[gheaders[3]]**2 + grad[gheaders[4]]**2 + grad[gheaders[5]]**2)
    return grad



def grad_dir_old(data):
    # Calculate gradients along the x axis
    data.sort_values(by=['z', 'y', 'x'], inplace=True)
    data.sort_values(by=[data.columns[2], data.columns[1], data.columns[0]], inplace=True)
    gbxx = np.gradient(data['Re-Bx'], data['x'], edge_order=2)
    gbyx = np.gradient(data['Re-By'], data['x'], edge_order=2)
    gbzx = np.gradient(data['Re-Bz'], data['x'], edge_order=2)
    dataI = list(data.index)
    
    gbxxI = sorted(list(zip(dataI, gbxx)), key=lambda l:l[0], reverse=False)
    gbyxI = sorted(list(zip(dataI, gbyx)), key=lambda l:l[0], reverse=False)
    gbzxI = sorted(list(zip(dataI, gbzx)), key=lambda l:l[0], reverse=False)
    
    # Calculate gradients along the y axis
    data.sort_values(by=['z', 'x', 'y'], inplace=True)
    gbxy = np.gradient(data['Re-Bx'], data['y'], edge_order=2)
    gbyy = np.gradient(data['Re-By'], data['y'], edge_order=2)
    gbzy = np.gradient(data['Re-Bz'], data['y'], edge_order=2)
    dataI = list(data.index)
    
    gbxyI = sorted(list(zip(dataI, gbxy)), key=lambda l:l[0], reverse=False)
    gbyyI = sorted(list(zip(dataI, gbyy)), key=lambda l:l[0], reverse=False)
    gbzyI = sorted(list(zip(dataI, gbzy)), key=lambda l:l[0], reverse=False)
    
    # Calculate gradients along the z axis
    data.sort_values(by=['y', 'x', 'z'], inplace=True)
    gbxz = np.gradient(data['Re-Bx'], data['z'], edge_order=2)
    gbyz = np.gradient(data['Re-By'], data['z'], edge_order=2)
    gbzz = np.gradient(data['Re-Bz'], data['z'], edge_order=2)
    dataI = list(data.index)
    
    gbxzI = sorted(list(zip(dataI, gbxz)), key=lambda l:l[0], reverse=False)
    gbyzI = sorted(list(zip(dataI, gbyz)), key=lambda l:l[0], reverse=False)
    gbzzI = sorted(list(zip(dataI, gbzz)), key=lambda l:l[0], reverse=False)

    # Create the gradients database headers
    gheaders = ['x', 'y', 'z']
    for i in list(data.columns)[3:]:
        for j in ['x', 'y', 'z']:
            gheaders.append('{}-g{}{}'.format(i.split('-')[0], i.split('-')[1], j))

    # Create the gradients database
    grad = pd.DataFrame(columns=gheaders)

    data.sort_index(inplace=True)
    
    grad['x'] = data['x'].copy()
    grad['y'] = data['y'].copy()
    grad['z'] = data['z'].copy()

    ml = [gbxxI, gbxyI, gbxzI, gbyxI, gbyyI, gbyzI, gbzxI, gbzyI, gbzzI]
    for num, i in enumerate(list(grad.columns)[3:]):
        grad[i] = [row[1] for row in ml[num]]


    #grad.sort_values(by=['x', 'y', 'z']).head(10).to_csv('grads-10-test.txt', sep=' ', index=False)
    return grad

def grad_dir(data):
    x = data.columns[0]
    y = data.columns[1]
    z = data.columns[2]
    bx = data.columns[3]
    by = data.columns[4]
    bz = data.columns[5]
    b = '|B|'
    
    # Calculate |B|
    data[b] = np.sqrt(data[bx]**2 + data[by]**2 + data[bz]**2)   
    
    # Calculate gradients along the x axis
    data.sort_values(by=[z, y, x], inplace=True)
    gbxx = np.gradient(data[bx], data[x], edge_order=2)
    gbyx = np.gradient(data[by], data[x], edge_order=2)
    gbzx = np.gradient(data[bz], data[x], edge_order=2)
    gbx = np.gradient(data[b], data[x], edge_order=2)
    dataI = list(data.index)
    
    gbxxI = sorted(list(zip(dataI, gbxx)), key=lambda l:l[0], reverse=False)
    gbyxI = sorted(list(zip(dataI, gbyx)), key=lambda l:l[0], reverse=False)
    gbzxI = sorted(list(zip(dataI, gbzx)), key=lambda l:l[0], reverse=False)
    
    gbxI = sorted(list(zip(dataI, gbx)), key=lambda l:l[0], reverse=False)
    
    # Calculate gradients along the y axis
    data.sort_values(by=[z, x, y], inplace=True)
    gbxy = np.gradient(data[bx], data[y], edge_order=2)
    gbyy = np.gradient(data[by], data[y], edge_order=2)
    gbzy = np.gradient(data[bz], data[y], edge_order=2)
    gby = np.gradient(data[b], data[y], edge_order=2)
    dataI = list(data.index)
    
    gbxyI = sorted(list(zip(dataI, gbxy)), key=lambda l:l[0], reverse=False)
    gbyyI = sorted(list(zip(dataI, gbyy)), key=lambda l:l[0], reverse=False)
    gbzyI = sorted(list(zip(dataI, gbzy)), key=lambda l:l[0], reverse=False)
    
    gbyI = sorted(list(zip(dataI, gby)), key=lambda l:l[0], reverse=False)
    
    # Calculate gradients along the z axis
    data.sort_values(by=[y, x, z], inplace=True)
    gbxz = np.gradient(data[bx], data[z], edge_order=2)
    gbyz = np.gradient(data[by], data[z], edge_order=2)
    gbzz = np.gradient(data[bz], data[z], edge_order=2)
    gbz = np.gradient(data[b], data[z], edge_order=2)
    dataI = list(data.index)
    
    gbxzI = sorted(list(zip(dataI, gbxz)), key=lambda l:l[0], reverse=False)
    gbyzI = sorted(list(zip(dataI, gbyz)), key=lambda l:l[0], reverse=False)
    gbzzI = sorted(list(zip(dataI, gbzz)), key=lambda l:l[0], reverse=False)
    
    gbzI = sorted(list(zip(dataI, gbz)), key=lambda l:l[0], reverse=False)

    # Create the gradients database headers
    gheaders = [x, y, z]
    for i in list(data.columns)[3:]:
        for j in [x, y, z]:
            #gheaders.append('{}-g{}{}'.format(i.split('-')[0], i.split('-')[1], j))
            gheaders.append('g{}{}'.format(i.replace('Re-', ''), j))

    # Create the gradients database
    grad = pd.DataFrame(columns=gheaders)

    data.sort_index(inplace=True)
    
    grad[x] = data[x].copy()
    grad[y] = data[y].copy()
    grad[z] = data[z].copy()

    ml = [gbxxI, gbxyI, gbxzI, gbyxI, gbyyI, gbyzI, gbzxI, gbzyI, gbzzI, gbxI, gbyI, gbzI]
    for num, i in enumerate(list(grad.columns)[3:]):
        grad[i] = [row[1] for row in ml[num]]


    #grad.sort_values(by=['x', 'y', 'z']).head(10).to_csv('grads-10-test.txt', sep=' ', index=False)
    return grad

def Grads(data):
    if len(data.columns)==4:
        grad = grad_B_(data)
    elif len(data.columns)==6:
        grad = grad_dir(data)
    else:
        return -1
    return grad
        

def Export(grad, fname):
    # Export gradient
    gfname = fname.rstrip('.txt') + '-Gradient.txt'
    grad.to_csv(gfname, sep=' ', index=False)
