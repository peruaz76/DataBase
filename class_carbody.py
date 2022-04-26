# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:32:02 2022

@author: Peru _Alana
"""

##############################################################################
#                                CLASS CARBODY                               #
##############################################################################

class Carbody():
    """
    class Carbody():
        In this class the Carbody's properties are stored.

    Properties
    ----------
    name: string
        Carbody name.

    """
    def __init__(self,name,dicti):
        #Name of the Bogie
        self.name = name

        if dicti != {}:
            for k, v in dicti.items():
                setattr(self, k, v)
