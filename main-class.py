# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 16:33:44 2021

@author: Konstantinos
"""


#from tkinter import Frame, Tk, BOTH, Text, Menu, END
import tkinter as tk
#from tkinter import filedialog

class Window(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   

        self.parent = parent        
        self.initUI()

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


    def onOpen(self):

        ftypes = [('CSV files', '*.csv'), ('Dat files', '*.dat'), ('Text files', '*.txt'), ('All files', '*')]
        dlg = tk.filedialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            self.txt.insert(END, text)

    def readFile(self, filename):

        f = open(filename, "r")
        text = f.read()
        return text
    
    def aboutMenu(self):
        tk.messagebox.showinfo("About", "This software has been created by Konstantinos Angelou!\nemail: angelou.konstantinos@gmail.com")
    
    def helpMenu(self):
        tk.messagebox.showinfo("Help", "This software is useful when you want to calculate the gradients of the magnetic field that has occurred from Sim4Life. The data from Sim4Life can be imported here (as is) and the gradients will be calculated for every direction.")


def main():

    root = tk.Tk()
    ex = Window(root)
    root.geometry("800x600")
    root.mainloop()  


if __name__ == '__main__':
    main()