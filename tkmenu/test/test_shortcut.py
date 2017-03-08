import unittest
import os
import inspect
import tkinter as tk


TIME = 1
KEEP_WINDOW = False
##KEEP_WINDOW = True

try:
    from tkmenu.bind import ShortCut, _VALID_KEY_NAMES, _MODIFIERS_NAMES
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
    from tkmenu.shortcut import ShortCut, _VALID_KEYS_NAMES, _MODIFIERS_NAMES


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
            A = ShortCut(key, function_copy)
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
                        A = ShortCut(combo, function_copy )            
                        A.bind(self.master)
                    except:
                        print("error occured at combo:",combo)
                        raise



class Test_Shortcut(unittest.TestCase):

    def setUp(self):
        self.master = tk.Tk()
        if not KEEP_WINDOW:
            self.master.after(1000*TIME, self.master.destroy)
        title = self.id().split(".")[-1]
        self.master.wm_title(title)

    def test_bind_by_binding_all_keys(self):
        # just checks if running the function gives any errors.
        # does not check if the result actually works.

        
        ShortCut("Ctrl+'P'",stupid_function).bind(self.master) #test if it accepts quotes around the key
        ShortCut("Ctrl-'-'",stupid_function).bind(self.master)
        bind_all_single_keys(self)
        bind_all_combo_keys(self)
        ShortCut("'",       stupid_function).bind(self.master)
        

    def test_exceptions(self):        
        with self.assertRaises(ValueError):
            # function should be capable to accept both 0 and 1 argument
            A = ShortCut("Ctrl",lambda x,y:print("something"))
            A.bind(self.master)
        with self.assertRaises(TypeError):
            A = ShortCut(">",2) # must be a function, not anything else
            A.bind(self.master)

    def test_argument_keepformat(self):
        # if keepformat is not specified, input-text will be reformatted
        # into standard format for presentation on menu-item
        A = ShortCut("Ctrl+'P'",stupid_function)
        A.bind(self.master)
        self.assertTrue(A.output_dict["accelerator"] == "Ctrl+P")
        
        A = ShortCut("Ctrl-'P'",stupid_function)
        A.bind(self.master)
        self.assertTrue(A.output_dict["accelerator"] == "Ctrl+P")

        A = ShortCut("ctrl-p",stupid_function)
        A.bind(self.master)
        self.assertTrue(A.output_dict["accelerator"] == "Ctrl+P")
        
        # if keepformat is set to True, input-text will NOT be reformatted
        # into standard format for presentation on menu-item
        A = ShortCut("ctrl-p",stupid_function, keepformat=True)
        A.bind(self.master)
        self.assertTrue(A.output_dict["accelerator"] == "ctrl-p")

        # if keepformat is a string, it will supersede the input-text for
        # presentation on menu-item
        A = ShortCut("ctrl-p",stupid_function, keepformat="something else")
        A.bind(self.master)
        self.assertTrue(A.output_dict["accelerator"] == "something else")        


# TODO: test with simulating keydown to really test the shortcut...
    # test shortcuts / test unbind...
    # http://stackoverflow.com/questions/11906925/python-simulate-keydown
        
            

    

    
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
    
