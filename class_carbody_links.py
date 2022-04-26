# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:33:32 2022

@author: Peru _Alana
"""

class CarbodyLinks():
    """
    class CarbodyLinks():
        In this class the Carbody Link's properties are stored.

    Properties
    ----------
    name: string
        Carbody Link name.

    """
    def __init__(self,name,dicti):

        self.name = name
        self.linkage_type = ''

        if dicti != {}:
            for k, v in dicti.items():
                setattr(self, k, v)
        