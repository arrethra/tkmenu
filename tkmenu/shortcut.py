import tkinter as tk
import string
import inspect

def list_lower(lst):
    """Applies str.lower to strings in the list (not recursively) """
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


class ShortCut:
    """
    This class is designed to make it easy to create shortcuts from
    menu-items. Preferably used in harmony with Menu. When used in Menu,
    just add it to the list of that menu-item; for an example, see
    example 4 in the relevant folder.

    Arguments:
    -text:        The string that defines the shortcut. The format for
                  this argument has some requirements. Call the
                  method help_on_format for more information. 
    -function:    Function that is to be performed when the shortcut is
                  called. The function has to be able to accept both
                  0 arguments or 1 argument.
    -keepformat:  text might be reformatted when format is added to
                  menu-item. Setting keepformat to True keeps the
                  format from text. Setting keepformat to a string,
                  will supersede the format from text.
    -master:      In order to bind the shortcuts to the function,
                  this class needs a master. If no master is supplied
                  initially, the shortcut still needs to be 'bound'
                  with the method bind (which requires a master)
                  When using this class in harmony with Menu, it takes
                  the master from Menu.
    -add:         If set to True, it enables multiple function to be
                  added to this specific shortcut. Adding another
                  function to the shortcut is enabled by using ShortCut
                  or method tk.Tk.bind_all again (with keyword add=True)

    Atttributes:
    -output_dict: A dictionary that can be accepted by a tk.Menu method
                  such as add_command. Dictionary specifies the
                  keyword-arguments "accelerator" and "command"
    -output:      event-binder for the keystrokes, that can be accepted
                  into method tk.Tk.bind_all.
    -master:      contains the master
    -text_formatted:
                  Text/format that will be displayed in the menu.
                  
    """

    SPLITTERS = "+-"
    QUOTATIONS = "\'\""
    def __init__(self, text, function, keepformat=False, master = None, add=None):       
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
            self.bind(master, add)




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


    def bind(self, master=None, add=None):
        """
        Binds the shortcut to the function. If no master is specified
        during initalization, this method needs to be called manually.
        """        
        if master:
            self.master = master
        else:
            try:
                master = self.master
            except AttributeError:
                pass
        if master == None:
            error_message = "No master has been specified, and this class "+\
                            "does not have a master as an attribute "+\
                            "(from previous uses)."
            raise TypeError(error_message) 
        
        master.bind_all(self.output, self.function, add=None)
        return self.output_dict
    

    def unbind(self):
        """
        Unbinds the function from the shortcut.
        """
        self.master.unbind_all(self.output)
        
        
    def _are_there_any_quotes(self,text):
        """
        Searches for KEYs or MODIFIERS to be encapsulated in brackets.
        If so, it returns the modifiers and keys broken down as a list,
        else return False.
        """
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
                
                
                
                
    def help_on_format(self, print_=True):
        """
        Prints 'help' on how to properly format the argument 'text'.
        This method also returns this help-text. To prevent printing,
        specifiy argument 'print_' to be False.
        """
        output = """
        The first argument of ShortCut should be a string, that formats the
        shortcut. This format must contain a KEY; all acceptable keys are
        defined below. This KEY can be preceded by one or more MODIFIER.
        If so, that the MODIFIER(s) and KEY have to be connected by
        either a plus-sign (+) or minus-sign (-) (but be consistant).
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
        """
        Some (combinations of) modifiers and/or keys will result in
        obscure errors. This method catches those cases.
        """
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
    #### TEST ####
    import unittest
    from test.test_shortcut import Test_Shortcut
    unittest.main()
