"""
When creating a menu in tkinter, the code might make a clear overview
somewhat 'cloudy'. With the help of this module, that code gets cleaned
up and enables a much clearer overview of the structure of the
'menu-to-be'.  For such an example, see main class Menu.

Author: Arrethra ( https://github.com/arrethra )
Created with help of Hans Maree ( https://github.com/snah )
"""

import tkinter as tk
import collections as col

# TODO: make function/class askokcancelcheckbox



def isiterable(var):
    """Returns whether input is iterable or not."""
    try:
        iter(var)
        return True
    except TypeError:
        return False
    


class Menu:
    """
    Creates a menu in tkinter, while enabling the user to have a clear
    overview of the structure of the (intended) menu. Submenus can be
    created through the class SubMenu from this module. See the example
    below on its application.

    Arguments:
    -Menu_lists are lists, in which the first item is a string for
     the title. This can be encapsulated within a list. Further items
     in the list are the separate options in that (sub)menu.


    Requirements of structure (or see example below):
    - Each separate 'main-menu' is added as an argument to this class.
    - Each 'main-menu' is a list/iterable, containing its menu-items.
          These menu items are encapsulated in a list, or within a
          SubMenu which creates an expandable/foldable menu-item.
      - Title/label must be first element of the list, either it be
            the label of the menu or the label of a simple menu-item.
            This can be a string or a string encapsulated within a list.
      - Extra options for menu(-items) are added as a dictionary, in
            which the keys are the option-keywords in string-form.
            For options that govern entire (sub)menu's, the dictionary
            is added to the first element (which must now be a list).
            For menu-items, this dictionary is added to their
            encapsulating list. Possible options can be found at
            http://effbot.org/tkinterbook/menu.htm
              Note that this class accepts "type" as a keyword for an
              option, which can have the values "command"(default),
              "radiobutton" or "checkbutton". See methods
              add_radiobutton and add_checkbutton for their specific
              implications.
       - A separator can be added between menu-items, and is indicated
            with a string that starts with either "___" or "---".
       - The function that is coupled to a menu-item (its 'command')
            can be added plainly to the encapsulating list. Reminder:
            This function should not have been called yet.
            
    
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
    """
    _POSSIBILITIES_TYPE = ("command","radiobutton","checkbutton")
    _handle_separator = ".__."

    
    def __init__(self, master, *menu_lists):
        self._menu_lists = menu_lists        
        self.initialize(master)


    def initialize(self, master):
        """
        Initializes this class further.
        -When defining the class Menu, this method is automatically
           called by __init__-method.
        -When defining the class SubMenu, this method needs to be
           called separately (which automaticaly happens if the class
           SubMenu is entered into Menu, as can be seen in the example
           of the Menu doc-string )

"""
        menu = tk.Menu(master)

        self._handles_dict = col.OrderedDict()
        submenu = []
        submenu_name = []
        submenu_dict = {}
        for menu_list in self._menu_lists:
                current_submenu_name = None
                 
                current_submenu, current_submenu_name = self._initiate_submenu(menu, menu_list[0])

                self._handles_dict[current_submenu_name] = current_submenu
                
                for menu_item in menu_list[1:]:                        
                        
                        if isinstance(menu_item,str):
                            self._add_separator(current_submenu, menu_item)
                            continue
                        elif isinstance(menu_item, SubMenu): 
                            menu_item.initialize(menu)
                            self._update_handles_dict_from_SubMenu( current_submenu_name, menu_item)

                            current_submenu.add_cascade( menu_item.submenu_dict ) 
                            
                        elif isiterable(menu_item) and not isinstance(menu_item,str):
                            text = menu_item[0] 
                            dict_with_keywords = self._get_keywords(menu_item)
                            
                            if self._identify_separator(text):
                                current_submenu.add_separator(dict_with_keywords)                            
                            else:
                                type_item = "command"
                                dict_with_keywords["label"] = text
                                if "type" in dict_with_keywords.keys():
                                    type_item = dict_with_keywords["type"]
                                    del dict_with_keywords["type"]
                                    if not type_item in self._POSSIBILITIES_TYPE:
                                        error_message = "The option 'type' was set to value '%s', while it can only be %s."%(type_item,self._POSSIBILITIES_TYPE)
                                        raise ValueError(error_message)
                                current_submenu.add(type_item, dict_with_keywords)
                        else:
                            error_message = "Expected a SubMenu, iterable or separator (str: '___'/'---'), but found type %s."%type(menu_item) 
                            raise TypeError(error_message)                            
                        
                
                dict_with_keywords = {"label": current_submenu_name, "menu": current_submenu}
                dict_with_keywords.update(submenu_dict)
                submenu_dict = {}
                if not isinstance(self, SubMenu):
                    menu.add_cascade(dict_with_keywords)
                submenu_name.append(current_submenu_name)
                submenu.append(current_submenu)
                
                    
        if isinstance(self, SubMenu):        
            self.submenu_dict.update({"label":submenu_name[0],"menu":submenu})
            try:
                del self.submenu_dict["tearoff"]
            except:
                pass
        else:
            tk.Tk.config(master,menu = menu)
            

    def _initiate_submenu(self, menu, menu_item):
        """
        Starts the creation of a submenu. It extracts the name of that
        submenu and creates the first instance of the submenu, to which
        later items will be added.
        """
        dict_with_keywords = {"tearoff":0}
        if isinstance(menu_item,str):
            current_submenu_name = menu_item
        elif isiterable(menu_item):
            current_submenu_name = menu_item[0]
            for elem in menu_item[1:]:
                if not isinstance(elem,dict):
                    error_message = "Expected dict with options for menu_item, but found type %s."%type(elem)
                    raise TypeError(error_message)
                dict_with_keywords.update(elem)

        if not isinstance(current_submenu_name,str):
            error_message = "Submenu name (first item in iterable) must be a string, but found type %s."%type(current_submenu_name)
            raise TypeError(error_message)
                
        current_submenu = tk.Menu(menu,dict_with_keywords)
        
        if isinstance(self, SubMenu):
            self.submenu_dict = dict_with_keywords.copy()

        return (current_submenu, current_submenu_name)


    def _add_separator(self, current_submenu, menu_item): 
        """Identifies and adds the separator to the (sub)menu."""
        if self._identify_separator(menu_item):
            current_submenu.add_separator()
        else:
            error_message = "Expected separator ('___'/'---'), but found '%s'. Otherwise it should be iterable or Submenu."%menu_item
            raise ValueError(error_message)

        
    def _identify_separator(self, text):
        """Identifies the separator."""
        return text.startswith("---") or text.startswith("___")


    def _get_keywords(self, menu_item):
        """
        Extracts the keywords from a given menu item.
        It also recognizes the function that is to be set as the
        command. This function can be added claiming to the list
        that makes up menu_item. 
        """
        dict_with_keywords = {}
        for elem in menu_item[1:]:
            if callable(elem):
                dict_with_keywords["command"] = elem
            elif isinstance(elem,dict):
                if not all(isinstance(a,str) for a in elem.keys()):
                    keys_of_wrong_type = [type(a) for a in elem.keys() if not isinstance(a,str)]
                    if len(keys_of_wrong_type) == 1:
                        error_message = "Dictionary contained a key that was not of type 'string', but of type '%s'."%keys_of_wrong_type[0]
                    else:
                        error_message = "Dictionary contained keys that were not of type 'string', but of types %s."%keys_of_wrong_type
                    raise TypeError(error_message)   
                dict_with_keywords.update(elem)
            else:
                error_message = "Expected function (command) or dict with options, but found type %s."%type(elem)
                raise ValueError(error_message)
        return dict_with_keywords

    def _update_handles_dict_from_SubMenu(self, current_submenu_name, Submenu):
        """TODO add doc """
        for old_key in Submenu._handles_dict.keys():
            new_key = current_submenu_name + self._handle_separator + old_key
            self._handles_dict[new_key] = Submenu._handles_dict[old_key]

    def get_handle(self,*path):
        """
        Get the handle of a submenu. The arguments *path are the full
        sequence of labels (of type string) leading to that specific
        submenu.
        E.g., in the example given in docstring of class Menu,
        the handle of submenu 'cheese' would be obtained by
        menubar.get_handle("file","milkproducts","cheese")
        """
        
        if not path:
            error_message = ""
            raise ValueError(error_message)
        
        _handles_dict_keys = self._handles_dict.keys()
        sep = self._handle_separator
        
        for i,path_partial in enumerate(path):
            if not isinstance(path_partial,str):
                error_message = "path must be string, but found type %s."%(type(path_partial))
                raise TypeError(error_message)
            
            full_path = sep.join(path[0:i+1])
            if not full_path in _handles_dict_keys: # Asses if built up path is correct so far.
                # If error, find out which keywords would have been correct in that position
                lesser_path = sep.join(full_path.split(sep)[:-1]) # path leading up to this current stage
                print(lesser_path)
                possible_keys = [a[len(lesser_path+sep):] for a in _handles_dict_keys if a.startswith(lesser_path+sep)] # must start with lesser_path, and also removes it
                possible_keys = [a for a in possible_keys if len(a.split(sep))==1 and a != ""] # remove any paths after base path
                
                if len(possible_keys):
                    error_message = "Argument #%s '%s' unrecognised. Correct argument at that place could have been '%s'."%(i+1,path_partial,"', '".join(possible_keys))
                else:
                    error_message = "Argument #%s '%s' unrecognised. There is no such path possible with that Argument."%(i+1,path_partial)
                
                raise ValueError(error_message)

            
        return self._handles_dict[full_path]
                
                
            
            
        

class SubMenu(Menu):
    """
    This class can make a single submenu, in conjunction with the class
    Menu. When initializing this class, the input is only stored. The
    method 'initialize' further initializes SubMenu. For more
    information see the class Menu from this module.

    Attributes:
    -menu_lists:      The input upon creating this class.
    -submenu_dict:    This attribute only exists once initialized by
                      method initialize. It holds a dictionary with
                      keywords for the method tk.Menu.add_cascade which
                      creates a submenu.
    """
    
    def __init__(self, menu_list):
        self._menu_lists = (menu_list,)
        

    




if __name__ == "__main__":
    ##### TEST
    master = tk.Tk()
    
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
                ,["quit",master.destroy]
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
    
    A = Menu(master, filemenu, editmenu, clockmenu, one_choice_only)
    
    


    master.mainloop()


    
