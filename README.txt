## Creates a menu in tkinter, while enabling the user to have a clear
## overview of the structure of the (intended) menu. Submenus can be
## created through the class SubMenu from this module. See Example 1
## (see below) for a demonstration on its application.

## tkmenu also allows easy updating/generation of submenus when they
## are required to change, even during runtime of the script/program.
## An example is shown in Example 3 (from map examples), where the 
## submenu 'recent files' can change according to history of file use.         

# TODO: add explanation of all methods (gather docstring and put it) in a document/tutorial-thingy.. 

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


## Requirements of structure of menu_lists:
## - Each separate dropdown-menu is added as a separate argument when 
##       initiating this class.
## - Each 'main-menu' is a list/iterable, containing its menu-items.
##       These menu items are encapsulated in a list, or within a
##       SubMenu which creates an expandable/foldable menu-item.
##   - Title/label must be first element of the list, either it be
##         the label of the menu or the label of a simple menu-item.
##         This can be a string or a string encapsulated within a list.
##   - Extra options for menu(-items) are added as a dictionary, in
##         which the keys are the option-keywords in string-form.
##         For options that govern entire (sub)menu's, the dictionary
##         is added to the first element (which must now be a list).
##         For menu-items, this dictionary is added to their
##         encapsulating list. Possible options can be found at
##         http://effbot.org/tkinterbook/menu.htm
##           Note that this class accepts "type" as a keyword for an
##           option, which can have the values "command"(default),
##           "radiobutton" or "checkbutton". See methods
##           add_radiobutton and add_checkbutton for their specific
##           implications.
##    - A separator can be added between menu-items, and is indicated
##         with a string that starts with either "___" or "---".
##    - The function that is coupled to a menu-item (its 'command')
##         can be added plainly to the encapsulating list. Reminder:
##         This function should not have been called yet.

## written in Python 3.5.2