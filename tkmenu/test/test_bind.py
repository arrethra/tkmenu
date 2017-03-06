import unittest
import os
import inspect
import tkinter as tk


TIME = 1
KEEP_WINDOW = False
##KEEP_WINDOW = True

try:
    from tkmenu.bind import Bind, _VALID_KEY_NAMES, _MODIFIERS_NAMES
except:
    # This garbage just so to import 'tkmenu', if it can't be done via the main way.
    import sys
    current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
    parent_folder = os.path.split(current_folder)[0]
    grandparent_folder = os.path.split(parent_folder)[0]
    if grandparent_folder not in sys.path:
        sys.path.insert(0, grandparent_folder)
    del sys
    del current_folder, parent_folder, grandparent_folder
    from tkmenu.bind import Bind, _VALID_KEYS_NAMES, _MODIFIERS_NAMES


def stupid_function(*x):
    print("stupid_function printed this text")


def foo(key):
    def bar(*args):
        print("Evidently, the key '%s' was bound."%key)
    return bar


def bind_all_single_keys(self,function="foo"):
    single_keys = _VALID_KEYS_NAMES
    #just to throw some variable upper/lower in there
    single_keys[4] = single_keys[4].upper()
    single_keys[5] = single_keys[5].lower()

    for key in single_keys:
        if function == "foo":
            function_copy = foo(key)
        else:
            function_copy = function
        try:
            A = Bind(key, function_copy)
            A.bind(self.master)
        except:
            print("error occured at key:", key)
            raise
    

def bind_all_combo_keys(self, function = "foo"):
    for mod1 in _MODIFIERS_NAMES:
        for single_key in _VALID_KEYS_NAMES:
            
            if single_key == "+":
                single_key = "'+'"
            elif single_key in ">":
                continue

            for mod2 in _MODIFIERS_NAMES + [""]:
                
                    if mod2:
                        if mod1[0] != mod2[0]:
                            combo = "+".join([mod1,mod2,single_key])
                        else: continue
                    else:
                        combo = "+".join([mod1,single_key])
                    if function == "foo":
                        function_copy = foo(combo)
                    else:
                        function_copy = function
                    try:                        
                        A = Bind(combo, function_copy )            
                        A.bind(self.master)
                    except:
                        print("error occured at combo:",combo)
                        raise



class Test_bind(unittest.TestCase):

    def setUp(self):
        self.master = tk.Tk()
        if not KEEP_WINDOW:
            self.master.after(1000*TIME, self.master.destroy)
        title = self.id().split(".")[-1]
        self.master.wm_title(title)

    def test_bind_by_binding_all_keys(self):
        # just checks if running the function gives any errors.
        # does not check if the result actually works.

        
        Bind("Ctrl+'P'",stupid_function).bind(self.master) #test if it accepts quotes around the key
        Bind("Ctrl-'-'",stupid_function).bind(self.master)
        bind_all_single_keys(self)
        bind_all_combo_keys(self)
        Bind("'",       stupid_function).bind(self.master)
        

    def test_exceptions(self):        
        with self.assertRaises(ValueError):
            # function should be capable to accept both 0 and 1 argument
            A = Bind("Ctrl",lambda x,y:print("something"))
            A.bind(self.master)
        with self.assertRaises(TypeError):
            A = Bind(">",2) # must be a function, not anything else
            A.bind(self.master)
        
            

    

    
    def tearDown(self):
        if not KEEP_WINDOW:
            try:    self.master.destroy()
            except: pass

            try:    del self.master
            except: pass

       

       



def run_test_tkmenu():
        unittest.main()

if __name__ == '__main__':
    run_test_tkmenu()
    
