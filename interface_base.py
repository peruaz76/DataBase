# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:34:39 2022

@author: Peru _Alana
"""
import os
from tkinter import ttk, Label, Frame, W, E, S, N
import tkinter as Tk
import tkinter.font as TkFont
import pandas as pd
from ttkbootstrap import Style
from PIL import ImageTk, Image
import re

from copy import deepcopy
from datetime import datetime
from getpass import getuser

from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import tools.interface_add
import tools.class_real_bogie

import pickle5 
import pickle

''' 
Color dictionary for the program
'''
colors= {}
colors['darkred']='#FF0000'
colors['darkblue']='#3399FF'
colors['orange']='#FD8D2A'
colors['yelow']='#E2DC39'
colors['ligthgreen']='#63D451'
colors['darkgreen']='#336600'
colors['ligthblue']='#00FFFF'
colors['ligthred']='#FF6666'
colors['purple']='#7F00FF'
colors['grey']='#708090'
colors['darkpink']='#CC00CC'
colors['blue_3']='#40E0D0'
colors['green_3']='#16A085'

name_colors = colors.values()
name_colors = list(name_colors)

linestyle= ['-', '--', '-.', ':','-', '--', '-.', ':','-', '--', '-.', ':','-', '--', '-.', ':','-', '--', '-.', ':' ]

# Program directory
current_path = os.getcwd()
data_base_directory = current_path + '/data_base/data_base.pkl'
FONT_TITLE = ('Helvetica', 10, "bold")

bars=[]
name_list= []

# Create lists to use with histogram data
for num in range(100):
    name = 'lista_plot{}'.format(num+1)
    name_list.append(name)
    name_list[num]=[]
  

class Base_interface():
    """
    class Base_interface:
        Base interface with general functions for the program

    Properties
    ----------

    master: Tk
        The tkinter window is stored in this variable

    width: Float
        This value has been initialized to save the screen width

    height: FLoat
        This value has been initialized to save the screen height

    Methods
    -------
    close_button(self,frames):
        Create exit window button

    close_program(self):
        Method to close program

    back_button(self, frame_forget, _class_raise):
        Create back to another frame button

    back_program(self,frame_forget,_class_raise):
        Method to go back frames

    menu_button(self,frame_forget):
        Create button to navigate to Main Menu

    travel_menu(self,frame_forget):
        Method to navigate to Main Menu

    new_frame(self,name):
        Method to create a new frame for the program

    figure_to_bars(self,ncols,nrows,frame):
        Create figure with a custom subplot and dimensions 

    bars_function(self,frame,data_plt,color,distance,name_bogie,list_figure,mode, list_who_plot,name_list):
        Separate imported data in different list to plot histogram with them

    list_to_dict(self,key_list, dictiorary):
        Create dictinary form any list

    dictionary_data_base(self):
        Create nested dictionary of the all data base

    to_csv_function(self,columns,index,data):
        With column, index and data create a correct dataframe to convert to csv

    create_figure(self,x,y,title,x_label,y_label,frame):
        Function to createa and configure

    """
    def __init__(self,master):
        self.master = master

        # Calculate screen size
        self.width=master.winfo_screenwidth()  
        self.height= master.winfo_screenheight()

        # Define style to GUI
        style = Style('flatly')
        # style.theme_use('default')
        self.title3 = TkFont.Font(family="Helvetica",size=13,underline=1)

    def close_button(self,frames):
        '''Create window close button'''

        self.close = ttk.Button(frames, text = 'EXIT',
                                style='danger.TButton', command = self.close_program)
        self.close.place( x= (0.96*float(self.width)),y=(0.9*float(self.height)))

    def close_program(self):
        '''Close the program '''

        self.master.destroy()

    def back_button(self, frame_forget, _class_raise):
        '''Back-to button create'''

        self.back = ttk.Button(frame_forget, text = 'BACK',
                               style='warning.Outline.TButton',
                               command = lambda:[self.back_program(frame_forget, _class_raise)])
        self.back.place( x= (0.025*float(self.width)),y=(0.85*float(self.height)))

    def back_program(self,frame_forget,_class_raise):
        '''Method to go back in the program'''

        frame_forget.pack_forget()
        _class_raise(self.master, self.data_base)


    def menu_button(self,frame_forget):
        '''Create button to navigate to main menu'''

        self.menu = ttk.Button(frame_forget, text = 'Main Menu', style='secondary.TButton', command = lambda:[self.travel_menu(frame_forget)])
        self.menu.place( x= (0.02*float(self.width)),y=(0.9*float(self.height)))

    def travel_menu(self,frame_forget):
        '''Navigate to Main Menu'''

        frame_forget.pack_forget()
        # print('menu_button', self.admin_mode)
        tools.interface_add.WindowMain(self.master, self.data_base, self.admin)
     
    def new_frame(self,name):
        ''' General method to create new frame'''

        frames= Frame(self.master)
        self.master.title('{}'.format(name))

        # Configure frame grid in the tkinter window
        frames.grid(row=0, column=0, sticky=N+S+E+W)
        for row_index in range(15):
            frames.rowconfigure(row_index, weight=1,minsize=40)
            for col_index in range(20):
                frames.columnconfigure(col_index, weight=1,minsize=40)

        # CAF I+D logo imported
        label2 = self.import_image(150, 60, "png_library\\caf_id.png", frames)
        label2.place( x= (0.9*float(self.width)),y=(0.01*float(self.height)))
        return frames

    def list_to_dict(self,key_list, dictiorary):
        '''Method to convert any list in a dictionary '''
        temp_dict = {}
        for key in key_list:
            value = dictiorary[key]
            if type(value)== list:
                for l in range(len(value)):
                    temp_dict[l] = value[l]
                dictiorary[key] = temp_dict
                temp_dict = {}
            
    def create_figure(self,x,y,title,x_label,y_label,frame,txt):
        '''Create figure for the frame'''

        fig = Figure(figsize=(x,y), dpi=100) 
        axis = fig.add_subplot(111) 
        canvas = FigureCanvasTkAgg(fig, master = frame)
        # fig.patch.set_facecolor('blue')
        canvas.draw()
        
        toolbar = NavigationToolbar2Tk(canvas,frame,pack_toolbar=False)
        axis.set_title(title)
        axis.set_xlabel(x_label)
        axis.set_ylabel(y_label)
        axis.text(1.025,0.5,txt,horizontalalignment='center',verticalalignment='center', transform = axis.transAxes,rotation=90, fontsize=8, color= 'red')
     
        return fig, axis, toolbar, canvas

    def import_image(self,x,y,path,frame):
        '''Import image as label in a frame'''
        image2 = Image.open(path)
        image2 = image2.resize((x, y), Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(image2)
        label2 = Label(frame, image = photo2)
        label2.image2 = photo2
        label2.configure
        return label2

    def import_data_to_table(self):
        '''Import vehicle data to the main menu table '''
        i=0
        data=[]
        while i<int(len(self.data_base.name_list)):
            b_str=''
            c_str=''
            name = self.data_base.name_list[i]
            b_config = self.data_base.vehicle[i].BOGIE_CONFIG['value']
            for bogie in b_config:
                b_str=b_str+str(bogie)+'-'    
            c_config = self.data_base.vehicle[i].CARBODY_CONFIG['value']
            for carbody in c_config:
                c_str = c_str+str(carbody)+'-'
            b_str=b_str[:-1]
            c_str=c_str[:-1]
            v_type = self.data_base.vehicle[i].VEHICLE_TYPE['value']
            v_code = self.data_base.vehicle[i].PROJECT_CODE['value']
            data.append((f'{v_code}',f'{name}',f'{v_type}',f'{b_str}',f'{c_str}'))
            i=i+1
        return data

    def import_all_the_proyect(self):
        '''Method to read excel and save all the attribute values in the database'''
        already_in = False
        atr_vehicle = deepcopy(self.data_base.attributes)
        archivo=fd.askopenfilename(initialdir=current_path + '/excel',
                                      title='Proyect Data',
                                      filetype=(('xls files','*xls*'),('All files','*.*')))
        dataframes={}

        sheet = pd.read_excel(archivo,None)
        sheet = list(sheet.keys())


        for pagina in sheet:
            df =  pd.read_excel(archivo,'{}'.format(pagina))
            dataframes[pagina] = df


        if archivo != '':
            df_proyect = pd.read_excel(archivo)
            df_track = pd.read_excel(archivo,'Track')
            df_carbody = pd.read_excel(archivo,'Carbody_data')
            df_carbody_link = pd.read_excel(archivo,'Carbody_links')
            df_wheeload = pd.read_excel(archivo,'LOADS')
            sheet = pd.read_excel(archivo,None)
            sheet = list(sheet.keys())

        # Create Vehicle
        name=archivo.split('/')
        name = name[len(name)-1]
        name = name.split('_')
        name = name[1]
        name = name.split('.')
        name = name[0]


        # Vehicle data
        values = list(df_proyect.iloc[:,1])
        sources = list(df_proyect.iloc[:,4])
        comments = list(df_proyect.iloc[:,5])
        atr_names = list(df_proyect.iloc[:,0])
        ini_code = values[0]
        for vehicle in self.data_base.vehicle:
            data = getattr(vehicle,'PROJECT_CODE')
            code = data['value']
            if code == ini_code:
                already_in = True

        if already_in:
            Tk.messagebox.showwarning(title = 'Warning' , message = 'The {} is already in the database'.format(ini_code))

        else:   
            self.train = tools.class_vehicle.Vehicle(name,atr_vehicle[0])
            train_atr = list((vars(self.train)).keys())
            self.data_base.add_vehicle(self.train, name)
            
            list_no = ['name', 'sheet' , 'bogie', 'carbody', 'carbody_links', 'carbody_links_names','carbody_2','real_bogie','track','excel']
            for atr in train_atr:
                if atr in list_no:
                    pass
                else:
                    if hasattr(self.train,atr):
                        dicti = getattr(self.train,atr)
                        index = atr_names.index(atr)
                        value = values[index]
                        source = sources[index]
                        comment = comments[index]
                        if 'BOGIE' in atr:
                            value = value.split('-')
                        elif 'CARBODY' in atr:
                            value = value.split('-')
                        elif 'TRAIN_CONFIG' in atr:
                            value = value.split('-')

                        dicti['value'] = value
                        dicti['Source'] = source
                        dicti['Comments'] = comment
                        setattr(self.train, atr, dicti)
    
            self.train.sheet = sheet
            self.train.excel = dataframes
            # # Import carbody Data
            carbodies = []
            c_names = (list(df_carbody.head()))[1:]
            units_index = c_names.index('Units')
            c_names = c_names[0:int(units_index)]
            atributtes_car = list(df_carbody.iloc[:,0])

            sources = list(df_carbody.iloc[:,units_index+3])
            comments = list(df_carbody.iloc[:,units_index+4])
            j=1
            for car_name in c_names:
                self.new_carbody = tools.class_carbody.Carbody(car_name, atr_vehicle[2])
                self.train.carbody.append(self.new_carbody)
            for carbody in self.train.carbody:
                data = []
                values = list(df_carbody.iloc[:,j])
                for atr in atributtes_car:
                    if str(atr) == 'nan':
                        pass
                    else:
                        if hasattr(carbody,atr):
                            dicti = getattr(carbody,atr)

                            index = atributtes_car.index(atr)
                            value = values[index]
                            source = sources[index]
                            comment = comments[index]
                            dicti['value'] = value
                            dicti['Source'] = source
                            dicti['Comments'] = comment
                            setattr(carbody, atr, dicti)
                carbodies.append(deepcopy(carbody))
                j=j+1
            setattr(self.train, 'carbody', carbodies)
           
            
            # Import atributtes from bogie 
            bogies = []
            b_names = (self.train.BOGIE_CONFIG)['value']
    
            for bogie_name in b_names:
                self.new_bogie = tools.class_bogie.Bogie(bogie_name, atr_vehicle[1])
                self.train.bogie.append(self.new_bogie)
    
            for bogie in self.train.bogie:
                index = self.train.bogie.index(bogie)
                name = b_names[int(index)]
                df_bogie = pd.read_excel(archivo,'{}'.format(name))
                atributtes_bogie = list(df_bogie.iloc[1:,0])
                values = list(df_bogie.iloc[1:,1])
                sources = list(df_bogie.iloc[1:,4])
                comments = list(df_bogie.iloc[1:,5])
    
                for atr in atributtes_bogie:
                    if str(atr) == 'nan':
                        pass
                    else:

                        if hasattr(bogie,atr):
                            dicti = getattr(bogie,atr)
                            index = atributtes_bogie.index(atr)
                            value = values[index]
                            if type(value) is str:
                                if value in self.train.sheet:
                                    df_curve = pd.read_excel(archivo,'{}'.format(value))
                                    units_np = list(df_curve.head())
                                    numpy = df_curve.to_numpy()
                                    numpy = numpy [:,[1,0]]
                                    value =  {value:numpy,'x':units_np[0],'y':units_np[1]}
                            source = sources[index]
                            comment = comments[index]
                            dicti['value'] = value
                            dicti['Source'] = source
                            dicti['Comments'] = comment
                            setattr(bogie, atr, dicti)
                bogies.append(deepcopy(bogie))
    
            setattr(self.train, 'bogie', bogies)

            
            # # Import Carbody Links
            links = []
            heads = list(df_carbody_link.head())[1:]
            names = []
            units_index = heads.index('Units')
            for head in heads:
                if heads.index(head)<units_index:
                    list_head = head.split('_')
                    names.append(list_head[1])
            self.train.carbody_links_names = names
            atributtes_link = list(df_carbody_link.iloc[:,0])
            sources = list(df_carbody_link.iloc[:,units_index+3])
            comments = list(df_carbody_link.iloc[:,units_index+4])
            j=1
            for l_name in names:
                self.new_link = tools.class_carbody_links.CarbodyLinks(l_name, atr_vehicle[3])
                self.train.carbody_links.append(self.new_link)
            for link in self.train.carbody_links:
                data = []
                values = list(df_carbody_link.iloc[:,j])
                for atr in atributtes_link:
                    if str(atr) == 'N/A':
                        pass
                    else:
                        if hasattr(link,atr):
                            dicti = getattr(link,atr)
                            index = atributtes_link.index(atr)
                            value = values[index]
                            if type(value) is str:
                                if value in self.train.sheet:
                                    df_curve = pd.read_excel(archivo,'{}'.format(value))
                                    units_np = list(df_curve.head())
                                    numpy = df_curve.to_numpy()
                                    numpy = numpy [:,[1,0]]
                                    value =  {value:numpy,'x':units_np[0],'y':units_np[1]}
                            source = sources[index]
                            comment = comments[index]
                            dicti['value'] = value
                            dicti['Source'] = source
                            dicti['Comments'] = comment
                            setattr(link, atr, dicti)
                links.append(deepcopy(link))
                j=j+1
            setattr(self.train, 'carbody_links', links)

            # Create Real Bogie objects
            self.list_real_bogies = []
            config = self.train.TRAIN_CONFIG['value']
        
            if len(config) > 0:
                i=0
                for real in config:

                    bogie_name = real.split('(')[0]
                    index = self.train.BOGIE_CONFIG['value'].index(bogie_name)
                    bogie_object = self.train.bogie[index]
                    carbody = re.findall(r'[(](.*?)[)]', real)
                    real_bogie = tools.class_real_bogie.RealBogie(bogie_object,carbody[0],real)
                    self.list_real_bogies.append(real_bogie)

                self.train.real_bogie = self.list_real_bogies


            # Import excel data to real bogie objects

            wheels = list(df_wheeload.iloc[6])

            names = ['QZ0_WOP_1','QZ0_NP_1','QZ0_EP_1','QZ0_WOP_3','QZ0_NP_3','QZ0_EP_3', 'QZ0_WOP_2','QZ0_NP_2','QZ0_EP_2', 'QZ0_WOP_4','QZ0_NP_4', 'QZ0_EP_4']
            j=0
            i=0
            while i<len(self.train.real_bogie):
                list_num = []
                values0 = []
                values1 = []
                values2 = []
                object_ = self.train.real_bogie[i]
                for k in range(int(len(self.train.real_bogie))):
                    list_num.append((k+1)*4)
                while j<list_num[i]:
                    for k in range(3):
                        value = df_wheeload.iat[k+1,j+1]
                        if len(values0) < len(names):
                            values0.append(value)
                    for k in [6,7,8]:
                        value = df_wheeload.iat[k+1,j+1]
                        if len(values1) < len(names):
                            values1.append(value)
                    for k in [12,13,14]:
                        value = df_wheeload.iat[k+1,j+1]
                        if len(values2) < len(names):
                            values2.append(value)
                    j=j+1

                for index,name in enumerate(names):
                    setattr(object_, name, {'value':values0[index],'units':'kN'})
                    name1 = name.replace('0','1',1)
                    name2 = name.replace('0','2',1)
                    setattr(object_, name1, {'value':values1[index],'units':'kN'})
                    setattr(object_, name2, {'value':values2[index],'units':'kN'})
                object_.calculate_loads()
                i=i+1

            # Import track data to data base
            
            values = list(df_track.iloc[:,1])
            sources = list(df_track.iloc[:,4])
            comments = list(df_track.iloc[:,5])
            atr_names = list(df_track.iloc[:,0])

            self.track = tools.class_track.Track( atr_vehicle[4])
            track_atr = list((vars(self.track)).keys())
            self.train.track.append(self.track)
            
            for atr in track_atr:
                if hasattr(self.track,atr):
                    dicti = getattr(self.track,atr)
                    index = atr_names.index(atr)
                    value = values[index]
                    source = sources[index]
                    comment = comments[index]
                    dicti['value'] = value
                    dicti['Source'] = source
                    dicti['Comments'] = comment
                    setattr(self.track, atr, dicti)
            
            
    def search_atr_database(self,name_vehicle,columns,name):
        values = []
        for col in columns:
            self.train = self.data_base.vehicle[self.data_base.name_list.index(name_vehicle)]
            name2 = name
            if '-' in name:
                name = name.split('-')[0]

            if name in self.train.BOGIE_CONFIG['value']:
                self.bogie = self.train.bogie[self.train.BOGIE_CONFIG['value'].index(name)]
                if hasattr(self.bogie,col) is True:
                    value = (getattr(self.bogie,col))['value']
                    if type(value) is dict:
                        value = list(value.keys())[0]
                else:
                    value = 'N/A'
                values.append(value)
    
            elif name in self.train.CARBODY_CONFIG['value']:
                self.carbody = self.train.carbody[self.train.CARBODY_CONFIG['value'].index(name)]
                if hasattr(self.carbody,col) is True:
                    value = (getattr(self.carbody,col))['value']
                    if type(value) is dict:
                        value = list(value.keys())[0]
                else:
                    value = 'N/A'
                values.append(value)
    
            elif name in self.train.carbody_links_names:
                self.link = self.train.carbody_links[self.train.carbody_links_names.index(name)]
                if hasattr(self.link,col) is True:
                    value = (getattr(self.link,col))['value']
                    if type(value) is dict:
                        value = list(value.keys())[0]
                else:
                    value = 'N/A'
                values.append(value)
    
            elif name in self.train.TRAIN_CONFIG['value']:
    
                index = self.train.TRAIN_CONFIG['value'].index(name)
                if '-' in name2:
                    index = index + 1
                self.real_bogie = self.train.real_bogie[index]
                if hasattr(self.real_bogie,col) is True:
                    value = (getattr(self.real_bogie,col))['value']
                    if type(value) is dict:
                        value = list(value.keys())[0]
                else:
                    object_ = self.real_bogie.bogie_object
                    if hasattr(object_,col) is True:
                        value = (getattr(object_,col))['value']
                        if type(value) is dict:
                            value = list(value.keys())[0]
                    else:
                        value = 'N/A'
                values.append(value)
    
            elif name == 'Track':
                self.track = self.train.track[0]
                if hasattr(self.track, col):
                    value = (getattr(self.track, col))['value']
                else:
                    value = 'N/A'
                values.append(value)        

        return values

    def data_to_excel(self,train):
        archivo=fd.asksaveasfilename(filetype=(('xls files','*xls*'),('All files','*.*')))
        archivo = archivo + '.xlsx'

        dataframes = train.excel
        dataframes = dataframes.values()
        sheet = train.sheet
        Excelwriter = pd.ExcelWriter(archivo, engine="xlsxwriter")

        for i,df in enumerate(dataframes):
            pag = sheet[i]
            df.to_excel(Excelwriter,sheet_name='{}'.format(pag),index=False)
        Excelwriter.save()
        pass
            
    def search_units(self, attribute):
      list_atrs = self.data_base.attributes
      for index, list_ in enumerate(list_atrs):
          if attribute in list_:
              dicti = list_[attribute]
              unit = dicti['units']
              return unit
          elif 'QZ' in attribute:
              unit = 'kN'
              return unit

    def search_description(self, attribute):
        list_atrs = self.data_base.attributes
        for index, list_ in enumerate(list_atrs):
            if attribute in list_:
                dicti = list_[attribute]
                descr = dicti['Description']
                return descr
            elif 'QZ' in attribute:
                descr = 'N/A'
                return descr

             
            
            
            
            
            