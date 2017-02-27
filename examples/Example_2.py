# need to import it from another folder; this block enables that
import sys, os, inspect
current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
parent_folder = os.path.split(current_folder)[0]
if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)
del sys, os, inspect, current_folder, parent_folder


##### EXAMPLE 2 #####
# Showcases a more elaborate example, in which radiobuttons have been added
# (see menu "one choice only") or which updates itself whenever the menu
# opens (see menu "get current time")

import tkinter as tk
import datetime
from  tkmenu import Menu, SubMenu

master = tk.Tk()

## Whenever the menu 'get current time' opens, this functions is called to
## update the menu(/time), thereby showing the current time as a menu-item.
## This behavior is enabled by passing the keyword 'postcommand' to that
## (sub)menu (see the menu-structure below).
def update_clock():
    time_string = str(datetime.datetime.now().time()).split(".")[0]
    A.get_handle("get current time").entryconfig(0,label=time_string)

# Needed for the radiobutton
Pet = tk.StringVar()
Pet.set("cat")

# The structure/overview for creating the menu.

filemenu = [["file"]
            ,["save", lambda:print("save")]
            ,"---"
            ,SubMenu(["vegetables"
                       ,["lettuce",     lambda:print("lettuce")]
                       ,["cauliflower", lambda:print("cauliflower")]
                     ])
            ,"___"
            ,["quit", master.destroy]
            ]

clockmenu= [["get current time", {"postcommand":update_clock} ] 
            ,["displays current time"]
            ]

one_choice_only = \
           ["one choice only"
            ,["cat", {"type":"radiobutton", "variable":Pet, "value":"cat"}]
            ,["dog", {"type":"radiobutton", "variable":Pet, "value":"dog"}]
            ]

# Final menu-creation
A = Menu(master, filemenu, clockmenu, one_choice_only)
master.wm_title("Example 2")
master.mainloop()
