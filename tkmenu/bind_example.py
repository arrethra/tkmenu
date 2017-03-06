import tkinter as tk
from bind import Bind
import bind 
               
               
        
    


master = tk.Tk()

##master.after(1000,master.destroy)

# TODO: write unittest

button = tk.Button(master,text = "click me")
button.pack()

Bind("p",      lambda*x,y=1:print("kaas")).bind(button)
Bind("Ctrl-P", lambda *y, z=1, **kwargs:print("vaas")).bind(button)
Bind("Ctrl-Shift-P", lambda y=1,z=1:print("maas")).bind(button)
Bind("shift-p",lambda*x:print("haas"), master = button)
Bind("+",lambda*x:print("raas"), master = button)

def foo(key):
    def bar(*args):
        print(key)
    return key, bar

for key in bind._VALID_KEYS:
    try:
        master.bind_all( *foo(key)  )
    except:
        print("error occurred with",key)
        raise

master.bind_all("<Control-Tab>",lambda*x:print("ctrl-tab"))
master.bind_all("<Shift-Control-Tab>",lambda*x:print("ctrl-shft-tab"))
master.mainloop()
##master.destroy()
