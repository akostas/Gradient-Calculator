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
import pandastable as pdt

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
        
        self.log_area = st.ScrolledText(self.parent, width = 50,height = 5, font = ("Times New Roman", 11), state='disabled' )
        self.log_area.grid(row=10, column=0, pady = 10, padx = 10, columnspan=2) 
       
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

    def updateLOG(self, logtext):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.INSERT, '{}\n'.format(logtext))    
        self.log_area.update()
        self.log_area.yview(tk.END)
        self.log_area.configure(state='disabled')


    def openFile(self):
        ftypes = [('Text files', '*.txt'), ('CSV files', '*.csv'), ('Dat files', '*.dat'), ('All files', '*')]
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
        if not self.gradData.empty:

            self.updateLOG('Now saving file')

            print('Test')
            ftypes = [('Text files', '*.txt'), ('CSV files', '*.csv'), ('Dat files', '*.dat'), ('All files', '*')]
            tmp = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = ftypes)
            if tmp != '':
                self.outfile.set(tmp)
                print(self.outfile.get())
                #self.outData = self.inData.to_csv(tmp, sep=self.seps[self.sepOut.get()], index=False)
                self.gradData.to_csv(tmp, sep=self.seps[self.sepOut.get()], index=False)
                self.updateLOG('File has been saved: {}'.format(tmp))

                print('Number of columns: {}'.format(len(self.gradData.columns)))
                print(self.gradData.head(20))
            else:
                self.updateLOG('No filename has been provided')
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
            print(self.sepIn.get())
        
        window = tk.Toplevel(self.parent)
        window.title("Open Parameters")
        window.geometry('160x180')
        
        initEntry = self.ird.get()
        initRadio = self.sepIn.get()
        
        
        rowsFrame = tk.Frame(window)
        rowsFrame.grid(row=0, column=0)
        
        labelRows = tk.Label(rowsFrame, text='Initial rows to delete').grid(row=0, column=0)      
        txtBox = tk.Entry(rowsFrame, textvariable = self.ird, width=6).grid(row=0, column=1) #entry textbox

        sepFrame = tk.Frame(window, bd=1, highlightthickness=1, highlightbackground='black')
        sepFrame.grid(row=1, column=0, sticky='nesw')

        label = tk.Label(sepFrame, text='Select separator:').grid(row=0, column=0)
        i=1
        for sep, val in self.sepsNames.items():
            tk.Radiobutton(sepFrame, text=val, variable=self.sepIn, 
                   value=sep, command=chooseSep).grid(row=i, column=0, sticky='w')
            i += 1
            
        
        butFrame = tk.Frame(window)
        butFrame.grid(row=2,column=0)
        
        quitButton = tk.Button(butFrame, text='Cancel', command=lambda : cancelButton(window,initEntry, initRadio))
        quitButton.grid(row=2, column=1)
   
        okButton = tk.Button(butFrame, text="OK", command=lambda: okBut(window))
        okButton.grid(row=2, column=0)

    def saveParams(self):
        
        def okBut(window):
            print(self.sepOut.get())
            window.destroy()
            
        def cancelButton(window, r):
            self.sepOut.set(r)
            window.destroy()
        
        def chooseSep():
            print(self.sepOut.get())
        
        initRadio = self.sepOut.get()
        
        window = tk.Toplevel(self.parent)
        window.title("Save Parameters")
        
        sepFrame = tk.Frame(window, bd=1, highlightthickness=1, highlightbackground='black')
        sepFrame.grid(row=0, column=0, sticky='nesw')
        
        label = tk.Label(sepFrame, text='Select separator:').grid(row=0, column=0)
        i = 1
        for sep, val in self.sepsNames.items():
            tk.Radiobutton(sepFrame, text=val, variable=self.sepOut, 
                   value=sep, command=chooseSep).grid(row=i, column=0, sticky='w')
            i += 1
            
        butFrame = tk.Frame(window)
        butFrame.grid(row=1,column=0)
        
        quitButton = tk.Button(butFrame, text='Cancel', command=lambda : cancelButton(window, initRadio))
        quitButton.grid(row=0, column=1)

    
        okButton = tk.Button(butFrame, text="OK", command=lambda: okBut(window))
        okButton.grid(row=0, column=0)

    def checkInputData(self):
        window = tk.Toplevel(self.parent)
        window.title("Check Input Data")
        window.geometry('600x400')
        
        frame = tk.Frame(window)
        frame.grid(row=0, column=0, sticky='nesw')
        
        tmp = self.inData.head(20)
        
        pt = pdt.Table(frame)
        pt.model.df = tmp
        pt.show()
        
        '''for num, col in enumerate(tmp.columns):
            print(col)
            tk.Entry(frame, text=col, width=10).grid(row=0, column=num)
        
        for index, row in tmp.iterrows():
            for num, col in enumerate(tmp.columns):
                tk.Label(frame, text='{:.6f}'.format(row[col]), width=10, borderwidth=2, relief='ridge', padx=0, pady=0).grid(row=index+1, column=num)'''
        
        
        
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

        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=self.openFile)
        fileMenu.add_command(label='Exit', command=self.parent.destroy)
        menubar.add_cascade(label="File", menu=fileMenu)    
        
        settingsMenu = tk.Menu(self.parent, tearoff=0)
        settingsMenu.add_command(label='Import parameters', command=self.openParams)
        settingsMenu.add_command(label='Edit data', command=lambda : self.checkInputData())
        settingsMenu.add_command(label='Save parameters', command=self.saveParams)
        menubar.add_cascade(label="Settings", menu=settingsMenu)   

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
        openButton.grid(row=mrow, column=1)
        
        # Check input data button (if data have been inserted correctly)
        checkDataButton = tk.Button(self.parent, text="Check Data", command=lambda : self.checkInputData(), width=15)
        checkDataButton.grid(row=mrow + 2, column=0)
        
 
        # Calculate gradients button
        calcGradButton = tk.Button(self.parent, text="Calculate Gradients", command=self.calculateGradients)
        calcGradButton.grid(row=mrow + 2, column=1)
        

        # Saved file button
        saveButton = tk.Button(self.parent, text="Save file", command=self.saveFile, width=15)
        saveButton.grid(row=mrow + 3, column=1)


        # Save parameters button
        saveParBut = tk.Button(self.parent, text="Save Parameters", command=self.saveParams, width=15)
        saveParBut.grid(row=mrow + 3, column=0)
        
        
        
        


def main():

    root = tk.Tk()
    ex = Window(root)
    root.geometry("400x200")
    root.mainloop()  


if __name__ == '__main__':
    main()