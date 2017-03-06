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

       #name to show in menu   # name that binds an event
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
          ,["SpaceBar",         "<space>"]                     ] +\
           [[s.upper(), s]      for s in string.ascii_lowercase] +\
           [[i,i]               for i in string.digits         ] +\
           [["F%s"%i,"<F%s>"%i] for i in range(1,13)           ] +\
          [["<",                "<less>"]
          ,["-",                "<minus>"]                     ] +\
           [[o,o]               for o in string.punctuation if not o in "-<"]

_VALID_KEYS       = [a[1] for a in VALID_KEYS_LIBRARY]
_VALID_KEYS_NAMES = [a[0] for a in VALID_KEYS_LIBRARY]
_VALID_KEYS_NAMES_lower = list_lower(_VALID_KEYS_NAMES)

MODIFIERS =   [["Ctrl",                 "Control"]
              ,["Control",              "Control"]
              ,["Alt",                  "Alt"]
              ,["Shift",                "Shift"]
               ]

_MODIFIERS_KEYS  = [a[1] for a in MODIFIERS]
_MODIFIERS_NAMES = [a[0] for a in MODIFIERS]
_MODIFIERS_NAMES_lower = list_lower(_MODIFIERS_NAMES)


class Bind:
    """
    TODO
    """

    SPLITTERS = "+-"
    QUOTATIONS = "\'\""
    def __init__(self, text, function, keepformat=False, master = None):       

        if self._assert_function(function):
            raise self._assert_function(function)
        self.function = function        
        
        if not isinstance(text,str):
            error_message = "Argument 'text' should be string, but found type "%type(text)
            return TypeError(error_message)
        
        self.text = text

        for split_char in self.SPLITTERS:
            list_keys =  self._are_there_any_quotes(text)
            if not list_keys:
                list_keys = text.split(split_char)
                
            if len(list_keys)>1 and list_keys[-1]:
                #checks for errors
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

        if self._assert_output(self.output):
            raise self._assert_output(self.output)

        self.output_dict = {"accelerator":self.text_formatted,
                            "command":    self.function}
        if keepformat:
            if isinstance(keepformat,str):
                self.output_dict["accelerator"] = keepformat
            else:
                self.output_dict["accelerator"] = self.text

        if master:
            self.bind(master)




    def _form_output_without_modifier(self,text):
        key_index =  _VALID_KEYS_NAMES_lower.index( text.lower() )
        output = _VALID_KEYS[key_index]
        text_formatted = _VALID_KEYS_NAMES[key_index]

        return output, text_formatted
    
    def _form_output_with_modifier(self,list_keys):
        modifiers_indices = [_MODIFIERS_NAMES_lower.index(a.lower()) for a in list_keys[0:-1]]
        key_index         =  _VALID_KEYS_NAMES_lower.index( list_keys[-1].lower() )

        modifier_keys = [_MODIFIERS_KEYS[i] for i in modifiers_indices]

        last_key_name = _VALID_KEYS[key_index]
        if last_key_name.startswith("<"):
            last_key_name = last_key_name[1:-1]

        # if the modifiers contain a shift, then
        # the last key must be capital if it is a letter
        if "Shift" in modifier_keys and len(last_key_name)==1:
            last_key_name = last_key_name.upper()
            
        output = "-".join(modifier_keys + [last_key_name])
        output = "<" + output + ">"
        text_formatted = "+".join([_MODIFIERS_NAMES[i] for i in modifiers_indices] + [_VALID_KEYS_NAMES[key_index]])
        
        return output, text_formatted


    def bind(self, master):
        """
        TODO
        """
        # can be bound to a button, apparently, and still work.
        # TODO got to test some more on which items it works, and on which not
