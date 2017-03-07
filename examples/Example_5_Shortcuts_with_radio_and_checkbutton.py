# need to import it from another folder; this block enables that
import sys, os, inspect
current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
parent_folder = os.path.split(current_folder)[0]
if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)
del sys, os, inspect, current_folder, parent_folder


##### EXAMPLE 5 #####
# Showcases a more elaborate example, in which radiobuttons and
# a checkbutton are used. Pressing the shortcut will change which
# animal in the menu is "checked". Additionally, whenever a New
# animal has been selected* (i.e., the "check" changes), the animal
# will be printed. Secondly, the checkbutton from the options-menu
# controls whether the button is visible or not. This checkbutton
# can also be controlled with the shortcut Ctrl-K
#
# *either because the menu-item is clicked, or a shortcut has been
#  pressed.

import tkinter as tk
import datetime
from  tkmenu import Menu, SubMenu, ShortCut

master = tk.Tk()




### code to support the radiobutton(s) ###
def set_animal(animal):
    """Generates function that is able to set Animal to animal if called."""
    # I need to do it this way, because otherwise I need to specify three
    # different functions.
    def foo(*event):
        # If a shortcut is called, 1 argument will be given.
        # If the menu-item is pressed, no argument will be given
        if event:
            Animal.set(animal)
    return foo

def animal_text():
    output = "Your animal is a '%s'.\nPress a shortcut (see animal-menu)\nto change your animal."%Animal.get()
    return output

Animal_label = tk.Label(master, width=50)
Animal_label.pack()

Animal = tk.StringVar()
Animal.trace("w",lambda*x:Animal_label.config(text=animal_text()))
Animal.set("Cat")





### code to support the Checkbutton ###
Useless_Button = tk.Button(master,text = "delete button\nor use shortcut Ctrl+K\n(see options menu)", command=lambda*x:toggle_useless_button(True))
def show_or_delete_useless_button(*x):
    if Useless_Button_var.get():
        Useless_Button.pack(padx=50,pady=20)
    else:
        Useless_Button.pack_forget()
        
Useless_Button_var = tk.IntVar()
Useless_Button_var.trace("w", show_or_delete_useless_button)
Useless_Button_var.set(1)

def toggle_useless_button(*event):
    """
    Shows or deletes the useless button, depending
    on the checkbutton in options menu.
    """
    if event:        
        x = abs(Useless_Button_var.get() - 1)
        Useless_Button_var.set(x)
        




filemenu = [["file"]
            ,["quit", master.destroy]
            ]

animal_menu = ["choose an animal"
               ,["Cat", {"type":"radiobutton", "variable":Animal, "value":"Cat"}, ShortCut("Ctrl+I", set_animal("Cat"))]
               ,["Dog", {"type":"radiobutton", "variable":Animal, "value":"Dog"}, ShortCut("Ctrl+O", set_animal("Dog"))]
               ,["Pig", {"type":"radiobutton", "variable":Animal, "value":"Pig"}, ShortCut("Ctrl+P", set_animal("Pig"))]
            ]

option_menu = ["options"
                 ,["show useless button",{"type":"checkbutton", "variable":Useless_Button_var},ShortCut("Ctrl+K", toggle_useless_button)]
               ]

# Final menu-creation
A = Menu(master, filemenu,  animal_menu, option_menu)



master.wm_title("Example 5")
master.mainloop()
