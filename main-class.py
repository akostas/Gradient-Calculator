# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 16:33:44 2021

@author: Konstantinos Angelou
"""

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import calcgrads as cg
import time
import tkinter.scrolledtext as st 
import pandastable as pdt
import datetime as dtm

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
        
        self.log_area = st.ScrolledText(self.parent, width=70, height=7, font=("Times New Roman", 8), state='disabled' )
        self.log_area.grid(row=10, column=0, pady=10, padx=10, columnspan=3)
        
        # Define input file
        self.inSource = tk.IntVar()
        self.inSource.set(1)
        self.inSourceLabel = tk.StringVar()
        self.inSourceLabel.set('Sim4Life')
        
        # Other file
        self.conHeaders = tk.IntVar() # Contains headers
        self.conHeaders.set(1)
        '''self.setHeaders = tk.IntVar() # Set new headers
        self.setHeaders.set(0)
        self.noColumns = tk.IntVar() # Number of columns
        self.noColumns.set(6)
        self.xCol = tk.StringVar() # Column x
        self.xCol.set('x')
        self.yCol = tk.StringVar() # Column y
        self.yCol.set('y')
        self.zCol = tk.StringVar() # Column z
        self.zCol.set('z')
        self.bxCol = tk.StringVar() # Column Bx
        self.bxCol.set('Bx')
        self.byCol = tk.StringVar() # Column By
        self.byCol.set('By')
        self.bzCol = tk.StringVar() # Column Bz
        self.bzCol.set('Bz')
        self.bCol = tk.StringVar() # Column B
        self.bCol.set('B')'''
       
        self.initUI()

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
            Contains the input data (Magnetic field).
        '''
        if self.inSource.get() == 1:
            data = cg.readData(filename, int(self.ird.get()), self.seps[self.sepIn.get()])
        else:
            data = pd.read_csv(filename, sep=self.seps[self.sepIn.get()], encoding='utf8')
        return data
    
    
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
        window = tk.Toplevel(self.parent)
        window.title("Help")
        window.geometry('700x500')
        
        helptext = '''This software is used to calculate the gradients of the magnetic field using the exported file from Sim4Life.\nThe steps to calculate the gradients are the following:\n\n  1) Import Parameters: Define the characteristics of the input file. First select if it is a Sim4Life file and leave the default parameters. If it is not a Sim4Life file, then select "Other". If the file includes headers, then check "Contains headers", else un-check it. You should also select the proper separator between the columns.\n\n  2) Open File: Choose the file with the data that need to be imported. The data must contain 4 or 6 columns. The first 3 columns are the three dimensions (x,y,z). If there are 4 columns, the 4th column is the absolute value of the vector. If there are 6 columns, the last 3 columns are the magnetic field in each direction (x,y,z).\n\n  3) Check Data: A table shows the first 10 lines to check whether the data have been imported correctly.\n\n  4) Calculate Gradients: Calculate the gradients in every direction using the gradient function from numpy library.\n\n  5) Check Gradient Data: A table shows the first 10 lines to check whether the gradients have been calculated correctly.\n\n  6) Save Parameters: Define the characteristics of the output file (e.g. column separator).\n\n  7) Save File: Save the gradients into a text file.\n'''
        
        label = tk.Label(window, text=helptext, wraplength=700, justify='left', font=12).grid(row=0, column=0)

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


    def openFile(self):
        '''
        Function to open the input data. They are assigned to inData variable.

        Returns
        -------
        None.

        '''
        # Define file types
        ftypes = [('Text files', '*.txt'), ('CSV files', '*.csv'), ('Dat files', '*.dat'), ('All files', '*')]
        # Open the file        
        tmp = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = ftypes)
        
        if tmp != '':
            self.infile.set(tmp)
            print(self.infile.get())
            print('Now opening file...')
            
            self.updateLOG('Now opening file: {}'.format(tmp))

            self.inData = self.readFile(tmp)       
            self.updateLOG('File is now open.')

            print('Number of columns: {}'.format(len(self.inData.columns)))
            print(self.inData.head(10))
        else:
            self.updateLOG('No file has been provided')

    def saveFile(self):
        '''
        Function to save the gradients data into a file.

        Returns
        -------
        None.

        '''
        if not self.gradData.empty:

            self.updateLOG('Now saving file')

            # Define file types
            ftypes = [('Text files', '*.txt'), ('CSV files', '*.csv'), ('Dat files', '*.dat'), ('All files', '*')]
            tmp = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = ftypes)
            if tmp != '':
                self.outfile.set(tmp)
                print(self.outfile.get())
                # Write the data to the file
                self.gradData.to_csv('{}'.format(tmp), sep=self.seps[self.sepOut.get()], index=False)
                self.updateLOG('File has been saved: {}'.format(tmp))

                print('Number of columns: {}'.format(len(self.gradData.columns)))
                print(self.gradData.head(20))
            else:
                self.updateLOG('No filename has been provided')
        else:
            self.updateLOG('No data to save')
        

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
            print(self.ird.get())
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
        
        '''def chooseSep():
            print(self.sepIn.get())'''
        
        
        def selSim4Life(window):
            '''
            Frame to define the parameters for a Sim4Life input file.

            Parameters
            ----------
            window : tk.Toplevel
                the window that it will be.

            Returns
            -------
            None.

            '''
            # Delete previous holders that exist
            for wid in window.grid_slaves():
                wid.grid_forget()

            # Set the Label to Sim4Life
            self.inSourceLabel.set('Sim4Life')

            # Create a new frame
            rowsFrame = tk.Frame(window)
            rowsFrame.grid(row=0, column=0)
            
            # Holders for the rows that need to be deleted
            labelRows = tk.Label(rowsFrame, text='Initial rows to delete').grid(row=0, column=0)      
            txtBox = tk.Entry(rowsFrame, textvariable = self.ird, width=6).grid(row=0, column=1) #entry textbox
    
            # Frame for the separators
            sepFrame = tk.Frame(window, bd=1, highlightthickness=1, highlightbackground='black')
            sepFrame.grid(row=1, column=0, sticky='nesw')
            
            # Holders for the separators
            label = tk.Label(sepFrame, text='Select separator:').grid(row=0, column=0)
            i=1
            for sep, val in self.sepsNames.items():
                #tk.Radiobutton(sepFrame, text=val, variable=self.sepIn,  
                #       value=sep, command=chooseSep).grid(row=i, column=0, sticky='w')
                tk.Radiobutton(sepFrame, text=val, variable=self.sepIn,  
                       value=sep).grid(row=i, column=0, sticky='w')
                i += 1
            
        
        def selOther(window):
            '''
            

            Parameters
            ----------
            window : tk.Toplevel
                the window that it will be.

            Returns
            -------
            None.

            '''
            # Delete previous holders that exist
            for wid in window.grid_slaves():
                wid.grid_forget()
            
            # Set the Label to Other
            self.inSourceLabel.set('Other')
            
            # Define if the input file contains headers
            ch1 = tk.Checkbutton(window, text='Contains headers', variable=self.conHeaders, onvalue=1, offvalue=0).grid(row=1, column=0)
            
            # Frame for the separators
            sepFrame = tk.Frame(window, bd=1, highlightthickness=1, highlightbackground='black')
            sepFrame.grid(row=2, column=0, sticky='nesw')
            
            # Holders for the separators
            label = tk.Label(sepFrame, text='Select separator:').grid(row=0, column=0)
            i=1
            for sep, val in self.sepsNames.items():
                #tk.Radiobutton(sepFrame, text=val, variable=self.sepIn, 
                #       value=sep, command=chooseSep).grid(row=i, column=0, sticky='w')
                tk.Radiobutton(sepFrame, text=val, variable=self.sepIn, 
                       value=sep).grid(row=i, column=0, sticky='w')
                i += 1
            
    
            """
            def changeState(frame):
                '''
                

                Parameters
                ----------
                frame : TYPE
                    DESCRIPTION.

                Returns
                -------
                None.

                '''
                print(self.setHeaders.get())
                '''for wid in frame.grid_slaves():
                    wid.configure(state='normal' if self.setHeaders==1 else 'disabled')'''
                if frame.winfo_children:               
                    for w in frame.winfo_children():
                        if self.setHeaders.get():
                            w.configure(state='normal')
                        else:
                            w.configure(state='disabled')
              """             
        
        
        window = tk.Toplevel(self.parent)
        window.title("Open Parameters")
        window.geometry('300x250')
        
        # Initial values - for use in cancel button
        # Initial value of rows that need to be deleted (for Sim4Life file)
        initEntry = self.ird.get()
        # Initial separator
        initRadio = self.sepIn.get()
        # Initial headers
        initHeaders = self.conHeaders.get()
        
        # LabelFrame based on selection
        tmpLabel = tk.Label(window, textvariable=self.inSourceLabel)
        labelFr = tk.LabelFrame(window, labelwidget=tmpLabel)
        labelFr.grid(row=1, column=0)
        selSim4Life(labelFr)
        
        # Frame for radiobuttons
        rbFrame = tk.Frame(window)
        rbFrame.grid(row=0, column=0)
        
        # Radiobuttons - selection between Sim4Life and Other
        rb1 = tk.Radiobutton(rbFrame, text='Sim4Life', variable=self.inSource, value=1, command=lambda:selSim4Life(labelFr)).grid(row=0, column=0)
        rb2 = tk.Radiobutton(rbFrame, text='Other', variable=self.inSource, value=2, command=lambda: selOther(labelFr)).grid(row=0, column=1)
        
        # Frame for OK and Cancel buttons
        butFrame = tk.Frame(window)
        butFrame.grid(row=2,column=0)
        
        # Cancel button
        quitButton = tk.Button(butFrame, text='Cancel', command=lambda : cancelButton(window, initEntry, initRadio, initHeaders))
        quitButton.grid(row=0, column=1)
        
        # OK button
        okButton = tk.Button(butFrame, text="OK", command=lambda: okBut(window))
        okButton.grid(row=0, column=0)

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
            print(self.sepOut.get())
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
        
        '''def chooseSep():
            print(self.sepOut.get())'''
        
        # Initial values - for use in cancel button
        # Initial separator
        initRadio = self.sepOut.get()
        
        window = tk.Toplevel(self.parent)
        window.title("Save Parameters")
        
        # Frame for the separators
        sepFrame = tk.Frame(window, bd=1, highlightthickness=1, highlightbackground='black')
        sepFrame.grid(row=0, column=0, sticky='nesw')
        
        # Holders for the separators
        label = tk.Label(sepFrame, text='Select separator:').grid(row=0, column=0)
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

        # OK button
        okButton = tk.Button(butFrame, text="OK", command=lambda: okBut(window))
        okButton.grid(row=0, column=0)

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
        
        window = tk.Toplevel(self.parent)
        window.title("Check Input Data")
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
          
    """   
    def checkGradData(self):
        '''
        Creates a window in which the input data may be checked, if they 
        have been imported correctly.

        Returns
        -------
        None.

        '''
        window = tk.Toplevel(self.parent)
        window.title("Check Gradient Data")
        window.geometry('600x400')
        
        # Frame for the printing
        frame = tk.Frame(window)
        frame.grid(row=0, column=0, sticky='nesw')
        
        tmp = self.gradData.head(20)
        
        pt = pdt.Table(frame)
        pt.model.df = tmp
        pt.show()
    """   
        
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
            print('Now calculating gradients.')
            # Check if the imported data is of the proper format
            if len(self.inData.columns)==4 or len(self.inData.columns)==6:
                self.gradData = cg.Grads(self.inData)
                self.updateLOG('Gradients have been calculated')
                print('They have been calculated')
                print(self.gradData.head(10))
            else:
                self.updateLOG('ERROR!!!Check Help->Information for proper input files!')
        else:
            self.updateLOG('!!!No input data!!!')

    def initUI(self):
        '''
        Initialize all the buttons, menus etc.

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
        fileMenu.add_command(label="Open", command=self.openFile)
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
        openParBut = tk.Button(self.parent, text="Import Parameters", command=self.openParams, width=15)
        openParBut.grid(row=mrow, column=0)
        
        # Open file button
        openButton = tk.Button(self.parent, text="Open File", command=self.openFile, width=15)
        openButton.grid(row=mrow, column=2)
        
        # Check input data button (if data have been inserted correctly)
        checkDataButton = tk.Button(self.parent, text="Check Data", command=lambda : self.checkData(self.inData), width=15)
        checkDataButton.grid(row=mrow + 2, column=0)
        
        # Calculate gradients button
        calcGradButton = tk.Button(self.parent, text="Calculate Gradients", command=self.calculateGradients)
        calcGradButton.grid(row=mrow + 2, column=1)
        
        # Check input data button (if data have been inserted correctly)
        checkGradButton = tk.Button(self.parent, text="Check  Gradient Data", command=lambda : self.checkData(self.gradData), width=15)
        checkGradButton.grid(row=mrow + 2, column=2)
        
        # Saved file button
        saveButton = tk.Button(self.parent, text="Save file", command=self.saveFile, width=15)
        saveButton.grid(row=mrow + 3, column=2)

        # Save parameters button
        saveParBut = tk.Button(self.parent, text="Save Parameters", command=self.saveParams, width=15)
        saveParBut.grid(row=mrow + 3, column=0)
        

def main():

    root = tk.Tk()
    ex = Window(root)
    root.geometry("460x200")
    root.mainloop()  


if __name__ == '__main__':
    main()