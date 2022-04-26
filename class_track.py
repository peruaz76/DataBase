# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 08:04:42 2022

@author: Peru _Alana
"""

class Track():
    def __init__(self,dicti):
        if dicti != {}:
            for k, v in dicti.items():
                setattr(self, k, v)