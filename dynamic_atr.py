# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:14:31 2022

@author: Peru _Alana
"""


import os
import pandas as pd

def atr_ini():
    '''Function to conver attributes in dictionaries'''

    current_path = os.getcwd()
    archivo = current_path + '\excel' + '\plantilla_ini.xlsx'

    if archivo != '':
        df_proyect = pd.read_excel(archivo)
        df_track = pd.read_excel(archivo,'Track')
        df_carbody = pd.read_excel(archivo,'Carbody_data')
        df_carbody_link = pd.read_excel(archivo,'Carbody_links')
        df_wheeload = pd.read_excel(archivo, 'WHEELOAD')
        paginas = pd.read_excel(archivo,None)
        paginas = list(paginas.keys())

    values = (list(df_proyect.iloc[:,0]))
    units = (list(df_proyect.iloc[:,2]))
    description = (list(df_proyect.iloc[:,3]))

    vehicle_atr = {}
    i=0
    for atr in values:
        vehicle_atr[atr] = {'value':'','units':units[i],'Description':description[i],
                            'Source':'', 'Comments': ''}
        i=i+1

    # Atributes carbody
    carbody_atr = {}
    head = ((list(df_carbody.head()))[1:])
    index_unit = head.index('Units')
    atr_car = list(df_carbody.iloc[:,0])
    units = (list(df_carbody.iloc[:,index_unit+1]))
    description = (list(df_carbody.iloc[:,index_unit +2]))

    i=0
    while i < (len(atr_car)-1):
        if ('*' in str(atr_car[i])) is True:
            i=i+1
            while ('*' in str(atr_car[i])) is False:
                if str(atr_car[i]) == 'nan':
                    pass

                else:
                    carbody_atr[atr_car[i]]={'value':'','units':units[i],'Description':description[i],
                                                'Source':'', 'Comments': '', 'block':'Carbody Data'}
                i=i+1
        else:
            i=i+1

    # Carbody Link attributes
    link_atr = {}
    head = ((list(df_carbody_link.head()))[1:])
    index_unit = head.index('Units')

    link_atr_value = list(df_carbody_link.iloc[:,0])
    units = list(df_carbody_link.iloc[:,index_unit+1])
    description = list(df_carbody_link.iloc[:,index_unit+2])
    i=0

    while i < (len(link_atr_value)-1):
        if ('*' in str(link_atr_value[i])) is True:
            block = (str(link_atr_value[i]))[1:]
            i=i+1
            while ('*' in str(link_atr_value[i])) is False:
                if str(link_atr_value[i]) == 'nan':
                    pass
                else:
                    link_atr[link_atr_value[i]]={'value':'','units':units[i],
                                                 'Description':description[i],
                                                 'Source':'', 'Comments': '','block':block}
                i=i+1
        else:
            i=i+1

    # Bogie attributes

    # Dictionary of attributes
    df_bogie = pd.read_excel(archivo, 'Bogie')
    bogie_atr = {}
    bogie_atr_value = list(df_bogie.iloc[:,0])
    units = list(df_bogie.iloc[:,2])
    description = list(df_bogie.iloc[:,3])
    i=0
    while i < (len(bogie_atr_value)-1):
        if ('*' in str(bogie_atr_value[i])) is True:
            block = (str(bogie_atr_value[i]))[1:]
            i=i+1
            while ('*' in str(bogie_atr_value[i])) is False:
                if str(bogie_atr_value[i]) == 'nan':
                    pass
                else:
                    bogie_atr[bogie_atr_value[i]]={'value':'','units':units[i],
                                                   'Description':description[i],
                                                   'Source':'', 'Comments': '',
                                                   'block':block}
                i=i+1
        else:
            i=i+1

    # Wheel loads attributes
    # atributtes_wheeload = list(df_wheeload.iloc[1:,0])
    # i=0
    # atr_wheeload = {}
    # list_names = []
    # while i< (len(atributtes_wheeload)-1):
    #     if '*' in atributtes_wheeload[i]:
    #         i=i+1
    #         while ('*' not in atributtes_wheeload[i]):
    #             name =  atributtes_wheeload[i]
    #             units = df_wheeload.iat[i+1,4]
    #             descri = df_wheeload.iat[i+1,5]
    #             atr_wheeload[name] = {'value':'', 'units':units, 'Description':descri,'Source':'', 'Comments':'', 'block':'Wheel Load'}
    #             print(atr_wheeload)
    #             i=i+1
    #     else:
    #             i=i+1

    # print(atr_wheeload)

    # Track attributes
    values = (list(df_track.iloc[:,0]))
    units = (list(df_track.iloc[:,2]))
    description = (list(df_track.iloc[:,3]))

    track_atr = {}
    i=0
    for atr in values:
        track_atr[atr] = {'value':'','units':units[i],'Description':description[i],
                            'Source':'', 'Comments': '','block':'Track Attributes'}
        i=i+1
 
    return vehicle_atr, bogie_atr, carbody_atr, link_atr,track_atr
