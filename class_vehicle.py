# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:30:02 2022

@author: Peru _Alana
"""

##############################################################################
#                              VEHICLE CLASS                                 #
##############################################################################
class Vehicle():
    """
    class Vehicle():
        In this class the Vehicle's properties are stored.

    Properties
    ----------
    name: string
        Name of the vehicle or project.

    type: string
        Name of the vehicle's type.

    bogie: list of bogie objects
        Bogie objects are stored in this list.

    carbody: list of carbody objects
        Carbody objects are stored in this list.

    carbody_links_names:
        Carbody link names are stored in this list

    """

    def __init__(self, name,dicti):

        # Name of the vehicle
        self.name = name
        self.sheet =[]
        self.excel = {}
        # List of bogie objects
        self.bogie = []
        self.real_bogie = []

        # List of carbody objects
        self.carbody = []
        # List of Carbody Links
        self.carbody_links = []

        self.carbody_links_names = []

        self.track = []

        if dicti != {}:
            for k, v in dicti.items():
                setattr(self, k, v)