##        if not isinstance(master,tk.Tk):
##            error_message = "TODO"
##            raise TypeError(error_message)
        self.master = master
        
        master.bind_all(self.output, self.function)
        return self.output_dict
        
        
        
    def _are_there_any_quotes(self,text):
        counter = [0]*len(self.QUOTATIONS)
        for i,q in enumerate(self.QUOTATIONS):
            for t in text:
                if t==q:
                    counter[i] += 1                    
        output = False
        text_copy = text
        for i,c in enumerate(counter):
            q = self.QUOTATIONS[i]
            if c>1 and c%2==0:
                parts = []
                assert int(c/2) == c/2
                for a in range(int(c/2)):
                    index1 = text_copy.index(q)
                    if a==0 and text_copy[:index1]:
                        parts.append((text_copy[:index1],))
                    text_copy = text_copy[index1+1:]
                    index2 = text_copy.index(q)
                    parts.append([text_copy[:index2]])
                    text_copy = text_copy[index2+1:]
                    if a==c/2-1 and text_copy[:index2]:
                        parts.append((text_copy[:index2],))

                output = []
                for p in parts:
                    if isinstance(p,list):
                        if self._assert_validity_key( p[0] ):
                            raise self._assert_validity_key( p[0] )
                        output += p
                    elif isinstance(p,tuple):
                        splitted = p
                        for spl in self.SPLITTERS[::-1]:
                            if spl in p[0]:
                                splitted = p[0].split(spl)
                        for s in splitted:
                            if s:
                                output.append(s)
        return output
                
                
                
                
    # TODO: make method help_on_format, with explanation
    def help_on_format(self, print_=True):
        output = """
        The first argument of Bind should be a string, that formats the
        shortcut. This format must contain a KEY; all acceptable keys are
        defined below. This KEY can be preceded by one or more MODIFIER.
        If so, that the MODIFIER(s) and KEY have to be connected by
        either a plus-sign (+) or minus-sign (-) (but be consequential).
        KEYs and MODIFIERs can be encapsulated within quotes*.        
        KEY and MODIFIER do not have to be case-sensitive.

        Examples:
        """
        output = output[1:]
        X,Y = 8,2
        output += Y*" "+"Ctrl+P   alt+'+'   shift-\"B\"   'ctrl'-ShiFt-Z\n\n"+X*" "
        
        
        output += "possible MODIFIER:\n%s%s"%((X+Y)*" ",(Y*" ").join(_MODIFIERS_NAMES))
        output += "\n"*2+X*" "+"possible KEY:"
        KEYS = _VALID_KEYS_NAMES.copy()
        while KEYS:
            line = "\n"+ X*" "
            while KEYS and len(line) + len(KEYS[0]) <72:
                line += Y*" " + KEYS[0]
                KEYS.remove(KEYS[0])
            output += line

        output += \
        """\n
        *quotes cannot math the KEY, i.e. if KEY is single quote, the
         quotes that encapsulate it must be double quotes."""
        if print_:
            print(output)
        else:
            return output
        
                
            



    def _assert_validity_key(self,key_text):
        if not key_text.lower() in _VALID_KEYS_NAMES_lower:
            error_message = "Input of key '%s' is not recognised. For help see method 'help_on_format'."%(key_text)
            return ValueError(error_message)

    def _assert_validity_modifier(self,list_modifiers):
        for modifier_text in list_modifiers:
            if not modifier_text.lower() in _MODIFIERS_NAMES_lower:
                if modifier_text.lower() in _VALID_KEYS_NAMES_lower:
                    error_message = "The part '%s' from text-input '%s' is supposed to be the modifier."%\
                                    (modifier_text, self.text)
                    return ValueError(error_message)
                else:
                    error_message = "The part '%s' from text-input '%s' was not recognised."%\
                                    (modifier_text, self.text)                
                    return ValueError(error_message)

    def _assert_output(self,output):
        if output.endswith("->>"):
            error_message = "The input '%s' is invalid, since no modifier can be combined with '>'."%self.text
            return ValueError(error_message)


    def _assert_function(self,function):
        """
        Checks the number of arguments that can be given to the function
        which is to be bound.
        """
        # This function will be given to menu as a command (which accepts no
        # arguments) and to method tk.Tk.bind_all (which gives 1 argument).
        # Function has to handle both situations.
        if not callable(function):
            error_message = "Expected a function/callable, but got type %s."%type(function)
            return TypeError(error_message)
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
            return ValueError(error_message)

        
            

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
    Bind("+",lambda*x:print("raas"), master = master).help_on_format()


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

    #### TEST ####
    import unittest
    from test.test_bind import Test_bind
    unittest.main()
