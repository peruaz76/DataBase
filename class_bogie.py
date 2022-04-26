# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:31:02 2022

@author: Peru _Alana
"""

##############################################################################
#                                CLASS_BOGIE                                 #
##############################################################################
class Bogie():
    """
    class Bogie():
        In this class the Bogie's properties are stored.

    Properties
    ----------
    name: string
        Vehicle Bogie name.

    """


    def __init__(self,name,dicti):


       # Name of the Bogie
        self.name = name

        if dicti != {}:
            for k, v in dicti.items():
                setattr(self, k, v)
