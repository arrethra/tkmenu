# need to import it from another folder; this block enables that
import sys, os, inspect
current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
parent_folder = os.path.split(current_folder)[0]
if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)
del sys, os, inspect, current_folder, parent_folder

import tkinter as tk
from tkmenu import Menu, SubMenu

###### EXAMPLE ######

## This example shows that a submenu can be varried during use.
## Whenever a file has been 'opened', the submenu 'recent files' changes
## accordingly.

## The memory in which the recent files are being stored.
RecentFiles = ["file 3",
               "file2",
               "file 1"
               ]

RecentFileNumber = 4
## Mundane functions with respect to handling opening
## The 'magic' happens after the next commented section.
def OpenNewFile():
    """Mimmicks the opening/creation of a NEW file. Adds the new file
    to the memory of recent files."""
    global RecentFileNumber
    global RecentFiles
    RecentFiles = ["file %s"%RecentFileNumber] + RecentFiles
    print( "'%s' has just been added to the 'recent files'-submenu.\n"\
             %RecentFiles[0] )    
    RecentFileNumber += 1

def ClearRecentFiles():
    """Clears the recent files."""
    global RecentFiles
    RecentFiles = []

def RecentFilesMenu():
    """Creates the required list structure for submenu 'recent files'.
    Incorporates any changes."""
    def OpenFile(txt):
        """Substitute function for opening a real file."""
        def openfile():
            print("Substitute function for opening '%s'."%txt)
        return openfile
    output = ["recent files"] +\
               [[a,OpenFile(a)] for a in RecentFiles ] +\
               [["___"]
               ,["clear history",ClearRecentFiles]]
    return output

master = tk.Tk()


## The keyword 'postcommand' enables the lambda-function to be carried out.
## This lambda function recreates the 'recent files' submenu, based on the
## latest changes to the 'recent files'-memory.

filemenu = [["file",    {"postcommand":
                             lambda:A.reconfigure_submenu( RecentFilesMenu() )}]
               ,["open new file",OpenNewFile]
               ,["___"]
               ,SubMenu(RecentFilesMenu())
               ,["___"]
               ,["quit",master.destroy]
            ]
            
A = Menu(master, filemenu)

## Button that enables a file to be 'opened'
OpenNewFile_Button = tk.Button(master,
                               text="'open' new\nimaginary file",
                               command = OpenNewFile)
OpenNewFile_Button.pack(padx=100,pady=30)

master.wm_title("Example 'Recent Files'")
master.mainloop()



