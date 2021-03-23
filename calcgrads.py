# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 17:44:10 2021

@author: Konstantinos Angelou
"""
import pandas as pd
import numpy as np


def getHeadersComments(fname, separ):
    '''
    Function to acquire the header names from Comsol files or files that
    contain the headers in single comment line.

    Parameters
    ----------
    fname : string
        The name of the input file.
    separ : string
        The separator between the columns.

    Returns
    -------
    header : list
        List that contains the columns names.

    '''
    # List with symbols used for comments
    comSym = ['%', '#', '//', '$']
    # The following part is necessary for Comsol files or 
    # files that contain the headers in comments
    # Open the file and read the first two lines
    # The first line is needed to extract the names of columns
    # The second line is needed to validate the number of columns
    with open(fname, encoding='utf-8') as myfile:
        header = myfile.readline().strip('\n')
        secondLine = myfile.readline().strip('\n')
    # Split the lines properly
    if separ in [' ', '\t']:
        header = ' '.join(header.split())
        secondLine = secondLine.split()        
    else:
        header = ' '.join(header.split(separ))
        secondLine = secondLine.split(separ)
        
    # Remove unnecessary symbols
    while (header[0] in comSym) or (header[0]==' '):
        header = header[1:]
    header = header.split()
    # Check if the two lines have the same number of columns
    tmphe = len(header)
    tmpse = len(secondLine)
    
    if tmphe!=tmpse:
        if tmpse>tmphe:
            for i in range(tmpse-tmphe):
                header.append('M{}'.format(i+1))
        else:
            print('Problem')
    return header


def getSim4LifeHeaders(fname, r2d):
    '''
    Function to acquire the header names from Sim4Life files.

    Parameters
    ----------
    fname : string
        The name of the input file.
    r2d : int
        Number of rows in which the headers exist.

    Returns
    -------
    List with the names of the headers.

    '''
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
    
    # The following part is necessary for Sim4Life files or similar
    # that contain the headers within comments in a range of rows
    # Read the first 20 lines to get the column labels    
    with open(fname, encoding='utf-8') as myfile:
        topfile = [next(myfile) for x in range(r2d)]
    
    # Remove { for top and } from bottom
    topfile = topfile[1:-1] 
    
    # Acquire the headers names (based on Sim4Life file format)
    heads = {}
    for line in range(len(topfile)):
        tmp = (topfile[line].strip('\n')).strip('#\t')
        topfile[line] = tmp
        fc = tmp.split(': ')[0]
        sc = tmp.split(': ')[1]
        '''# Get units
        if 'Field Quantity Units' in fc:
            unit = sc.strip('\"')'''
        if 'Column' in tmp:       
            if 'Quantity' in fc:
                # Find the number of columns
                ds = get_digits(fc)
                # Find the name of columns
                sc = sc.strip('"')
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
    return(headers)
    


def readData(fname, r2d=20, ih=True, mts=False, separ='\t'):
    '''
    Function to read the input file.

    Parameters
    ----------
    fname : string
        The name of the file that will be opened.
    r2d : int, optional
        The number of rows that need to be deleted. The default is 20.
    ih : boolean, optional
        Indicates if the file includes headers. The default is True.
    mts : boolean, optional
        Indicates if repeating separators exist. The default is False.
    separ : string, optional
        The separator between the columns. The default is '\t'.

    Returns
    -------
    data : pandas DataFrame
        Contains the input data (field).

    '''
  
    # If headers are included either in rows that we want to delete
    # or in a separate row
    if ih:
        # When no rows are to be deleted
        if r2d==0:
            headers = getHeadersComments(fname, separ)
            # If there are multiple separators
            if mts:
                separ = '\s+'
            data = pd.read_csv(fname, sep=separ, encoding='utf-8', dtype=np.float64, na_values=0.0, skiprows=1, names=headers, header=None)
            data = data.fillna(0.0)
        else:
            # Get SIM4Life headers
            headers = getSim4LifeHeaders(fname, r2d)
            # If repeating separators exist
            if mts:
                separ = '\s+'
            # Read the magnetic-field file    
            data = pd.read_csv(fname, sep=separ, encoding='utf-8', dtype=np.float64, na_values=0.0, skiprows=r2d, names=headers, usecols=range(len(headers)))
            data = data.fillna(0.0)
            
            # Im values are 0, so delete them
            for name in headers:
                if 'Im' in name:
                    data.drop(name, inplace=True, axis=1)       
    else: 
        # If headers are not included or we do not want to include them
        data = pd.read_csv(fname, sep=separ, encoding='utf-8', dtype=np.float64, na_values=0.0, skiprows=r2d, header=None)
        data = data.fillna(0.0)
        # Assign names to the columns
        # The first 3 are named after the space dimensions x-y-z
        data.rename(columns={0: 'x', 1: 'y', 2: 'z'}, inplace=True)
        # Every next column is named after the letter M and a number
        for i in range(3, len(data.columns)):
            data.rename(columns={i: 'M{}'.format(i-2)}, inplace=True)
    return data


def Grads(data):
    '''
    Calculate the gradients for any number of columns (values for each 
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
    
    def cgrad(sval, data):
        '''
        Function to calculate the gradients for every column of the input data
        (except for the coordinates) for a specific direction.

        Parameters
        ----------
        sval : tuple
            The first part of tuple indicates the order of sorting 
            and the second part the plane that gradients will be found.
        data : pandas.DataFrame
            input data.

        Returns
        -------
        tripleDF : pandas.DataFrame
            the gradients for every column of the input data
            (except for the coordinates) for a specific direction.

        '''
        # Initiate a DataFrame that will contain the gradients
        tripleDF = pd.DataFrame()
        # Calculate the gradient on the sval[1] dimension
        data.sort_values(by=sval[0], inplace=True)
        # Keep the index column, for sorting purposes
        dataI = list(data.index)
        for col in data.columns[3:]:
            tmp = np.gradient(data[col], data[sval[1]], edge_order=2)
            tmpDF = pd.DataFrame({'g{}{}'.format(sval[1],col): tmp}, index=dataI)
            tripleDF = pd.concat([tripleDF, tmpDF], axis=1, ignore_index=False)
        return tripleDF
        
    # Get the names of the columns
    names = list(data.columns)
    # If there are more than 4 columns (which means more than one direction),
    # then calculate the root mean square of the directions
    if len(names)>4:
        b = '|B|'
        names.append(b)
        
        data[b] = 0
        for head in names[3:-1]:
            data[b] += data[head]**2
        data[b] = np.sqrt(data[b])
    
    # Get the coordinates from the input data
    x = data.columns[0]
    y = data.columns[1]
    z = data.columns[2]
    grad = pd.concat([data[x], data[y], data[z]], axis=1, ignore_index=False)
    
    # List with tuples. The first part of tuple indicates the order of sorting
    # and the second part the plane that gradients will be found.
    sorval = [([z, y, x], x), ([z, x, y], y), ([y, x, z], z)]    
    
    # Calculate gradients for every direction
    for item in sorval:
        # Check whether the column contains just one number
        if not data[item[1]].eq(data[item[1]].iloc[0]).all():
            grad = pd.concat([grad, cgrad(item, data)], axis=1, ignore_index=False)

    return grad