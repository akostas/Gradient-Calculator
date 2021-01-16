# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 16:33:44 2021

@author: Konstantinos
"""


#from tkinter import Frame, Tk, BOTH, Text, Menu, END
import tkinter as tk
from tkinter import filedialog
import pandas as pd

class Window(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   
        self.infile = tk.StringVar()
        #self.infile.set()
        self.outfile = tk.StringVar()
        self.outfile.set('')
        self.parent = parent  
        self.inData = pd.DataFrame()
        self.initUI()

    def onOpen(self):

        ftypes = [('CSV files', '*.csv'), ('Dat files', '*.dat'), ('Text files', '*.txt'), ('All files', '*')]
        dlg = tk.filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            self.txt.insert(END, text)

    def readFile(self, filename, msep=' '):

        '''f = open(filename, "r")
        text = f.read()
        return text'''
        data = pd.read_csv(filename, sep=' ', encoding='utf8')
        return data
    
    def aboutMenu(self):
        tk.messagebox.showinfo("About", "This software has been created by Konstantinos Angelou!\nemail: angelou.konstantinos@gmail.com")
    
    def helpMenu(self):
        tk.messagebox.showinfo("Help", "This software is useful when you want to calculate the gradients of the magnetic field that has occurred from Sim4Life. The data from Sim4Life can be imported here (as is) and the gradients will be calculated for every direction.")


    def openFile(self, label):
        ftypes = [('Text files', '*.txt'), ('CSV files', '*.csv'), ('Dat files', '*.dat'), ('All files', '*')]
        tmp = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = ftypes)
        self.infile.set(tmp)
        label.configure(text=tmp)
        print(self.infile.get())
        if tmp != '':
            self.inData = self.readFile(tmp)
            print(self.inData)


    def initUI(self):

        self.parent.title("Gradients Calculator")
        self.pack(fill=tk.BOTH, expand=1)

        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
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

        self.txt = tk.Text(self)
        self.txt.pack(fill=tk.BOTH, expand=1)
        
        

        # Opened file path
        openLabel = tk.Label(self.parent, text='Here is the path')
        openLabel.pack(side=tk.RIGHT)

        # Open file button
        openButton = tk.Button(self.parent, text="Open")
        openButton.bind("<Button>", lambda e: self.openFile(openLabel)) 
        openButton.pack(side=tk.LEFT)



def main():

    root = tk.Tk()
    ex = Window(root)
    root.geometry("800x600")
    root.mainloop()  


if __name__ == '__main__':
    main()