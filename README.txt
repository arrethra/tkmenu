## Creates a menu in tkinter, while enabling the user to have a clear
## overview of the structure of the (intended) menu. Submenus can be
## created through the class SubMenu from this module. See Example 1
## (see below) for a demonstration on its application.

## tkmenu also allows easy updating/generation of submenus when they
## are required to change, even during runtime of the script/program.
## An example is shown in Example 3 (from map examples), where the 
## submenu 'recent files' can change according to history of file use.         
 

###### EXAMPLE 1 ######

import tkinter as tk
from tkmenu import Menu, SubMenu

master = tk.Tk()

filemenu = ["file"                   
            ,["save",lambda:print("save")]             
            ,"---"                                       
            ,SubMenu(["milkproducts"                 
                      ,["whey",lambda:print("whey")]
                      ,SubMenu(["cheese"   
                               ,["20%", lambda:print("cheese 20%")]
                               ,["40%", lambda:print("cheese 40%")]
                              ])
                      ,["yogurt", lambda:print("yogurt")]
                     ])                            
            ,"---"
            ,["quit", master.destroy, {"foreground":"red"}]
           ]                    

editmenu = [["edit",{"tearoff":1}]
            ,["copy",lambda:print("copy")]
           ]

menubar = Menu(master, filemenu, editmenu)   
master.mainloop()


## written in Python 3.5.2