# need to import from another folder; this block enables that
import sys, os, inspect
current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
parent_folder = os.path.split(current_folder)[0]
if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)
del sys, os, inspect, current_folder, parent_folder

########## EXAMPLE 1 #######
# Example from docstring of Menu (i.e., see [help(Menu)])
# to show the structure of the code, and the overview that has been gained.
from tkmenu import Menu, SubMenu
import tkinter as tk    
master = tk.Tk()

filemenu = ["file"                   
            ,["save", lambda:print("save")]             
            ,"---"                                       
            ,SubMenu(["milkproducts"                 
                      ,["whey", lambda:print("whey")]
                      ,SubMenu(["cheese"   
                               ,["20%", lambda:print("cheese 20%")]
                               ,["40%", lambda:print("cheese 40%")]
                              ])
                      ,["yogurt", lambda:print("yogurt")]
                     ])                            
            ,"---"
            ,["quit", master.destroy, {"foreground":"red"}]
           ]                    

editmenu = [["edit", {"tearoff":1}]
            ,["copy", lambda:print("copy")]
           ]

menubar = Menu(master,filemenu,editmenu)   
master.mainloop()
