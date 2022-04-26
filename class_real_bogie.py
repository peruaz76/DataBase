# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 13:50:19 2022

@author: Peru _Alana
"""
import statistics

class RealBogie:
    def __init__(self, object_bogie, carbody_name,name):
        self.name = name
        self.bogie_object = object_bogie
        self.carbody_name = carbody_name

        # Wheel Load
        self.QZ0_WOP_1 = 0.0
        self.QZ0_WOP_3= 0.0
        self.QZ0_WOP_2 = 0.0
        self.QZ0_WOP_4= 0.0

        self.QZ0_NP_1 = 0.0
        self.QZ0_NP_3= 0.0
        self.QZ0_NP_2 = 0.0
        self.QZ0_NP_4= 0.0

        self.QZ0_EP_1 = 0.0
        self.QZ0_EP_3= 0.0
        self.QZ0_EP_2 = 0.0
        self.QZ0_EP_4= 0.0

        #Primary Load
        self.QZ1_WOP_1 = 0.0
        self.QZ1_WOP_3= 0.0
        self.QZ1_WOP_2 = 0.0
        self.QZ1_WOP_4= 0.0

        self.QZ1_NP_1 = 0.0
        self.QZ1_NP_3= 0.0
        self.QZ1_NP_2 = 0.0
        self.QZ1_NP_4= 0.0

        self.QZ1_EP_1 = 0.0
        self.QZ1_EP_3= 0.0
        self.QZ1_EP_2 = 0.0
        self.QZ1_EP_4= 0.0


        #Secondary Load
        self.QZ2_WOP_1 = 0.0
        self.QZ2_WOP_3= 0.0
        self.QZ2_WOP_2 = 0.0
        self.QZ2_WOP_4= 0.0

        self.QZ2_NP_1 = 0.0
        self.QZ2_NP_3= 0.0
        self.QZ2_NP_2 = 0.0
        self.QZ2_NP_4= 0.0

        self.QZ2_EP_1 = 0.0
        self.QZ2_EP_3= 0.0
        self.QZ2_EP_2 = 0.0
        self.QZ2_EP_4= 0.0

        self.QZ0_WOP_MAX= 0.0
        self.QZ0_WOP_AVG= 0.0
        self.QZ0_WOP_MIN = 0.0

        self.QZ0_EP_MAX = 0.0
        self.QZ0_EP_AVG = 0.0
        self.QZ0_EP_MIN = 0.0

        self.QZ0_NP_MAX = 0.0
        self.QZ0_NP_AVG = 0.0
        self.QZ0_NP_MIN = 0.0

        #Primary Load
        self.QZ1_WOP_MAX = 0.0
        self.QZ1_WOP_AVG = 0.0
        self.QZ1_WOP_MIN = 0.0

        self.QZ1_EP_MAX = 0.0
        self.QZ1_EP_AVG = 0.0
        self.QZ1_EP_MIN = 0.0

        self.QZ1_NP_MAX = 0.0
        self.QZ1_NP_AVG = 0.0
        self.QZ1_NP_MIN = 0.0

        #Secondary Load
        self.QZ2_WOP_MAX = 0.0
        self.QZ2_WOP_AVG = 0.0
        self.QZ2_WOP_MIN = 0.0

        self.QZ2_EP_MAX = 0.0
        self.QZ2_EP_AVG = 0.0
        self.QZ2_EP_MIN = 0.0

        self.QZ2_NP_MAX= 0.0
        self.QZ2_NP_AVG = 0.0
        self.QZ2_NP_MIN = 0.0
        
    def calculate_loads(self):
        #Wheel Load
        self.QZ0_WOP_MAX = {'value':max([self.QZ0_WOP_1['value'],self.QZ0_WOP_3['value'],self.QZ0_WOP_2['value'],self.QZ0_WOP_4['value']]),'units':'kN'}
        self.QZ0_WOP_AVG = {'value':statistics.median([self.QZ0_WOP_1['value'],self.QZ0_WOP_3['value'],self.QZ0_WOP_2['value'],self.QZ0_WOP_4['value']]),'units':'kN'}
        self.QZ0_WOP_MIN ={'value': min([self.QZ0_WOP_1['value'],self.QZ0_WOP_3['value'],self.QZ0_WOP_2['value'],self.QZ0_WOP_4['value']]),'units':'kN'}

        self.QZ0_EP_MAX = {'value':max([self.QZ0_EP_1['value'],self.QZ0_EP_3['value'],self.QZ0_EP_2['value'],self.QZ0_EP_4['value']]),'units':'kN'}
        self.QZ0_EP_AVG = {'value':statistics.median([self.QZ0_EP_1['value'],self.QZ0_EP_3['value'],self.QZ0_EP_2['value'],self.QZ0_EP_4['value']]),'units':'kN'}
        self.QZ0_EP_MIN = {'value':min([self.QZ0_EP_1['value'],self.QZ0_EP_3['value'],self.QZ0_EP_2['value'],self.QZ0_EP_4['value']]),'units':'kN'}

        self.QZ0_NP_MAX ={'value':max([self.QZ0_NP_1['value'],self.QZ0_NP_3['value'],self.QZ0_NP_2['value'],self.QZ0_NP_4['value']]),'units':'kN'}
        self.QZ0_NP_AVG = {'value':statistics.median([self.QZ0_NP_1['value'],self.QZ0_NP_3['value'],self.QZ0_NP_2['value'],self.QZ0_NP_4['value']]),'units':'kN'}
        self.QZ0_NP_MIN = {'value':min([self.QZ0_NP_1['value'],self.QZ0_NP_3['value'],self.QZ0_NP_2['value'],self.QZ0_NP_4['value']]),'units':'kN'}

        #Primary Load
        self.QZ1_WOP_MAX = {'value':max([self.QZ1_WOP_1['value'],self.QZ1_WOP_3['value'],self.QZ1_WOP_2['value'],self.QZ1_WOP_4['value']]),'units':'kN'}
        self.QZ1_WOP_AVG = {'value':statistics.median([self.QZ1_WOP_1['value'],self.QZ1_WOP_3['value'],self.QZ1_WOP_2['value'],self.QZ1_WOP_4['value']]),'units':'kN'}
        self.QZ1_WOP_MIN ={'value': min([self.QZ1_WOP_1['value'],self.QZ1_WOP_3['value'],self.QZ1_WOP_2['value'],self.QZ1_WOP_4['value']]),'units':'kN'}

        self.QZ1_EP_MAX = {'value':max([self.QZ1_EP_1['value'],self.QZ1_EP_3['value'],self.QZ1_EP_2['value'],self.QZ1_EP_4['value']]),'units':'kN'}
        self.QZ1_EP_AVG = {'value':statistics.median([self.QZ1_EP_1['value'],self.QZ1_EP_3['value'],self.QZ1_EP_2['value'],self.QZ1_EP_4['value']]),'units':'kN'}
        self.QZ1_EP_MIN = {'value':min([self.QZ1_EP_1['value'],self.QZ1_EP_3['value'],self.QZ1_EP_2['value'],self.QZ1_EP_4['value']]),'units':'kN'}

        self.QZ1_NP_MAX ={'value':max([self.QZ1_NP_1['value'],self.QZ1_NP_3['value'],self.QZ1_NP_2['value'],self.QZ1_NP_4['value']]),'units':'kN'}
        self.QZ1_NP_AVG = {'value':statistics.median([self.QZ1_NP_1['value'],self.QZ1_NP_3['value'],self.QZ1_NP_2['value'],self.QZ1_NP_4['value']]),'units':'kN'}
        self.QZ1_NP_MIN = {'value':min([self.QZ1_NP_1['value'],self.QZ1_NP_3['value'],self.QZ1_NP_2['value'],self.QZ1_NP_4['value']]),'units':'kN'}

        #Secondary Load
        self.QZ2_WOP_MAX = {'value':max([self.QZ2_WOP_1['value'],self.QZ2_WOP_3['value'],self.QZ2_WOP_2['value'],self.QZ2_WOP_4['value']]),'units':'kN'}
        self.QZ2_WOP_AVG = {'value':statistics.median([self.QZ2_WOP_1['value'],self.QZ2_WOP_3['value'],self.QZ2_WOP_2['value'],self.QZ2_WOP_4['value']]),'units':'kN'}
        self.QZ2_WOP_MIN ={'value': min([self.QZ2_WOP_1['value'],self.QZ2_WOP_3['value'],self.QZ2_WOP_2['value'],self.QZ2_WOP_4['value']]),'units':'kN'}

        self.QZ2_EP_MAX = {'value':max([self.QZ2_EP_1['value'],self.QZ2_EP_3['value'],self.QZ2_EP_2['value'],self.QZ2_EP_4['value']]),'units':'kN'}
        self.QZ2_EP_AVG = {'value':statistics.median([self.QZ2_EP_1['value'],self.QZ2_EP_3['value'],self.QZ2_EP_2['value'],self.QZ2_EP_4['value']]),'units':'kN'}
        self.QZ2_EP_MIN = {'value':min([self.QZ2_EP_1['value'],self.QZ2_EP_3['value'],self.QZ2_EP_2['value'],self.QZ2_EP_4['value']]),'units':'kN'}

        self.QZ2_NP_MAX ={'value':max([self.QZ2_NP_1['value'],self.QZ2_NP_3['value'],self.QZ2_NP_2['value'],self.QZ2_NP_4['value']]),'units':'kN'}
        self.QZ2_NP_AVG = {'value':statistics.median([self.QZ2_NP_1['value'],self.QZ2_NP_3['value'],self.QZ2_NP_2['value'],self.QZ2_NP_4['value']]),'units':'kN'}
        self.QZ2_NP_MIN = {'value':min([self.QZ2_NP_1['value'],self.QZ2_NP_3['value'],self.QZ2_NP_2['value'],self.QZ2_NP_4['value']]),'units':'kN'}