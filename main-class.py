# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 16:33:44 2021

@author: Konstantinos Angelou
"""

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import calcgrads as cg
import tkinter.scrolledtext as st 
import pandastable as pdt
import datetime as dtm
import dataplot as dpl

## import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

class Window(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent) 
        self.parent = parent
        
        # Labels text
        self.infile = tk.StringVar() # Filename of the input file
        self.infile.set('Here is the input file path')
        self.outfile = tk.StringVar() # Filename of the output file
        self.outfile.set('Here is the output file path')
        
        # Open parameters        
        self.sepIn = tk.IntVar() # Separator for input file
        self.sepIn.set(2)
        self.sepMulti = tk.BooleanVar() # If the separator is repeated multiple times
        self.sepMulti.set(False)
        self.ird = tk.IntVar() # Initial rows to delete
        self.ird.set(20)
        
        # Save parameters        
        self.sepOut = tk.IntVar() # Separator for output file      
        self.sepOut.set(0)
        
        # DataFrames
        self.inData = pd.DataFrame() # Container for input file
        self.gradData = pd.DataFrame() # Container for gradients
        
        self.sepsNames = {0: 'space', 1: 'comma', 2: 'tab', 3: 'semicolon'}
        self.seps = {0: ' ', 1: ',', 2: '\t', 3: ';'}
        
        logFrame = tk.LabelFrame(self.parent, text='Log')
        logFrame.grid(row=10, column=0, pady=10, padx=10, columnspan=3)
        
        self.log_area = st.ScrolledText(logFrame, width=70, height=7, font=("Times New Roman", 8), state='disabled' )
        self.log_area.grid(row=10, column=0, pady=10, padx=10, columnspan=3)
        
        # Define input file
        self.inSource = tk.IntVar()
        self.inSource.set(1)
        ## self.inSourceLabel = tk.StringVar()
        ## self.inSourceLabel.set('Sim4Life')
        
        # Other file
        self.conHeaders = tk.IntVar() # Contains headers
        self.conHeaders.set(1)
       
        # Which database to plot - 1 for gradients, 0 for magnetic field
        self.dataPlot = tk.IntVar()
        self.dataPlot.set(1)
        # Which dimension to plot - 0 for x-y, 1 for x-z, 2 for y-z
        self.dataDim = tk.IntVar()
        self.dataDim.set(0)
        self.dataDimDict = {0:'x-y', 1:'x-z', 2:'y-z'}
        # Plot variable
        self.yax = tk.StringVar()
        self.options = ['']
        
        self.fig = ''
        
        self.initUI()

    def aboutMenu(self):
        '''
        Pops up a message box to inform about the creator of the software
        
        Returns
        -------
        None.
        '''
        tk.messagebox.showinfo("About", "This software has been created by Konstantinos Angelou!\nemail: angelou.konstantinos@gmail.com")    


    def helpMenu(self):
        '''
        Creates a new window that informs the user on the steps that need to 
        be followed for the calculation of the magnetic field gradients.
        
        Returns
        -------
        None.
        '''
        window = tk.Toplevel(self.parent, width=75, height=27)
        window.title("Help")
        #window.geometry('700x500')
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        
        
        helptext = "This software is used to calculate the gradients of a 3D field. The steps to calculate the gradients are the following:\n\t1) Open file: Define the characteristics of the input file. First select the number of rows that need to be deleted. Default is 20, which is the appropriate for some Sim4Life files. If the file includes headers, then check 'Contains headers', else un-check it. You should also select the proper separator between the columns. Finally, press 'Open file' and select the proper file. The data must contain 3 coordinates columns (the first three columns) and the rest (any of them) are the components of the field. \n\t2) Check Data: A table shows the first 10 lines to check whether the data have been imported correctly. The data may also be plotted here. \n\t3) Calculate Gradients: Calculate the gradients in every direction using the gradient function from numpy library.\n\t4) Check Gradient Data: A table shows the first 10 lines to check whether the gradients have been calculated correctly. The gradients may also be plotted here.\n\t5) Save File: Define the characteristics of the output file (i.e. column separator) and press 'Save file'."
        
        
        label = st.ScrolledText(window, wrap=tk.WORD, width=72, height=25, font=("Times New Roman", 16) )
        label.configure(state='normal')
        label.grid(row=0, column=0, pady=10, padx=10, sticky='ensw')
        label.insert(tk.INSERT, helptext)    
        label.configure(state='disabled')
        label.update()

    def updateLOG(self, logtext):
        '''
        Function to update the log.

        Parameters
        ----------
        logtext : string
            The text that will be written in the log.
            
        Returns
        -------
        None.
        '''
        # Get current time
        cdtm = dtm.datetime.now()
        # Convert current time to readable (custom) format
        logdate = '{}/{}/{}-{}:{}:{}'.format(cdtm.day, cdtm.month, cdtm.year, cdtm.hour, cdtm.minute, cdtm.second)
        # Update log
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.INSERT, '{}: {}\n'.format(logdate, logtext))    
        self.log_area.update()
        self.log_area.yview(tk.END)
        self.log_area.configure(state='disabled')


    def readFile(self, filename):
        '''
        Function to open the file that contains the Magnetic field data.

        Parameters
        ----------
        filename : string
            The name of the file that will be opened.

        Returns
        -------
        data : pandas.DataFrame
            Contains the input data (field).
        '''
        data = cg.readData(filename, int(self.ird.get()), self.conHeaders.get(), self.sepMulti.get() ,self.seps[self.sepIn.get()])
        return data
    

    def openFile(self, window):
        '''
        Function to open the input data. They are assigned to inData variable.

        Returns
        -------
        None.

        '''
        window.destroy()
        # Define file types
        ftypes = [('Text files', '*.txt'), ('CSV files', '*.csv'), ('Dat files', '*.dat'), ('All files', '*')]
        # Open the file        
        tmp = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = ftypes)
        
        if tmp != '':
            self.infile.set(tmp)         
            self.updateLOG('Now opening file: {}'.format(tmp))
            try:
                self.inData = self.readFile(tmp)
            except:
                self.updateLOG('There was an error opening the file. Please check import parameters and try again.')
            else:
                self.updateLOG('File is now open.')
        else:
            self.updateLOG('No file has been provided')

    def openParams(self):
        '''
        Create a window to define the parameters of the imported file
        (e.g. separator, if it contains headers)

        Returns
        -------
        None.

        '''
        
        def okBut(window):
            '''
            OK Button

            Parameters
            ----------
            window : tk.Toplevel
                the window that it will be.

            Returns
            -------
            None.

            '''
            window.destroy()
            
        def cancelButton(window, e, r, h):
            '''
            Cancel button

            Parameters
            ----------
            window : tk.Toplevel
                the window that it will be.
            e : int
                Number of rows to delete.
            r : string
                initial separator.
            h : int
                If headers exist.

            Returns
            -------
            None.

            '''
            self.ird.set(e)
            self.sepIn.set(r)
            self.conHeaders.set(h)
            window.destroy()

        
        window = tk.Toplevel(self.parent)
        window.title("Open Parameters")
        window.geometry('200x225')
        
        # Initial values - for use in cancel button
        # Initial value of rows that need to be deleted (for Sim4Life file)
        initEntry = self.ird.get()
        # Initial separator
        initRadio = self.sepIn.get()
        # Initial headers
        initHeaders = self.conHeaders.get()
        
        
        # Create a new frame
        rowsFrame = tk.Frame(window)
        rowsFrame.grid(row=0, column=0)
        # Holders for the rows that need to be deleted
        labelRows = tk.Label(rowsFrame, text='Initial rows to delete')
        labelRows.grid(row=0, column=0)      
        txtBox = tk.Entry(rowsFrame, textvariable = self.ird, width=6)
        txtBox.grid(row=0, column=1) #entry textbox

        # Define if the input file contains headers
        ch1 = tk.Checkbutton(window, text='Contains headers', variable=self.conHeaders, onvalue=1, offvalue=0)
        ch1.grid(row=1, column=0)
    
        # Frame for the separators
        sepFrame = tk.Frame(window, bd=1, highlightthickness=1, highlightbackground='black')
        sepFrame.grid(row=2, column=0, sticky='nesw')
        
        # Holders for the separators
        label = tk.Label(sepFrame, text='Select separator:')
        label.grid(row=0, column=0)
        i=1
        for sep, val in self.sepsNames.items():
            tk.Radiobutton(sepFrame, text=val, variable=self.sepIn,  
                    value=sep).grid(row=i, column=0, sticky='w')
            i += 1

        # Repeating separator
        ch1 = tk.Checkbutton(sepFrame, text='Repeating separator', variable=self.sepMulti , onvalue=True, offvalue=False)
        ch1.grid(row=i, column=0)
        
        # Frame for OK and Cancel buttons
        butFrame = tk.Frame(window)
        butFrame.grid(row=4,column=0)
        
        # Cancel button
        quitButton = tk.Button(butFrame, text='Cancel', command=lambda : cancelButton(window, initEntry, initRadio, initHeaders))
        quitButton.grid(row=0, column=1)
        
        # Open file button
        openButton = tk.Button(butFrame, text="Open File", command=lambda:self.openFile(window), width=15)
        openButton.grid(row=0, column=0)
        
        # OK button
        # okButton = tk.Button(butFrame, text="OK", command=lambda: okBut(window))
        # okButton.grid(row=0, column=0)

    def saveFile(self, window):
        '''
        Function to save the gradients data into a file.

        Returns
        -------
        None.

        '''
        window.destroy()
        # Check if gradients have been calculated
        if not self.gradData.empty:
            self.updateLOG('Now saving file')
            # Define file types
            ftypes = [('Text files', '*.txt'), ('CSV files', '*.csv'), ('Dat files', '*.dat'), ('All files', '*')]
            tmp = filedialog.asksaveasfilename(defaultextension=('Text files', '*.txt'), initialdir = "/", title = "Select file",filetypes = ftypes)
            if tmp != '':
                self.outfile.set(tmp)
                # Write the data to the file
                try:
                    self.gradData.to_csv('{}.txt'.format(tmp.rstrip('.txt')), sep=self.seps[self.sepOut.get()], index=False)
                except:
                    self.updateLog('There was an error trying to export gradients. Please try again.')
                else:
                    self.updateLOG('File has been saved: {}'.format(tmp))
            else:
                self.updateLOG('No filename has been provided')
        else:
            self.updateLOG('Gradient have not been calculated. No export of data.')



    def saveParams(self):
        '''
        Function for the window where the parameters of the output file
        are defined

        Returns
        -------
        None.

        '''
        
        def okBut(window):
            '''
            OK button

            Parameters
            ----------
            window : tk.Toplevel
                the window that it will be.

            Returns
            -------
            None.

            '''
            window.destroy()
            
        def cancelButton(window, r):
            '''
            Cancel button

            Parameters
            ----------
            window : tk.Toplevel
                the window that it will be.
            r : string
                separator.

            Returns
            -------
            None.

            '''
            self.sepOut.set(r)
            window.destroy()
        
        # Initial values - for use in cancel button
        # Initial separator
        initRadio = self.sepOut.get()
        
        window = tk.Toplevel(self.parent)
        window.title("Save Parameters")
        
        # Frame for the separators
        sepFrame = tk.Frame(window, bd=1, highlightthickness=1, highlightbackground='black')
        sepFrame.grid(row=0, column=0, sticky='nesw')
        
        # Holders for the separators
        label = tk.Label(sepFrame, text='Select separator:')
        label.grid(row=0, column=0)
        i = 1
        for sep, val in self.sepsNames.items():
            #tk.Radiobutton(sepFrame, text=val, variable=self.sepOut, 
            #       value=sep, command=chooseSep).grid(row=i, column=0, sticky='w')
            tk.Radiobutton(sepFrame, text=val, variable=self.sepOut, 
                   value=sep).grid(row=i, column=0, sticky='w')
            i += 1
        
        # Frame for OK and Cancel buttons
        butFrame = tk.Frame(window)
        butFrame.grid(row=1,column=0)
        
        # Cancel button
        quitButton = tk.Button(butFrame, text='Cancel', command=lambda : cancelButton(window, initRadio))
        quitButton.grid(row=0, column=1)

        # Saved file button
        saveButton = tk.Button(butFrame, text="Save file", command=lambda: self.saveFile(window), width=15)
        saveButton.grid(row=0, column=0)

        # OK button
        # okButton = tk.Button(butFrame, text="OK", command=lambda: okBut(window))
        # okButton.grid(row=0, column=0)

    def checkData(self, data):
        '''
        Creates a window in which the input/output data may be checked, if they 
        have been imported/created correctly.

        Parameters
        ----------
        data : pandas.DataFrame
            The input/output data.

        Returns
        -------
        None.

        '''
        
        def myPlot(data, zax, uaxis, scale, cslice):
            '''
            Function to plot the data

            Parameters
            ----------
            data : pandas.DataFrame
                data to plot.
            zax : string
                z-axis.
            uaxis : string
                the 2 dimensions that we plot.
            scale : string
                linear or log.
            cslice : int
                the slice of the 3rd axis that we plot.

            Returns
            -------
            None

            '''
            def createFig():
                '''
                Function to create a figure and a canvas

                Returns
                -------
                fig : Figure
                    DESCRIPTION.
                canvas : Canvas
                    DESCRIPTION.

                '''
                fig = Figure(dpi=80)
                fig.set_size_inches(6.5, 5.2)
                canvas = FigureCanvasTkAgg(fig, master=frameFig)
                canvas.get_tk_widget().grid(row=0,column=0, columnspan=3)
                return fig, canvas
            
            def UpdateButton(uaxis, zax, cslice, data, scale):
                '''
                Function to plot new slices

                Parameters
                ----------
                uaxis : string
                    the 2 dimensions that we plot..
                zax : string
                    z-axis.
                cslice : int
                    the slice of the 3rd axis that we plot.
                data : pandas.DataFrame
                    data to plot.
                scale : string
                    linear or log.

                Returns
                -------
                None.

                '''
                self.fig.clf() # Clear previous items
                self.fig, canvas = createFig()
                ax = self.fig.subplots()
                dpl.createPlot(self.fig, ax, uaxis, zax, cslice, data, scale)
                canvas.draw()
                
                
            def savePlot():
                '''
                Function to save the figure

                Returns
                -------
                None.

                '''
                ftypes = [('JPG', '*.jpg'), ('JPEG', '*.jpeg'), ('PNG', '*.png'), ('EPS', '*.eps'), ('TIFF', '*.tiff'), ('PDF', '*.pdf'), ('All files', '*')]
                tmp = filedialog.asksaveasfilename(defaultextension=('JPG', '*.jpg'), initialdir = "/", title = "Select file", filetypes = ftypes)
                if tmp != '':
                    #dpl.saveFig(self.fig, tmp)
                    cformat = tmp.split('.')[-1]
                    fname = ".".join(tmp.split('.')[:-1])
                    self.fig.savefig('{}.{}'.format(fname, cformat), format=cformat, dpi=300, bbox_inches='tight')
            
            # Figure
            window = tk.Toplevel(self.parent)
            window.title('Figure')
            
            # Slider
            frameSlice = tk.LabelFrame(window, text='Slice')
            frameSlice.grid(row=0, column=0, columnspan=3)

            # Identify the 3rd dimension, whose slice we get
            tmpDimList = [str(data.columns[0]), str(data.columns[1]), str(data.columns[2])]
            tmpDimList.remove(uaxis.split('-')[0])
            tmpDimList.remove(uaxis.split('-')[1])
            
            # Get the number of slices that exist
            limits = set(list(data[tmpDimList[0]]))
            
            # Create slider
            cslider = tk.Scale(frameSlice, from_=0, to=len(limits)-1, orient=tk.HORIZONTAL)
            cslider.grid()
            
            # Frame for the figure
            frameFig = tk.Frame(window)
            frameFig.grid(row=1, column=0, columnspan=3)
            
            # Create figure
            self.fig, canvas = createFig()        
            ax = self.fig.subplots()
            
            # Plot
            dpl.createPlot(self.fig, ax, uaxis, zax, 0, data, scale)
            
            # Update button
            updateBut = tk.Button(frameSlice, text='Update plot', command=lambda:UpdateButton(uaxis, zax, cslider.get(), data, scale))
            updateBut.grid(row=0, column=4)
            
            canvas.draw()
            
            # Frame for matplotlib toolbar
            frameToolbar = tk.Frame(master=window)
            frameToolbar.grid(row=2,column=0)
            
            # Matplotlib toolbar
            toolbar= NavigationToolbar2Tk(canvas, frameToolbar)
            toolbar.grid(row=0, column=0, columnspan=2)
            
            # Save button
            b2 = tk.Button(frameToolbar, text='Save', command=lambda:savePlot(), width=20)
            b2.grid(row=0, column=2)

        
        window = tk.Toplevel(self.parent)
        window.title("Check Data")
        window.geometry('600x400')
        
        # Frame for the printing
        frame = tk.Frame(window)
        frame.grid(row=0, column=0, sticky='nesw')
        
        # Keep the first 20 rows of the dat
        tmp = data.head(20)
        
        # Print the first 20 rows of the data
        pt = pdt.Table(frame)
        pt.model.df = tmp
        pt.show()
                
        # Plot options
        framePlot = tk.LabelFrame(window, text='Plot')
        framePlot.grid(row=1, column=0, columnspan=4)
        
        # Variable for Z axis
        myVar = tk.StringVar()
        myVar.set('')
              
        tmptext = []
        plotEnabled = 'normal'
        # In case no data have been imported
        if len(data)==0:
            options = ['']
            tmptext.extend(['x-y', 'x-z', 'y-z'])
            plotEnabled = 'disabled'
        else:
            options = list(data.columns[3:])
            # Create pairs of coordinates
            for i in range(3):
                if not data.iloc[:,i].eq(data.iloc[:,i].iloc[0]).all():
                    for j in range(i+1,3):
                        if not data.iloc[:,j].eq(data.iloc[:,j].iloc[0]).all():
                            tmptext.append('{}-{}'.format(data.columns[i], data.columns[j]))

        myVar.set(options[0])
        
        # Choose which Dimension to plot
        frameDim = tk.LabelFrame(framePlot, text='Plane')
        frameDim.grid(row=0, column=2)
        for num in range(len(tmptext)):            
            tk.Radiobutton(frameDim, text=tmptext[num], variable=self.dataDim, value=num, state=plotEnabled).grid(row=0, column=num, sticky='w')
        
        # Choose z-axis
        zLabel = tk.Label(framePlot, text='Choose z-Axis: ')
        zLabel.grid(row=0, column=0)
        w = tk.OptionMenu(framePlot, myVar, *options)
        w.grid(row=0, column=1)

        # Button to plot
        frameBut = tk.Frame(framePlot)
        frameBut.grid(row=0, column=4)

        b1 = tk.Button(frameBut, text='Plot', command=lambda: myPlot(data, myVar.get(), tmptext[self.dataDim.get()], 'linear', 0), state=plotEnabled)
        b1.grid(row=0, column=0)



    def calculateGradients(self):
        '''
        Function to apply the required steps for the calculation
        of the gradients

        Returns
        -------
        None.

        '''
        # Check if the imported data is empty
        if not self.inData.empty:
            self.updateLOG('Now calculating gradients')
            try:                
                # Calculate gradients
                self.gradData = cg.Grads(self.inData)
            except:
                self.updateLOG('There was a problem in calculating the gradients. Please try again.')
            else:
                self.updateLOG('Gradients have been calculated')
        else:
            self.updateLOG('!!!No input data!!!')



    def initUI(self):
        '''
        Initialize the main window.

        Returns
        -------
        None.

        '''
        # Window title
        self.parent.title("Gradients Calculator")

        # Define the menubar
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        # File menu
        fileMenu = tk.Menu(menubar, tearoff=0)
        #fileMenu.add_command(label="Open", command=self.openFile)
        fileMenu.add_command(label='Exit', command=self.parent.destroy)
        menubar.add_cascade(label="File", menu=fileMenu)    
        # Settings menu
        settingsMenu = tk.Menu(self.parent, tearoff=0)
        settingsMenu.add_command(label='Import parameters', command=self.openParams)
        settingsMenu.add_command(label='Check Input data', command=lambda : self.checkData(self.inData))
        settingsMenu.add_command(label='Check Gradient data', command=lambda : self.checkData(self.gradData))
        settingsMenu.add_command(label='Save parameters', command=self.saveParams)
        menubar.add_cascade(label="Settings", menu=settingsMenu)   
        # Information menu
        aboutMenu = tk.Menu(self.parent, tearoff=0)
        aboutMenu.add_command(label='Help', command=self.helpMenu)
        aboutMenu.add_command(label='About', command=self.aboutMenu)
        menubar.add_cascade(label="Information", menu=aboutMenu)   
        
        mrow = 0
        
        # Open parameters button
        openParBut = tk.Button(self.parent, text="Open file", command=self.openParams, width=15)
        openParBut.grid(row=mrow, column=0)
        
        
        # Check input data button (if data have been inserted correctly)
        checkDataButton = tk.Button(self.parent, text="Check Data", command=lambda : self.checkData(self.inData), width=15)
        checkDataButton.grid(row=mrow, column=2)
        
        # Calculate gradients button
        calcGradButton = tk.Button(self.parent, text="Calculate Gradients", command=self.calculateGradients)
        calcGradButton.grid(row=mrow + 1, column=0)
        
        # Check gradients data button
        checkGradButton = tk.Button(self.parent, text="Check Gradient Data", command=lambda : self.checkData(self.gradData), width=15)
        checkGradButton.grid(row=mrow + 1, column=1)

        # Save parameters button
        saveParBut = tk.Button(self.parent, text="Save File", command=self.saveParams, width=15)
        saveParBut.grid(row=mrow + 2, column=0)
        

def main():

    root = tk.Tk()
    root.resizable(width=False, height=False)
    ex = Window(root)
    # root.geometry("460x200")
    root.geometry("485x240")
    root.mainloop()  


if __name__ == '__main__':
    main()