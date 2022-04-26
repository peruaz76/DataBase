# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:11:37 2022

@author: Peru _Alana
"""

import os
from tkinter import Tk
import pickle5 as pickle
from IPython import get_ipython
import tools.interface_add
import tools.class_database

##############################################################################
#                                PREAMBLE                                    #
##############################################################################

#Clean up

get_ipython().magic('reset -sf')
clear = lambda: os.system('cls')
clear()

##############################################################################
#                                MAIN PROGRAM                                #
##############################################################################

# Check if the data_base file exists
current_path = os.getcwd()
data_base_directory = current_path + '/data_base/data_base.pkl'

if os.path.exists(data_base_directory) is True:
    with open(data_base_directory, "rb") as pickle_file:
        data_base = pickle.load(pickle_file)
else:
    data_base = tools.class_database.Data_base()


# Main menu Interface
def main():
    '''Create window to the application'''
    menu_ini = Tk()
    menu_ini.state('zoomed')
    menu_ini.rowconfigure(0,weight=1)
    menu_ini.columnconfigure(0,weight=1)

    tools.interface_add.WindowMain(menu_ini,data_base,True)
    menu_ini.mainloop()

if __name__ == '__main__':
    main()

# Add the introduced vehicle in the data_base file
with open(data_base_directory, "wb") as pickle_file:
    pickle.dump(data_base, pickle_file)
