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



def readFile(fname, initrows, separ):
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

def Grads(data):
    # Calculate gradients along the x axis
    data.sort_values(by=['z', 'y', 'x'], inplace=True)
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


def Export(grad, fname):
    # Export gradient
    gfname = fname.rstrip('.txt') + '-Gradient.txt'
    grad.to_csv(gfname, sep=' ', index=False)
