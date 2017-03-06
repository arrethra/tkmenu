import tkinter as tk
import string
import inspect

def list_lower(lst):
    lst_output = []
    for item in lst:
        if isinstance(item, str):
            lst_output.append(item.lower())
        else:
            lst_output.append(item)
    return lst_output


VALID_KEYS_LIBRARY = \
          [["Ctrl",             "<Control_L>"]
          ,["Control",          "<Control_L>"]
          ,["Alt",              "<Alt_L>"]
          ,["Shift",            "<Shift_L>"]   
          ,["Enter",            "<Return>"]
          ,["Return",           "<Return>"]
          ,["Left",             "<Left>"]
          ,["Right",            "<Right>"]
          ,["Up",               "<Up>"]
          ,["Down",             "<Down>"]
          ,["PageUp",           "<Prior>"]
          ,["PageDown",         "<Next>"]
          ,["Backspace",        "<BackSpace>"]
          ,["Delete",           "<Delete>"]
          ,["End",              "<End>"]
          ,["Esc",              "<Escape>"] 
          ,["Escape",           "<Escape>"]
          ,["Home",             "<Home>"]
          ,["Insert",           "<Insert>"]           
          ,["Ins",              "<Insert>"]
          ,["Print",            "<Print>"]
          ,["Tab",              "<Tab>" ]
          ,["CapsLock",         "<Caps_Lock>"]
          ,["NumLock",          "<Num_Lock>"]
          ,["ScrollLock",       "<Scroll_Lock>"]
          ,["Break",            "Cancel"]                    
          ,["SpaceBar",         "<space>"]
          ,["<",                "<less>"]
          ,["-",                "<minus>"]                     ] +\
           [["F%s"%i,"<F%s>"%i] for i in range(1,13)           ] +\
           [[s.upper(), s]      for s in string.ascii_lowercase] +\
           [[i,i]               for i in string.digits         ] +\
           [[o,o]               for o in string.punctuation if not o in "-<'\""]

_VALID_KEYS       = [a[1] for a in VALID_KEYS_LIBRARY]
_VALID_KEYS_NAMES = [a[0] for a in VALID_KEYS_LIBRARY]
_VALID_KEYS_NAMES_lower = list_lower(_VALID_KEYS_NAMES)

MODIFIERS =   [["Ctrl",                 "Control"]
              ,["Control",              "Control"]
              ,["Alt",                  "Alt"]
              ,["Shift",                "Shift"]
               ]

MODIFIERS_KEYS  = [a[1] for a in MODIFIERS]
MODIFIERS_NAMES = [a[0] for a in MODIFIERS]
MODIFIERS_NAMES_lower = list_lower(MODIFIERS_NAMES)




class Bind:
    """
    TODO
    """



    





    
    SPLITTERS = "+-"
    def __init__(self, text, function, keepformat=False, master = None):       

        if self._assert_function(function):
            raise self._assert_function(function)
        self.function = function        
        
        if not isinstance(text,str):
            error_message = "Argument 'text' should be string, but found type "%type(text)
            return TypeError(error_message)
        
        self.text = text
        
        
        for split_char in self.SPLITTERS:
            list_keys = text.split(split_char)
                
            if len(list_keys)>1 and list_keys[-1]:
                #check for errors
                if self._assert_validity_key(list_keys[-1]):
                    raise self._assert_validity_key(list_keys[-1])
                if self._assert_validity_modifier(list_keys[0:-1]):
                    raise self._assert_validity_modifier(list_keys[0:-1])
                
                self.output, self.text_formatted = self._form_output_with_modifier(list_keys)
                
                break
        else:
            if self._assert_validity_key( text ):
                raise self._assert_validity_key( text )

            self.output, self.text_formatted = self._form_output_without_modifier(text)

        self.output_dict = {"accelerator":self.text_formatted,
                            "command":    self.function}
        if keepformat:
            self.output_dict["accelerator"] = self.text

        if master:
            self.master = master
            self.bind(master)




    def _form_output_without_modifier(self,text):
        key_index =  _VALID_KEYS_NAMES_lower.index( text.lower() )
        output = _VALID_KEYS[key_index]
        text_formatted = _VALID_KEYS_NAMES[key_index]

        return output, text_formatted
    
    def _form_output_with_modifier(self,list_keys):
        modifiers_indices = [MODIFIERS_NAMES_lower.index(a.lower()) for a in list_keys[0:-1]]
        key_index         =  _VALID_KEYS_NAMES_lower.index( list_keys[-1].lower() )

        modifier_keys = [MODIFIERS_KEYS[i] for i in modifiers_indices]

        last_key_name = _VALID_KEYS[key_index]
        if last_key_name.startswith("<"):
            last_key_name = last_key_name[1:-1]

        # if the modifiers contain a shift, then
        # the last key must be capital if it is a letter
        if "Shift" in modifier_keys and len(last_key_name)==1:
            last_key_name = last_key_name.upper()
            
        output = "-".join(modifier_keys + [last_key_name])
        output = "<" + output + ">"
        text_formatted = "+".join([MODIFIERS_NAMES[i] for i in modifiers_indices] + [_VALID_KEYS_NAMES[key_index]])
        
        return output, text_formatted


    def bind(self, master):
        """
        TODO
        """
