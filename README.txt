Creates a menu in tkinter, while enabling the user to have a clear
overview of the structure of the (intended) menu. Submenus can be
created through the class SubMenu from this module. See the example
below on its application.
        

Example:

import tkinter as tk    
master = tk.Tk()

filemenu = ["file"                   
            ,["save",lambda:print("save")]             
            ,"---"                                       
            ,SubMenu(["milkproducts"                 
                      ,["whey",lambda:print("whey")]
                      ,SubMenu(["cheese"   
                               ,["20%",lambda:print("cheese 20%")]
                               ,["40%",lambda:print("cheese 40%")]
                              ])
                      ,["yogurt",lambda:print("yogurt")]
                     ])                            
            ,"---"
            ,["quit",master.destroy,{"foreground":"red"}]
           ]                    

editmenu = [["edit",{"tearoff":1}]
            ,["copy",lambda:print("copy")]
           ]

menubar = Menu(master,filemenu,editmenu)   
master.mainloop()
