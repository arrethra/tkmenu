import unittest
import os
import inspect
import tkinter as tk


TIME = 1

try:
    from tkmenu import Menu, SubMenu
except:
    # This garbage just so to import 'tkmenu', if it can't be done via the main way.
    import sys
    current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
    parent_folder = os.path.split(current_folder)[0]
    grandpa_folder = os.path.split(parent_folder)[0]
    if grandpa_folder not in sys.path:
        sys.path.insert(0, grandpa_folder)
    del sys
    del current_folder, parent_folder, grandpa_folder
    from tkmenu import Menu, SubMenu

# TODO: now you're testing with static examples, but use an example with an automatic iterator... ?


def initialize_menu1(self):

    # standard example from docstring
    self.master = tk.Tk()
    
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
                ,["quit",self.master.destroy,{"foreground":"red"}]
               ]                    
    
    editmenu = [["edit",{"tearoff":1}]
                ,["copy",lambda:print("copy")]
               ]
    
    menubar = Menu(self.master, filemenu, editmenu)
    
    self.master.after(TIME*1000,self.master.destroy) # if test fails, the window will destroy itself anyway...
    
    return menubar


def assert_menu1(self):
    self.assertTrue(  self.menubar.get_handle("file").entrycget(0,'label')  == "save"  )

    self.assertTrue(self.menubar.get_handle("file").type(0) == "command")
    self.assertTrue(self.menubar.get_handle("file").type(1) == "separator"   )
    self.assertTrue(  self.menubar.get_handle("file").entrycget(2,'label')  == "milkproducts"  )

    self.assertTrue(self.menubar.get_handle("file").type(2) == "cascade")
    self.assertTrue(self.menubar.get_handle("file").entrycget(4,'label') == 'quit')
    self.assertTrue(str(self.menubar.get_handle("file").entrycget(4,'command')).endswith("destroy"))
    self.assertTrue(str(self.menubar.get_handle("file").entrycget(4,'foreground')) == 'red')


    self.assertTrue(self.menubar.get_handle("edit").type(0) == "tearoff")
    self.assertTrue(self.menubar.get_handle("edit").type(1) == "command")
    self.assertTrue(self.menubar.get_handle("edit").entrycget(1,'label')  == "copy"  )
            



    

def assert_submenu1(self):
    self.assertTrue(isinstance(self.menubar.get_handle(),tk.Menu))
    self.assertTrue(self.menubar.get_handle("file","milkproducts").entrycget(0,'label') == "whey")
    self.assertTrue(self.menubar.get_handle("file","milkproducts").entrycget(1,'label') == "cheese")
    self.assertTrue(self.menubar.get_handle("file","milkproducts").entrycget(2,'label') == "yogurt")
    
    self.assertTrue(self.menubar.get_handle("file","milkproducts","cheese").entrycget(0,'label') == "20%")
    self.assertTrue(self.menubar.get_handle("file","milkproducts","cheese").entrycget(1,'label') == "40%")
    
    
def initialize_menu2(self):
    self.master = tk.Tk()
    
    import datetime
    time_string = ""    
    def update_clock():
        global time_string
        time_string = str(datetime.datetime.now().time()).split(".")[0]
        try:
            A.get_handle("get current time").entryconfig(0,label=time_string)
        except: pass
    update_clock()

    radiobutton_var = tk.StringVar()
    radiobutton_var.set("cat")

    filemenu = [["file"]
                ,["save",lambda:print("save")]
                ,"---"
                ,SubMenu(["milkproducts"
                          ,["whey",  lambda:print("whey")]
                          ,SubMenu([["cheese",{"foreground":"red"}]
                                     ,["20%",lambda:print("cheese 20%")]
                                     ,["40%",lambda:print("cheese 40%")]
                                    ])
                           ,["yogurt",lambda:print("yogurt")]                                                             
                          ])
                ,SubMenu(["vegetables"
                          ,["lettuce",    lambda:print("lettuce")]
                          ,["cauliflower",lambda:print("cauliflower")]
                         ])
                ,["---"]
                ,["quit",self.master.destroy]
                ]
    
    editmenu = [["edit",{"tearoff":1}]
                ,["copy",lambda:print("copy")]
                ]
    
    clockmenu= [["get current time",{"postcommand":update_clock}]
                ,[time_string]
                ]

    one_choice_only = \
               [["one choice only"]
                ,["cat",{"type":"radiobutton", "variable":radiobutton_var, "value":"cat"}]
                ,["dog",{"type":"radiobutton", "variable":radiobutton_var, "value":"dog"}]
                ]    
    self.master.after(TIME*1000,self.master.destroy) # if test fails, the window will destroy itself anyway...
    
    menubar =  Menu(self.master, filemenu, editmenu, clockmenu, one_choice_only)

    return menubar


def assert_menu2(self):
    self.assertTrue(  self.menubar.get_handle("file").entrycget(0,'label')  == "save"  )

    self.assertTrue(self.menubar.get_handle("file").type(0) == "command")
    self.assertTrue(self.menubar.get_handle("file").type(1) == "separator"   )
    self.assertTrue(self.menubar.get_handle("file").entrycget(2,'label')  == "milkproducts"  )
    self.assertTrue(self.menubar.get_handle("file").type(2) == "cascade")

    self.assertTrue(self.menubar.get_handle("file").entrycget(3,'label')  == "vegetables"  )
    self.assertTrue(self.menubar.get_handle("file").type(3) == "cascade")   
    
    self.assertTrue(self.menubar.get_handle("file").entrycget(5,'label') == 'quit')
    self.assertTrue(str(self.menubar.get_handle("file").entrycget(5,'command')).endswith("destroy"))

    self.assertTrue(self.menubar.get_handle("edit").type(0) == "tearoff")
    self.assertTrue(self.menubar.get_handle("edit").type(1) == "command")
    self.assertTrue(self.menubar.get_handle("edit").entrycget(1,'label')  == "copy"  )

    
    self.assertTrue(self.menubar.get_handle("one choice only").type(0) == "radiobutton")
    self.assertTrue(self.menubar.get_handle("one choice only").type(1) == "radiobutton")

def assert_submenu2(self):
    assert_submenu1(self)      
    self.assertTrue(str(self.menubar.get_handle("file","milkproducts").entrycget(1,'foreground')) == "red")
    
    





class Test_tkmenu(unittest.TestCase):




    def test_initialize_menu1(self):
        self.menubar = initialize_menu1(self)
        
        assert_menu1(self)
        assert_submenu1(self)


    def test_initialize_menu2(self):
        self.menubar = initialize_menu2(self)
        
        assert_menu2(self)
        assert_submenu2(self)
        


    def test_get_handle(self):
        self.menubar = initialize_menu1(self)
        
        self.assertTrue(self.menubar.get_handle("file").entrycget(2,"menu")== (str(self.menubar.get_handle("file","milkproducts")),))
        self.assertTrue(self.menubar.get_handle("file","milkproducts").entrycget(1,"menu")== (str(self.menubar.get_handle("file","milkproducts","cheese")),))


    def tearDown(self):
        try:    self.master.destroy()
        except: pass

        try:    del self.master
        except: pass


  
        
       

       



def run_test_tkmenu():
        unittest.main()

if __name__ == '__main__':
    run_test_tkmenu()
