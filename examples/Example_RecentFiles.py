# need to import it from another folder; this block enables that
import sys, os, inspect
current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
parent_folder = os.path.split(current_folder)[0]
if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)
del sys, os, inspect, current_folder, parent_folder

import tkinter as tk
from tkmenu import Menu, SubMenu

## This is an example of how a list of varying length can still
## be used to create menu-items. This example uses the varying
## list of "recently used files"

RecentFiles = ["file 3",
               "file2",
               "file 1"
               ]

RecentFileNumber = 4
# mundane functions with respect to handling Recent Files
def OpenNewFile():
    max_files = 8
    global RecentFileNumber
    global RecentFiles
    RecentFiles = ["file %s"%RecentFileNumber] + RecentFiles
    if len(RecentFiles)>max_files:
        RecentFiles = RecentFiles[0:max_files]
    print("You just 'opened' %s."%RecentFiles[0],
          "You can now see that this file has been ",
          "\nadded to the submenu 'recent files' under 'file'.\n")
    RecentFileNumber += 1

def ClearRecentFiles():
    global RecentFiles
    RecentFiles = []

def RecentFilesMenu():
    def substitute(txt):
        def bar():
            print("substitute function for opening '%s'."%txt)
        return bar
    output = ["recent files"] +\
               [[a,substitute(a)] for a in RecentFiles ] +\
               [["___"]
               ,["clear history",ClearRecentFiles]]
    return output

master = tk.Tk()


# where the magic happens (updates the menu everytime it is called upon)
filemenu = [["file",    {"postcommand":
                             lambda:A.reconfigure_submenu( RecentFilesMenu() )}]
               ,SubMenu(RecentFilesMenu())
               ,["___"]
               ,["quit",master.destroy]
            ]
            
A = Menu(master, filemenu)

OpenNewFile_Button = tk.Button(master,
                               text="'open' new\nimaginary file",
                               command = OpenNewFile)
OpenNewFile_Button.pack(padx=100,pady=30)

master.wm_title("Example 'Recent Files'")
master.mainloop()



