# Author: Maciej Madej

"""
Script reads XP.CNF and creates file counters.txt, which contains
TTG/TTR output configuration and variables definitions
"""

import tkinter as tk
import webbrowser
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import messagebox

class App(object):

    def __init__(self):
        self.path=''

    def set_label(self,label_name):
        """Change label after choosing directory to directory path"""
        self.dir_path_label_var.set(label_name)

    def chooseDirectory(self):
        """Set [self.path] to chosen directory path and changes [dir_path_label_var]"""
        self.path=askdirectory()
        self.set_label(self.path)

    def getValue(self,spinbox_name):
        """Gets value from spinbox widget"""
        return spinbox_name.get()

    def extractSG(self, name):
        """Extracts SGs names from XP.CNF file"""
        file_path = name + "/XP.CNF"
        with open(file_path,'r') as f:
            sg = []
            enableReading = False
            for line in f:
                if line.startswith("/* Signal Groups */"):
                    enableReading = True
                    continue
                elif line.startswith("/* Detectors */"):
                    enableReading = False
                    break
                if enableReading and line is not "\n":
                    sg.append(line.split()[1])
        return(sg)

    def generate(self,path):
        """Generates all counters configuration and variables names and writes it to counters.txt"""
        try:
            SG = self.extractSG(path)
        except:
            SG=[]
            self.error_message()
        if SG:
            with open('counters.txt', 'w') as f:
                s=[""]*4
                j=1;

                for i in SG:
                    s[0] += "TTG{0}, ".format(i)
                    if i == SG[-1]:
                        s[0] += "TTR{0};\n".format(i)
                    else:
                        s[0] += "TTR{0}, ".format(i)

                for i in SG:
                    s[1] += "wxsf({0},TTG{1}); \n".format(str(100+j),i)
                    j += 1
                    s[1] += "wxsf({0},TTR{1}); \n".format(str(100+j),i)
                    j += 1
                    if j % 25==0:
                        j+=26;
                try:
                    j=int(self.getValue(self.outputNumber))
                except:
                    j=7
                for i in SG:
                    s[2] += "put(h_xout,{0},TTG{1}); \n".format(str(j),i)
                    j += 1
                    s[2] += "put(h_xout,{0},TTR{1}); \n".format(str(j),i)
                    j += 1

                s[3]= "/* \n"
                for i in SG:
                    s[3] += "D(\"_TTG_{0},0,1,XIO.BMO/127\"); \n".format(i)
                    s[3] += "D(\"_TTR_{0},0,1,XIO.BMO/127\"); \n".format(i)
                s[3] += "*/"

                f.write("\n".join(s))
                webbrowser.open("counters.txt")

    def error_message(self):
        """Error message when no XP.CNF is found"""
        messagebox.showerror("Open file", "Cannot open XP.CNF")

    def start(self):
        """GUI for this program"""
        root=tk.Tk()
        root.title("Counters generator")
        sb_label=Label(root,text="First output number")
        sb_label.grid(row=0, column=0)
        sb_default_val = StringVar()
        sb_default_val.set("7")
        self.outputNumber=Spinbox(root,from_=0, to=100,width=5, textvariable=sb_default_val)
        self.outputNumber.grid(row=0, column=1, sticky=W)
        browse_btn=tk.Button(text="Browse",command = lambda: self.chooseDirectory(), width=25,height=2)
        browse_btn.grid(row=1, column=0)
        self.dir_path_label_var=StringVar()
        self.dir_path_label_var.set("Choose directory")
        dir_path_label=Label(root, textvariable=self.dir_path_label_var, width=70, anchor=W, justify=LEFT)
        dir_path_label.grid(row=1, column=1, sticky=W)
        generate_btn=tk.Button(root, text="Generate",command = lambda: self.generate(self.path), width=25,height=3,bg="light green")
        generate_btn.grid(row=3, columnspan=2)
        for child in root.winfo_children():
            child.grid(padx=5, pady=10)
        root.mainloop()


app = App()
app.start()
