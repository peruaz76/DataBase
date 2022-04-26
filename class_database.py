# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 08:30:37 2022

@author: Peru _Alana
"""

##############################################################################
#                                CLASS DATA_BASE                             #
##############################################################################


class Data_base():
    """
    class Data_base():
        In this class the Vehicle's data are stored.

    Properties
    ----------
    vehicle: List
        List of vehicle's of the data base.
    name_list: List
        List of vehicle names

    Methods
    -------
    add_vehicle(self,vehicle_name):
        Insert the vehicle name on the list Vehicle[]
    delete_vehicle(self, index)
        Detele the vehicle in the list
    """

    def __init__(self):

        #List of Vehicle
        self.vehicle = []
        self.name_list = []
        self.attributes = []
        

    def add_vehicle(self,vehicle_name,name_t):
        '''Append the vehicle name to the list'''

        self.vehicle.append(vehicle_name)
        self.name_list.append(name_t)

    def add_attributes(self,vehi,bogie,car,link,track):
        self.attributes = [vehi,bogie,car,link,track]