##        if not isinstance(master,tk.Tk):
##            error_message = "TODO"
##            raise TypeError(error_message)
        self.master = master
        
        master.bind_all(self.output, self.function)
        return self.output_dict
        
        
        



    def _assert_validity_key(self,key_text):
        if not key_text.lower() in _VALID_KEYS_NAMES_lower:
            error_message = "Input of key '%s' is not recognised"%(key_text)
            return ValueError(error_message)

    def _assert_validity_modifier(self,list_modifiers):
        for modifier_text in list_modifiers:
            if not modifier_text.lower() in MODIFIERS_NAMES_lower:
                if modifier_text.lower() in _VALID_KEYS_NAMES_lower:
                    error_message = "The part '%s' from text-input '%s' is supposed to be the modifier."%\
                                    (modifier_text, self.text)
                    return ValueError(error_message)
                else:
                    error_message = "The part '%s' from text-input '%s' was not recognised."%\
                                    (modifier_text, self.text)                
                    return ValueError(error_message)


    def _assert_function(self,function):
        """
        Checks the number of arguments that can be given to the function
        which is to be bound.
        """
        # This function will be given to menu as a command (which accepts no
        # arguments) and to method tk.Tk.bind_all (which gives 1 argument).
        # Function has to handle both situations.
        nr_of_args_given = [0,1]

        lower, upper = args_taken_by(function)
        
        if not (lower <= nr_of_args_given[0] and nr_of_args_given[1] <= upper):
            if lower == upper:
                error_message = str(function) + " takes %s argument(s), while it has to accept between %s and %s number of arguments"%\
                                (lower, nr_of_args_given[0], nr_of_args_given[1])
            else:
                error_message = str(function) + " takes between %s and %s argument(s), while it has to accept between %s and %s number of arguments."%\
                                (lower, upper, nr_of_args_given[0], nr_of_args_given[1])
            error_message += " (Suggestion; use the code lambda*x:foo(..) )"
            return TypeError(error_message)
            

def args_taken_by(function):
    """
    Calculates number of arguments that can be taken by input. Returns
    tuple with minimum and maximum (maximum can be float("inf")).
    """
    if not callable(function):
        error_message = "Input must be callable, but found type %s"%type(function)
        raise TypeError(error_message)
    
    arguments = inspect.signature(function)
    Par = arguments.parameters
    parameters = [Par[key] for key in Par]
    
    nr_of_req_args = 0
    nr_of_pot_args = 0

    for X in parameters:
        x = str( X.kind)
        if x == 'POSITIONAL_ONLY':
            nr_of_req_args += 1
        elif x == 'POSITIONAL_OR_KEYWORD':
            if type(X.default) == type(inspect._empty):
                nr_of_req_args += 1
            else:
                nr_of_pot_args += 1
        elif x == 'VAR_POSITIONAL':
            nr_of_pot_args = float("inf")
        elif x == 'KEYWORD_ONLY':
            nr_of_pot_args += 1
            
    return (nr_of_req_args, nr_of_req_args+nr_of_pot_args)

            
            
        
        
        
        
        
               
               
               
        
    

if __name__ == "__main__":

    master = tk.Tk()

    master.after(1000,master.destroy)

    # TODO: write unittest
    
    Bind("p",      lambda*x,y=1:print("kaas")).bind(master)
    Bind("Ctrl-P", lambda *y, z=1, **kwargs:print("vaas")).bind(master)
    Bind("Ctrl-Shift-P", lambda y=1,z=1:print("maas")).bind(master)
    Bind("shift-p",lambda*x:print("haas"), master = master)
    Bind("+",lambda*x:print("raas"), master = master)

    def foo(key):
        def bar(*args):
            print(key)
        return key, bar
    
    for key in _VALID_KEYS:
        try:
            master.bind_all( *foo(key)  )
        except:
            print("error occurred with",key)
            raise
    
    master.bind_all("<Control-Tab>",lambda*x:print("ctrl-tab"))
    master.bind_all("<Shift-Control-Tab>",lambda*x:print("ctrl-shft-tab"))
##    master.mainloop()
    master.destroy()
