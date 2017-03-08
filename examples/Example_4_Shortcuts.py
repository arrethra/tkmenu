# need to import it from another folder; this block enables that
import sys, os, inspect
current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
parent_folder = os.path.split(current_folder)[0]
if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)
del sys, os, inspect, current_folder, parent_folder

import tkinter as tk
from tkmenu import Menu, SubMenu, ShortCut


###### EXAMPLE ######
master = tk.Tk()

def SaveFile(*x):
    print("saved a file")
def Undo(*x):
    print("undo action")
def PrintFile(*x):
    print("print file")

filemenu = ["file"
               ,["save",  ShortCut("Ctrl+S", SaveFile )]
               ,["print", ShortCut("ctrl-p", PrintFile)]
               ,["___"]
               ,["quit", master.destroy]
           ]

editmenu = ["edit"
               ,["undo",  ShortCut("Ctrl+Z", Undo)]
           ]
            
A = Menu(master, filemenu, editmenu)

master.wm_title("Example 'Shortcuts'")
master.mainloop()



