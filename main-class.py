# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 16:33:44 2021

@author: Konstantinos
"""


#from tkinter import Frame, Tk, BOTH, Text, Menu, END
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import calcgrads as cg
import time
import tkinter.scrolledtext as st 

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
       
        self.log_area = st.ScrolledText(self.parent, width = 30,height = 5, font = ("Times New Roman", 15), state='disabled' )
        self.log_area.grid(row=10, column = 0, pady = 10, padx = 10) 
       
        self.initUI()

    '''def onOpen(self):

        ftypes = [('CSV files', '*.csv'), ('Dat files', '*.dat'), ('Text files', '*.txt'), ('All files', '*')]
        dlg = tk.filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            self.txt.insert(END, text)'''

    def readFile(self, filename):

        '''f = open(filename, "r")
        text = f.read()
        return text'''
        # data = pd.read_csv(filename, sep=self.seps[self.sepIn.get()], encoding='utf8')
        data = cg.readData(filename, int(self.ird.get()), self.seps[self.sepIn.get()])
        return data
    
    def aboutMenu(self):
        tk.messagebox.showinfo("About", "This software has been created by Konstantinos Angelou!\nemail: angelou.konstantinos@gmail.com")
    
    def helpMenu(self):
        tk.messagebox.showinfo("Help", "This software is useful when you want to calculate the gradients of the magnetic field that has occurred from Sim4Life. The data from Sim4Life can be imported here (as is) and the gradients will be calculated for every direction.")

    def updateLOG(self, text):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.INSERT, '{}\n'.format(text))      
        self.log_area.update()
        self.log_area.yview(tk.END)
        self.log_area.configure(state='disabled')


    def openFile(self):
        ftypes = [('Text files', '*.txt'), ('CSV files', '*.csv'), ('Dat files', '*.dat'), ('All files', '*')]
        tmp = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = ftypes)
        self.infile.set(tmp)
        print(self.infile.get())
        
        if tmp != '':
            print('Now opening file...')
            
            self.updateLOG('Now opening file...')

            self.inData = self.readFile(tmp)       
            self.updateLOG('File is now open.')

            print('Number of columns: {}'.format(len(self.inData.columns)))
            print(self.inData.head(10))

    def saveFile(self):
        if not self.gradData.empty:

            self.updateLOG('Now saving file')

            print('Test')
            ftypes = [('Text files', '*.txt'), ('CSV files', '*.csv'), ('Dat files', '*.dat'), ('All files', '*')]
            tmp = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = ftypes)
            self.outfile.set(tmp)
            print(self.outfile.get())
            if tmp != '':
                #self.outData = self.inData.to_csv(tmp, sep=self.seps[self.sepOut.get()], index=False)
                self.gradData.to_csv(tmp, sep=self.seps[self.sepOut.get()], index=False)
                self.updateLOG('File has been saved')

                print('Number of columns: {}'.format(len(self.gradData.columns)))
                print(self.gradData.head(20))
        else:
            self.updateLOG('No data to save')
        

    def openParams(self):
        
        def okBut(window):
            #tmp = txtBox.get()
            #self.ird.set(tmp)
            print(self.ird.get())
            window.destroy()
            
        def cancelButton(window, e, r):
            self.ird.set(e)
            self.sepIn.set(r)
            window.destroy()
        
        def chooseSep():
            #self.sepIn.set(s)
            print(self.sepIn.get())
        
        window = tk.Toplevel(self.parent)
        window.title("Open Parameters")
        
        initEntry = self.ird.get()
        initRadio = self.sepIn.get()
        
        labelRows = tk.Label(window, text='Initial rows to delete').grid(row=0, column=0)      
        txtBox = tk.Entry(window, textvariable = self.ird).grid(row=0, column=2) #entry textbox

        i = 3
        label = tk.Label(window, text='Select separator:').grid(row=i, column=0)
        for sep, val in self.sepsNames.items():
            i += 1
            tk.Radiobutton(window, text=val, variable=self.sepIn, 
                   value=sep, command=chooseSep).grid(row=i, column=0)
            
        quitButton = tk.Button(window, text='Cancel', command=lambda : cancelButton(window,initEntry, initRadio))
        #quitButton.bind("<Button>", lambda e: cancelButton(window,initEntry, initRadio))
        quitButton.grid(row=i+2, column=1)

        okButton = tk.Button(window, text="OK", command=lambda: okBut(window))
        #okButton.bind("<Button>", lambda e: okBut(window))
        okButton.grid(row=i+2, column=0)

    def saveParams(self):
        
        def chooseSep():
            #self.sepIn.set(s)
            print(self.sepOut.get())
        
        window = tk.Toplevel(self.parent)
        window.title("Save Parameters")
        i = 0
        label = tk.Label(window, text='Select separator:').grid(row=i, column=0)
        for sep, val in self.sepsNames.items():
            i += 1
            tk.Radiobutton(window, text=val, variable=self.sepOut, 
                   value=sep, command=chooseSep).grid(row=i, column=0)

    def checkInputData(self):
        pass
        
    def calculateGradients(self):
        if not self.inData.empty:
            self.updateLOG('Now calculating gradients')
            print('Now calculating gradients.')   
            self.gradData = cg.Grads(self.inData)
            self.updateLOG('Gradients have been calculated')
            print('They have been calculated')
            print(self.gradData.head(10))
        else:
            self.updateLOG('!!!No input data!!!')

    def initUI(self):

        self.parent.title("Gradients Calculator")
        #self.pack(fill=tk.BOTH, expand=1)

        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Open")
        fileMenu.add_command(label='Exit', command=self.parent.destroy)
        menubar.add_cascade(label="File", menu=fileMenu)    
        
        settingsMenu = tk.Menu(self.parent)
        settingsMenu.add_command(label='Import parameters')
        settingsMenu.add_command(label='Edit data')
        menubar.add_cascade(label="Settings", menu=settingsMenu)   

        aboutMenu = tk.Menu(self.parent)
        aboutMenu.add_command(label='Help', command=self.helpMenu)
        aboutMenu.add_command(label='About', command=self.aboutMenu)
        menubar.add_cascade(label="Information", menu=aboutMenu)   
        
        mrow = 0
        
        # Open parameters button
        openParBut = tk.Button(self.parent, text="Open Parameters", command=self.openParams)
        openParBut.grid(row=mrow, column=0)
        
        # Opened file path
        openLabel = tk.Label(self.parent, textvariable=self.infile)
        #openLabel.pack(side=tk.RIGHT)
        openLabel.grid(row=mrow + 1, column=1)

        # Log Label
        #logLabel = tk.Label(self.parent, textvariable=self.logText)
        #logLabel.grid(row=mrow + 5, column=1)

        # Open file button
        openButton = tk.Button(self.parent, text="Open", command=self.openFile)
        #openButton.bind("<Button>", lambda e: self.openFile(openLabel, logLabel))
        openButton.grid(row=mrow + 1, column=0)
        
        # Check input data button (if data have been inserted correctly)
        checkDataButton = tk.Button(self.parent, text="Check Data", command=lambda : self.checkInputData())
        #checkDataButton.bind("<Button>", lambda e: self.checkInputData)
        checkDataButton.grid(row=mrow + 2, column=0)
        
        
        
        
        # Calculate gradients button
        calcGradButton = tk.Button(self.parent, text="Calculate Gradients", command=self.calculateGradients)
        #calcGradButton.bind("<Button>", lambda e: self.calculateGradients)
        calcGradButton.grid(row=mrow + 2, column=1)
        

        # Saved file path
        saveLabel = tk.Label(self.parent, textvariable=self.outfile)
        saveLabel.grid(row=mrow + 4, column=1)

        # Saved file button
        saveButton = tk.Button(self.parent, text="Save", command=self.saveFile)
        #saveButton.bind("<Button>", lambda e: self.saveFile(saveLabel, logLabel)) 
        saveButton.grid(row=mrow + 4, column=0)


        # Save parameters button
        saveParBut = tk.Button(self.parent, text="Save Parameters", command=self.saveParams)
        saveParBut.grid(row=mrow + 3, column=0)
        
        
      
        


def main():

    root = tk.Tk()
    ex = Window(root)
    root.geometry("800x600")
    root.mainloop()  


if __name__ == '__main__':
    main()