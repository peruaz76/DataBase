# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:40:28 2022

@author: Peru _Alana
"""
from tkinter import ttk, END, Label
from tkinter import Frame,W, E, S, N,Scrollbar,RIGHT,Y, Canvas,CENTER,BOTTOM,X, Toplevel, Checkbutton
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.transforms import Bbox


from ttkwidgets import CheckboxTreeview

import pandas as pd
from tkinter import filedialog as fd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import mplcursors
from copy import deepcopy
from sklearn.metrics import r2_score

import tkinter as Tk
import tools.interface_add
import tools.interface_base

STYLE_LABEL = 'primary.TLabel'
STYLE_ENTRY = 'info.TEntry'

class CompareParameter(tools.interface_base.Base_interface):
    """
    class CompareParameter:
        Class to create compare parameters window

    Properties
    ----------

    values: list
        List to save values to plot
    column0: list
        Value created to save the names of the vehicle and part of this
    names: list
        List initilized to save checked attributes
    boxes: list
        List created to add attribute checkbox variables
    checkbox: list
        List created to add attribute checkbox
    list_canvas: list
        
    ploted_bars: list
        Variable to add attribute names who is ploted

    units: string
        String with the current attribute units

    hold_units: string
        String who save the units when hold checkbutton detect click

    atr_to_plot: list
        List initialized to save two attributes values

    units_to_plot: list
        List initialized to save two attributes units

    title_to_plot: list
        List initialized to save two attributes title


    Methods
    -------
    create_widgets(self):
        Create necesary widgets to the frame

    clear_two_atr(self):
        method to clear the figuer when detect event in the checkbox

    attributes_axis(self,table,col):
        Methot to plot one attribute against another

    position_text(self,event):
        Define data click  to postion there label with its project name

    set_axis(self):
        Update figure axis texts

    attribute_menu(self):
    detect_checkbox(self):
        Method to save current units value, when checkbox event change
        
    option_changed(self,list_var,option):
    elementos_deformables(self,boton1,boton2):
    body(self,boton1, boton2):

    sortby_val(self,filt):
        Filter search in the vehicles and in its parts, to check them
    sortby_atr(self, filt):
        
    select_all_checkbox(self):
    check_attributes(self):
    filter_description(self, filt, name):
        Iterate treeview elements, searching entry.get() text in their names and descriptions

    create_fig(self):
        Method to create figure in the frame

    export_to_csv(self):
        Export values table to excel to continue working with selected data

    plot_column(self,tree, col):
        Method to take out values from tabel to plot after

    plot_to_bar (self, data,values,title, numpy_detect, ylabel):
        Using values,title and other infroamtion, draw in the figure your type of plot

    clear_all(self):
        Clear all the selected checkbox and also teh figure

    import_attributes(self):
        This method imports all the vehicles from the database

    atribute_seleted(self):
        Method to confirm selected attributes and vehicles, and move values to another table 

    selectItem(self,event):
        Table attribute selection to popup new window with this ttribute values

    import_parameters(self):
        Import all the exixting attributes to a treeview table
        
    """
    def __init__(self, master,data_base,admin):
        super().__init__(master)

        # Call to Base interface to crate new frame
        self.frame_compare_parameter = self.new_frame('Compare Parameter')
        self.frame_compare_parameter.tkraise()

        self.data_base = data_base
        self.create_widgets()

        self.values = []
        self.column0 = []
        self.names = []
        self.boxes = []
        self.checkbox = []
        self.list_canvas = []
        self.ploted_bars = []
        self.units = ''
        self.hold_units = ''
        self.atr_to_plot = []
        self.units_to_plot = []
        self.title_to_plot = []
        self.check_on = False
        self.all_columns = []
        self.admin = admin
        self.multiple_ylabel = ''

    def create_widgets(self):
        '''Widgets of the frame'''

        # Define general widgets for the frame
        self.hold_var = Tk.BooleanVar(self.frame_compare_parameter)
        self.hold_check = Checkbutton(self.frame_compare_parameter, text = 'HOLD FIGURE', variable = self.hold_var, command = lambda:[self.detect_checkbox()])
        self.hold_check.grid(row=12, column=16, columnspan=3, rowspan=4)

        self.two_atr = Tk.BooleanVar(self.frame_compare_parameter)
        self.two_check = Checkbutton(self.frame_compare_parameter, text = 'TWO ATTRIBUTES', variable = self.two_atr, command = lambda:[self.clear_two_atr()])
        self.two_check.grid(row=13, column=16, columnspan=4)

        self.menu_button(self.frame_compare_parameter)
        self.close_button(self.frame_compare_parameter)

        self.search_atr_button = self.import_image(45, 30, "png_library\\flecha_abajo2.png", self.frame_compare_parameter)
        self.search_atr_button.configure(borderwidth=4, relief="groove")
        self.search_atr_button.grid(row=11, column=2, columnspan=4)
        self.search_atr_button.bind("<Button-1>", lambda e:[self.atribute_seleted()])
        
        self.atribute_exact = ttk.Button(self.frame_compare_parameter,text = 'Atr Menu', style = 'priamry.Outline.TButton', command= lambda:[self.attribute_menu()])
        self.atribute_exact.grid(row=0, column=6, columnspan=2)

        # self.clear_table = ttk.Button(self.frame_compare_parameter, text='Clear All', style= 'danger.Outline.TButton', command = lambda:[self.clear_all()])
        # self.clear_table.grid(row=12, column=16,columnspan=2)
        self.clear_figure = ttk.Button(self.frame_compare_parameter, text='Clear Figure', style= 'danger.Outline.TButton', command = lambda:[self.axis.cla(),self.canvas_fig.draw()])
        self.clear_figure.grid(row=12, column=16,columnspan=3)

        self.clear_table2 = ttk.Button(self.frame_compare_parameter, text='Clear Table', style= 'danger.Outline.TButton', command = lambda:[self.clear_table()])
        self.clear_table2.grid(row=10, column=16,columnspan=3,rowspan=3)

        self.table_to_csv = ttk.Button(self.frame_compare_parameter, text='Export To CSV', style= 'success.Outline.TButton', command = lambda:[self.export_to_csv()])
        self.table_to_csv.grid(row=11, column=16, columnspan=3,rowspan=3)

        # Prameter Treeview
        self.frame1= Frame(self.frame_compare_parameter)
        self.frame1.grid(row=2, column=4,rowspan=9,columnspan=3,sticky='nswe')
        scroll = Scrollbar(self.frame1)
        scroll.pack(side=RIGHT, fill=Y)

        scrollx = Scrollbar(self.frame1,orient='horizontal')
        scrollx.pack(side= BOTTOM,fill=X)
        
        self.table1=CheckboxTreeview(self.frame1,yscrollcommand=scroll,xscrollcommand=scrollx)
        self.table1.pack(expand=1,fill=Y)
        scroll.config(command=self.table1.yview)
        scrollx.config(command=self.table1.xview)
        self.table1.column("#0", width=250)
        self.table1.heading('#0', text ='Attributes')

        #Ploted parameter frame
        self.frame2= Frame(self.frame_compare_parameter)
        self.frame2.grid(row=12, column=1, columnspan=14, rowspan=2)
        self.scroll = Scrollbar(self.frame2)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.scrollx = Scrollbar(self.frame2,orient='horizontal')
        self.scrollx.pack(side= BOTTOM,fill=X)

        columns = []
        for i in range(100):
            columns.append('c{}'.format(i))
        
        self.table2=ttk.Treeview(self.frame2,columns = columns,yscrollcommand= self.scroll,xscrollcommand= self.scrollx)
        self.table2.pack(expand=1,fill=Y)
        self.scroll.config(command=self.table2.yview)
        self.scrollx.config(command=self.table2.xview)
        self.table2.column("#0", width=1000)
        

        self.search_box_atr = ttk.Entry(self.frame_compare_parameter, style = STYLE_ENTRY)
        self.search_box_atr.grid(row=1, column=4, columnspan=3)
        self.search_button = ttk.Button(self.frame_compare_parameter,text = 'Search Attribute', style = 'priamry.Outline.TButton', command= lambda:[self.sortby_atr(self.search_box_atr.get())])
        self.search_button.grid(row=0, column=4, columnspan=3)

        self.search_box_val = ttk.Entry(self.frame_compare_parameter, style = STYLE_ENTRY)
        self.search_box_val.grid(row=1, column=0, columnspan=4)
        self.search_button_val = ttk.Button(self.frame_compare_parameter,text = 'Search Vehicle', style = 'priamry.Outline.TButton', command= lambda:[self.sortby_val(self.search_box_val.get())])
        self.search_button_val.grid(row=0, column=0, columnspan=4)

        # Table of vehicles 
        self.types = ['Urbos100X']
        self.atr_type = []
        self.frame3= Frame(self.frame_compare_parameter)
        self.frame3.grid(row=2, column=1,rowspan=9, columnspan = 3,sticky='nse')

        scroll = Scrollbar(self.frame3)
        scroll.pack(side=RIGHT, fill=Y)

        scrollx = Scrollbar(self.frame3,orient='horizontal')
        scrollx.pack(side= BOTTOM,fill=X)
        
        self.table3=CheckboxTreeview(self.frame3,yscrollcommand=scroll,xscrollcommand=scrollx)
        self.table3.pack(expand=1,fill=Y)
        scroll.config(command=self.table3.yview)
        scrollx.config(command=self.table3.xview)
        self.table3.column("#0", width=250)
        self.table3.heading('#0',text= 'Projects')

        self.colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","beige","brown","gray","cyan","magenta"])

        self.table_no_empty = True
        self.columns = []
        self.create_fig()
        self.import_parameters()
        self.import_attributes()

    def clear_table(self):
        self.all_columns.clear()
        self.column0.clear()
        self.columns.clear()
        self.units = ''
        self.table_no_empty = True
        self.table2.pack_forget()
        self.scroll.pack_forget()
        self.scrollx.pack_forget()
        self. scroll = Scrollbar(self.frame2)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.scrollx = Scrollbar(self.frame2,orient='horizontal')
        self.scrollx.pack(side= BOTTOM,fill=X)
 
        columns = []
        
        for i in range(len(self.all_columns)):
            columns.append('c{}'.format(i))
          
        self.table2=ttk.Treeview(self.frame2,columns = columns,yscrollcommand= self.scroll,xscrollcommand= self.scrollx)
        self.table2.pack(expand=1,fill=Y)
        self.scroll.config(command=self.table2.yview)
        self.scrollx.config(command=self.table2.xview)
        self.table2.column("#0", width=1400)
        self.table2.bind('<Double-Button-1>', self.selectItem)


    def clear_two_atr(self):
        '''Detect two attribute check, to clear figure'''

        self.x = ttk.Label(self.frame_compare_parameter, text = ' * Select column data to define X axis *')
        self.x.place( x= (0.25*float(self.width)),y=(0.9*float(self.height)))

        self.hold_check.grid_forget()
        self.canvas_fig.draw()

        if self.two_atr.get() is False:
            self.x.place_forget()
            self.hold_check.grid(row=12, column=16, columnspan=3, rowspan=4)
            self.units_to_plot.clear()
            self.title_to_plot.clear()
            
    def attributes_axis(self,table,col):
        '''Select two attribute to plot them'''
        self.figure_data = []
        if self.two_atr.get() is True:
            self.axis.cla()
            self.canvas_fig.draw()

            temp_list= []
            data = [(table.set(child, col), child) for child in table.get_children('')]
            num = (int(str(col[1:])))
            num = num-1
    
            title = self.columns[num]
    
            attributes = self.data_base.attributes
            for atr in attributes:
                lista = list(atr.keys())

                if title in lista:
                    value = atr[title]
                    units = value['units']
            if 'QZ' in title:
                units = 'kN'
    
            # temp_list = [float(i[0]) for i in data]
            for i in data:
                if i[0] == 'N/A':
                     pass
                else:
                    temp_list.append(float(i[0]))

            if len(self.atr_to_plot) <2:
                self.units_to_plot.append(units)
                self.title_to_plot.append(title)
                if len(self.atr_to_plot) == 0:
                    self.x.place_forget()
                    self.y = ttk.Label(self.frame_compare_parameter, text = '* The x-axis has been defined with "{}", now elect column data to define Y axis *'.format(self.title_to_plot[0]))
                    self.y.place( x= (0.25*float(self.width)),y=(0.9*float(self.height)))
                    self.axis.set_xlabel('{} [{}]'.format(self.title_to_plot[0],self.units_to_plot[0]))
                if len(self.atr_to_plot) == 1:
                    self.axis.set_ylabel('{} [{}]'.format(self.title_to_plot[1],self.units_to_plot[1]))

                self.atr_to_plot.append(temp_list)
                self.canvas_fig.draw()

            if len(self.atr_to_plot) == 2:
                self.y.place_forget()
                self.axis.cla()
                self.canvas_fig.draw()

                self.a = np.transpose(self.atr_to_plot)

                self.set_axis()

                def on_pick(event):
                    self.index = event.ind
                    self.val = (self.a[event.ind]).tolist()
                    self.check_on = True
                    self.canvas_fig.draw()
                    self.fig.canvas.mpl_connect("button_press_event", self.position_text)
                    
                self.fig.canvas.mpl_connect('pick_event', on_pick)
                self.canvas_fig.get_tk_widget().pack()
                self.toolbar.update()
                self.canvas_fig.draw()
                self.atr_to_plot.clear() ##### Para poder seguir eligiendo atributos para plotear #####



    def position_text(self,event):
        '''Detect data click to set atr name in the figure'''

        if self.figure_data != []:
            for data in self.figure_data:
                data.set_visible(False)
        self.figure_data.clear()

        if self.check_on is True:

            name = '{}'.format(self.column0[self.index[0]])
            x = float(event.xdata)
            y = float(event.ydata)

            text = self.axis.text(x, y,s=name,size = 7, bbox=dict(boxstyle="round",ec=(1., 0.5, 0.5),fc=(1., 0.8, 0.8)))
            self.figure_data.append(text)
            self.canvas_fig.draw()
            self.check_on = False

        for child in self.table2.get_children():
            lista = self.table2.item(child)['text']
            if self.column0[self.index[0]] in self.table2.item(child)['text']:
               self.table2.selection_set(child)

    def set_axis(self):
        '''Set figure axis and title'''
        markers = ["o", "X", "d", "v", "s", "*", "^", "d", "v", "s", "*", "^","<",">","p","P","h","1","2","3","4"]
        self.axis.cla()

        for xp, yp, m, l in zip(self.a[:,0], self.a[:,1], markers,self.column0):
            self.axis.scatter(xp, yp, marker=m,label=l, s=50)
        self.coll = self.axis.scatter(self.a[:,0], self.a[:,1],color='none', picker = 5,s=40)

        z = np.polyfit(self.a[:,0],self.a[:,1], 1)
        p = np.poly1d(z)
        self.axis.plot(self.a[:,0], p(self.a[:,0]), "r",lw=0.5)
        text = f"$y={z[0]:0.3f}\;x{z[1]:+0.3f}$\n$R^2 = {r2_score(self.a[:,1],p(self.a[:,0])):0.3f}$"
        self.axis.text(0.32, 1.8, text,transform=plt.gca().transAxes,
             fontsize=8, verticalalignment='top')
        self.axis.set_xlabel('{} [{}]'.format(self.title_to_plot[len(self.title_to_plot)-2],self.units_to_plot[len(self.title_to_plot)-2]))
        self.axis.set_ylabel('{} [{}]'.format(self.title_to_plot[len(self.title_to_plot)-1],self.units_to_plot[len(self.title_to_plot)-1]))
        # self.axis.set_title('{} / {}'.format(self.title_to_plot[len(self.title_to_plot)-2],self.title_to_plot[len(self.title_to_plot)-1]))

        self.axis.legend(prop={"size":8},loc='upper center', bbox_to_anchor=(1.16, 1),fancybox=True, shadow=True, ncol=1)
        self.axis.set_axisbelow(True)
        self.axis.grid(color='black', linestyle='dashed',linewidth=0.3)
        self.canvas_fig.draw()


    def attribute_menu(self):
        self.type_element_dict = {'NaN':'','Spring':'SPR', 'Damper':'DMP','Bump Stop': 'BST', 'Lift Stop':'LST','Turn Stop': 'TST','Ball Joint': 'BJ','Traction Link':'TRL','Antiroll Bar': 'AROLL'}
        self.type_element = tuple(self.type_element_dict.keys())
        self.direction_dict = {'NaN':'','Longitudinal':'A','Lateral/Transversal':'T','Vertical':'V'}
        self.direction = tuple(self.direction_dict.keys())
        self.suspension_stage_dict = {'NaN':'','Primary':'1', 'Secondary':'2','Between Carbodies': '3'}
        self.suspension_stage = tuple(self.suspension_stage_dict.keys())
        self.characteristic_dict = {'NaN':'','Stiffness':'K', 'Damping':'C', 'Point':'P', 'Number(Without Direction)':'N', 'Type Number(Without direction)':'TYPE', 'Distance between same type of elements': 'DIST','Slope of the mounting':'SL',
                                'Damping Saturation':'CSAT', 'Friction coefficient of the element':'XNU','Stroke(Full Stroke)':'DF','Air Gap':'D0', 'Point in the bogie 1':'PB1','Point in the carbody 1':'PC1',
                                'Point in the bogie 2':'PB2', 'Point in the carbody 2':'PC2', 'Radial stiffness(for BJ)':'KR','Torsional Stiffness':'KT','COnical Stiffness(for BJ)':'KC'}
        self.characteristic = tuple(self.characteristic_dict.keys())


        # BODIES

        self.body_type_dict = {'NaN':'','Whell':'WHL', 'Wheelset':'WST','Bogie':'BOG', 'Carbody':'CAR'}
        self.body_type = tuple(self.body_type_dict.keys())
        self.body_characteristic_dict ={'NaN':'','Mass 1':'M1', 'Mass 2':'M2', 'Mass 3':'M3', 'Mass 4':'M4', 'Other Mass':'M',' Gravity Center X':'CGX',' Gravity Center Y':'CGY',' Gravity Center Z':'CGZ',
                                   'Inertia X':'IXX', 'Inertia Y':'IYY', 'Inertia Z':'IZZ', 'Profile':'PRFL', 'New Wheel Radius':'R0', 'Worn Wheel Radius':'RW', 'Wheel Base(empate de bogie)':'S',
                                   'Running Gear Distance (Empate de bogie)':'S2', 'Torsional Stifness (for BOG and CAR)':'KT'}
        self.body_characteristic = tuple(self.body_characteristic_dict.keys())
        self.load_condition_dict = {'NaN':'','Working Order Payload':'WOP', 'Normal Payload':'NP', 'Exceptional Payload':'EP'}
        self.load_condition = tuple(self.load_condition_dict.keys())

        self.atr_menu = Toplevel()
        self.atr_menu.geometry('700x500')
        for row_index in range(15):
            self.atr_menu.rowconfigure(row_index, weight=1,minsize=40)
            for col_index in range(20):
                self.atr_menu.columnconfigure(col_index, weight=1,minsize=60)
        
        elementos_btn = ttk.Button(self.atr_menu, text = 'ELEMENTOS DEFORMABLES', style = 'priamry.Outline.TButton', command = lambda:[self.elementos_deformables(elementos_btn, bodies_btn)])
        elementos_btn.grid(row=3, column=1, columnspan = 2)
        bodies_btn = ttk.Button(self.atr_menu, text = 'BODY ATTRIBUTE', style = 'priamry.Outline.TButton', command = lambda:[self.body(elementos_btn, bodies_btn)])
        bodies_btn.grid(row=3, column=4, columnspan = 2)
        self.atr_menu.mainloop()

    def detect_checkbox(self):
        '''Detect hold checkbox, to save current units'''

        if self.units == '':
            Tk.messagebox.showwarning(title = 'Warning' , message = 'Before hold figure, you have to choose the attribute to define units')
            self.hold_var.set(False)
            
        else:
            self.hold_units = self.units

    def option_changed(self,list_var,option):
        if option is 'elementos':
            one = list_var[0].get()
            two = list_var[1].get()
            three = list_var[2].get()
            four = list_var[3].get()

            one = self.type_element_dict[one]
            two = self.direction_dict[two]
            three = self.suspension_stage_dict[three]
            four = self.characteristic_dict[four]
            print(one,'-',two,'-',three,'-',four,)

        if option is 'body':
            one = list_var[0].get()
            two = list_var[1].get()
            three = list_var[2].get()

            one = self.body_type_dict[one]
            two = self.body_characteristic_dict[two]
            three = self.load_condition_dict [three]
            print(one,'-',two,'-',three)

    def elementos_deformables(self,boton1,boton2):
        boton1.destroy()
        boton2.destroy()
        element_type_var = Tk.StringVar()
        element_direction_var = Tk.StringVar()
        element_suspension_var = Tk.StringVar()
        element_characteristic_var = Tk.StringVar()
        list_var = [element_type_var, element_direction_var,element_suspension_var,element_characteristic_var]
        
        menu_type = ttk.OptionMenu(self.atr_menu, element_type_var, self.type_element[0], *self.type_element).grid(row=2, column=2, columnspan=3)
        menu_direction = ttk.OptionMenu(self.atr_menu, element_direction_var, self.direction[0], *self.direction).grid(row=3, column=2, columnspan=3)
        menu_suspension = ttk.OptionMenu(self.atr_menu,element_suspension_var,self.suspension_stage[0],*self.suspension_stage).grid(row=4, column=2, columnspan=3)
        menu_characteristic = ttk.OptionMenu(self.atr_menu, element_characteristic_var, self.characteristic[0], *self.characteristic).grid(row=5, column=2, columnspan=3)
        
        label_type = ttk.Label(self.atr_menu, text = 'ELEMENT TYPE',  font= ('Helvetica', 9,'underline')).grid(row=2, column=1, columnspan=2)
        label_menu = ttk.Label(self.atr_menu, text = 'ELEMENTS MAIN DIRECTION',  font= ('Helvetica', 9,'underline')).grid(row=3, column=1, columnspan=2)
        label_suspension = ttk.Label(self.atr_menu, text = 'SUSPENSION STAGE',  font= ('Helvetica', 9,'underline')).grid(row=4, column=1, columnspan=2)
        label_type = ttk.Label(self.atr_menu, text = 'CHARACTERISTIC',  font= ('Helvetica', 9,'underline')).grid(row=5, column=1, columnspan=2)
        boton = ttk.Button(self.atr_menu, text = 'Select Attribute', command = lambda:[self.option_changed(list_var,'elementos')]).grid(row=6, column=3)
        back_btn = ttk.Button(self.atr_menu, text = 'BACK', command = lambda:[self.atr_menu.destroy()]).grid(row=6, column=4)

    def body(self,boton1, boton2):
        boton1.destroy()
        boton2.destroy()
        body_type_var = Tk.StringVar()
        body_characteristic_var = Tk.StringVar()
        body_load_codi_var = Tk.StringVar()
        list_var = [body_type_var,body_characteristic_var, body_load_codi_var]

        label_type = ttk.Label(self.atr_menu, text = 'BODY TYPE',  font= ('Helvetica', 9,'underline')).grid(row=2, column=1, columnspan=2)
        label_characteristic = ttk.Label(self.atr_menu, text = 'CHARACTERISTIC',  font= ('Helvetica', 9,'underline')).grid(row=3, column=1, columnspan=2)
        label_load_condition = ttk.Label(self.atr_menu, text = 'LOAD CONTITION (FOR CARBODIES)',  font= ('Helvetica', 9,'underline')).grid(row=4, column=1, columnspan=2)    

        menu_body_type = ttk.OptionMenu(self.atr_menu,body_type_var, 'NaN', *self.body_type).grid(row=2, column=2, columnspan=3)
        menu_body_characteristic = ttk.OptionMenu(self.atr_menu, body_characteristic_var, 'NaN', *self.body_characteristic).grid(row=3, column=2, columnspan=3)
        menu_load_condition = ttk.OptionMenu(self.atr_menu, body_load_codi_var, 'NaN', *self.load_condition).grid(row=4, column=2, columnspan=3)
        
        boton = ttk.Button(self.atr_menu, text = 'Select Attribute', command = lambda:[self.option_changed(list_var,'body')]).grid(row=6, column=3)
        back_btn = ttk.Button(self.atr_menu, text = 'BACK', command = lambda:[self.atr_menu.destroy()]).grid(row=6, column=4)

    def sortby_val(self,filt):
        '''Search entry.get() in the treeview'''

        filt = filt.lower()

        for item in self.table3.get_children():
            if filt in (self.table3.item(item)['text']).lower():
                self.table3.change_state(item,'checked')
            else:
                self.table3.item(item, open=True)
                for subitem in self.table3.get_children(item):
                    if filt in (self.table3.item(subitem)['text']).lower():
                        self.table3.change_state(subitem,'checked')
                        self.table3._check_ancestor(subitem)
                        self.table3._check_descendant(subitem)
                    else:
                        self.table3.item(subitem, open=True)
                        for subsubitem in self.table3.get_children(subitem):
                            if filt in (self.table3.item(subsubitem)['text']).lower():
                                self.table3.change_state(subsubitem,'checked')
                                self.table3._check_ancestor(subsubitem)
                                self.table3._check_descendant(subsubitem)
                            else:                  
                                for subsubsubitem in self.table3.get_children(subsubitem):
                                    if filt in (self.table3.item(subsubsubitem)['text']).lower():
                                        self.table3.item(subsubitem, open=True)
                                        self.table3.change_state(subsubsubitem,'checked')
                                        self.table3._check_ancestor(subsubsubitem)
                                        self.table3._check_descendant(subsubsubitem)
                                
    def sortby_atr(self, filt):
        ''' Search your text in all the attributes and in it is descriptions'''

        self.names.clear()
        self.boxes.clear()
        self.checkbox.clear()

        self.i = 1
        filt = filt.lower()
        self.tl = Toplevel(self.frame_compare_parameter)
        self.tl.geometry('470x600')
        self.tl_frame = tools.interface_view_data.ScrollableFrame(self.tl,470,575)
        self.tl_frame.pack()
        check_all = ttk.Button(self.tl_frame.scrollable_frame, text = 'Select All', command = lambda:[self.select_all_checkbox()])
        check_all.grid(row=0, column=1)

        for item in self.table1.get_children():
            if self.filter_description(filt,(self.table1.item(item)['text'])):
                self.i = self.i+1
                self.table1.change_state(item,'checked')
            else:
                self.table1.item(item, open=True)
                for subitem in self.table1.get_children(item):
                    if self.filter_description(filt,(self.table1.item(subitem)['text'])):
                        self.i = self.i+1
                        pass
                    else:
                        self.table1.item(subitem, open=True)
                        for subsubitem in self.table1.get_children(subitem):
                            if self.filter_description(filt,(self.table1.item(subsubitem)['text'])):
                                self.i = self.i+1
                                pass
                            else:
                                for subsubsubitem in self.table1.get_children(subsubitem):
                                    if self.filter_description(filt,(self.table1.item(subsubsubitem)['text'])):
                                        self.i = self.i+1
                                        pass

        self.check_atr = self.import_image(70, 40, "png_library\\flecha_abajo2.png", self.tl_frame.scrollable_frame)
        self.check_atr.configure(borderwidth=4, relief="groove")
        self.check_atr.grid(row=self.i+1, column=1)
        self.check_atr.bind("<Button-1>", lambda e:[self.check_attributes(),self.atribute_seleted(), self.tl.destroy()])

    def select_all_checkbox(self):
        '''Check all the attributes'''

        for box in self.checkbox:
            box.select()

    def check_attributes(self):
        '''Detect the selected checkbox, to plot all in the table with its values'''

        for box in self.boxes:
             if box.get():
                 name = self.names[self.boxes.index(box)]
                 name = (name.split('-'))[0]

                 for item in self.table1.get_children():
                     if name == self.table1.item(item)['text']:
                         self.table1.change_state(item, 'checked')

                     else:
                         self.table1.item(item, open = True)
                         for subitem in self.table1.get_children(item):
                             if name == self.table1.item(subitem)['text']:
                                 self.table1.change_state(subitem, 'checked')


                             else:
                                 self.table1.item(subitem, open= True)
                                 for subsubitem in self.table1.get_children(subitem):
                                     if name == self.table1.item(subsubitem)['text']:
                                         self.table1.change_state(subsubitem, 'checked')


                                     else:
                                         for subsubsubitem in self.table1.get_children(subsubitem):
                                             if name == self.table1.item(subsubsubitem)['text']:
                                                 self.table1.change_state(subsubsubitem, 'checked')
                                                 self.table1._check_ancestor(subsubsubitem)

    def filter_description(self, filt, name):
        ''' Search entry text in all the attributes names and descritions'''

        filt = filt.lower()
        bogie = tools.class_bogie.Bogie('b',self.data_base.attributes[1])
        car = tools.class_carbody.Carbody('c',self.data_base.attributes[2])
        link = tools.class_carbody_links.CarbodyLinks('d',self.data_base.attributes[3])
        real_bogie = tools.class_real_bogie.RealBogie('a','a','e')
        validate = False
        

        if hasattr(bogie, name):
            text = (getattr(bogie, name))['Description']
            if filt in (str(text)).lower():
                atr_name = '{}'.format(name)
                if atr_name not in self.names:
                    variab = Tk.BooleanVar(self.tl_frame.scrollable_frame)

                    check = Checkbutton(self.tl_frame.scrollable_frame, text = '{}-{}'.format(name,text), variable = variab )
                    check.grid(row=self.i, column=1,columnspan=3, sticky = W)
                    self.boxes.append(variab)
                    self.checkbox.append(check)

                    self.names.append(atr_name)
                    validate = True

            if filt in name.lower():
                text = (getattr(bogie, name))['Description']
                variab = Tk.BooleanVar(self.tl_frame.scrollable_frame)
                atr_name = '{}'.format(name)

                if atr_name not in self.names:
                    check = Checkbutton(self.tl_frame.scrollable_frame, text = '{}-{}'.format(name,text), variable = variab )
                    check.grid(row=self.i, column=1,columnspan=3,sticky = W)
                    self.boxes.append(variab)
                    self.checkbox.append(check)
                    
                    self.names.append(atr_name)
                    self.i = self.i +1

        elif hasattr(car, name):
            text = (getattr(car, name))['Description']
            if filt in (str(text)).lower():
                atr_name = '{}'.format(name)
                if atr_name not in self.names:
                    variab = Tk.BooleanVar(self.tl_frame.scrollable_frame)
    
                    check = Checkbutton(self.tl_frame.scrollable_frame, text = '{}-{}'.format(name,text), variable = variab )
                    check.grid(row=self.i, column=1,columnspan=3, sticky = W)
                    self.boxes.append(variab)
                    self.checkbox.append(check)
                    
                    self.names.append(atr_name)
                    validate = True

            if filt in name.lower():
                text = (getattr(car, name))['Description']
                variab = Tk.BooleanVar(self.tl_frame.scrollable_frame)
                atr_name = '{}'.format(name)

                if atr_name not in self.names:
                    check = Checkbutton(self.tl_frame.scrollable_frame, text = '{}'.format(name), variable = variab )
                    check.grid(row=self.i, column=1,columnspan=3,sticky = W)
                    self.boxes.append(variab)
                    self.checkbox.append(check)
                    
                    self.names.append(atr_name)
                    self.i = self.i +1

        elif hasattr(link, name):
            text = (getattr(link, name))['Description']
            if filt in (str(text)).lower():
                atr_name = '{}'.format(name)
                if atr_name not in self.names:
                    variab = Tk.BooleanVar(self.tl_frame.scrollable_frame)
    
                    check = Checkbutton(self.tl_frame.scrollable_frame, text = '{}-{}'.format(name,text), variable = variab )
                    check.grid(row=self.i, column=1,columnspan=3,sticky = W)
                    self.boxes.append(variab)
                    self.checkbox.append(check)
                    atr_name = '{}'.format(name)
                    self.names.append(atr_name)
                    validate = True

            if filt in name.lower():
                text = (getattr(link, name))['Description']
                variab = Tk.BooleanVar(self.tl_frame.scrollable_frame)
                atr_name = '{}'.format(name)

                if atr_name not in self.names:
                    check = Checkbutton(self.tl_frame.scrollable_frame, text = '{}'.format(name), variable = variab )
                    check.grid(row=self.i, column=1,columnspan=3,sticky = W)
                    self.boxes.append(variab)
                    self.checkbox.append(check)
                    
                    self.names.append(atr_name)
                    self.i = self.i +1

        elif hasattr(real_bogie, name):
            text = (getattr(real_bogie, name))
            if filt in (str(text)).lower():
                atr_name = '{}'.format(name)
                if atr_name not in self.names:
                    variab = Tk.BooleanVar(self.tl_frame.scrollable_frame)
    
                    check = Checkbutton(self.tl_frame.scrollable_frame, text = '{}-{}'.format(name,text), variable = variab )
                    check.grid(row=self.i, column=1,columnspan=3,sticky = W)
                    self.boxes.append(variab)
                    self.checkbox.append(check)
                    atr_name = '{}'.format(name)
                    self.names.append(atr_name)
                    validate = True

            if filt in name.lower():
                text = (getattr(real_bogie, name))
                variab = Tk.BooleanVar(self.tl_frame.scrollable_frame)
                atr_name = '{}'.format(name)

                if atr_name not in self.names:
                    check = Checkbutton(self.tl_frame.scrollable_frame, text = '{}'.format(name), variable = variab )
                    check.grid(row=self.i, column=1,columnspan=3,sticky = W)
                    self.boxes.append(variab)
                    self.checkbox.append(check)
                    
                    self.names.append(atr_name)
                    self.i = self.i +1

        return validate
        
    def create_fig(self):
        ''' Create figure in the frame to bar,scatter,line plots'''

        self.frame4= Frame(self.frame_compare_parameter)
        self.frame4.grid(row=0, column=8,rowspan=11,columnspan=13,sticky='nswe')
       
        self.fig = Figure(figsize=(11,6), dpi=100) 
        gs = self.fig.add_gridspec(nrows=1, ncols=6, left=0.05, right=0.75,
                      hspace=0.1, wspace=0.05)
        self.axis = self.fig.add_subplot(gs[-1,1:6])

        self.canvas_fig = FigureCanvasTkAgg(self.fig, master = self.frame4)
        # self.fig.patch.set_facecolor('blue')
        self.canvas_fig.draw()

        self.annot = self.axis.annotate("", xy=(0,0), xytext=(-10.0,-20.0),textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="white", alpha=0.6))
        self.canvas_fig.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas_fig,self.frame_compare_parameter,pack_toolbar=False)
        self.toolbar.place( x= (0.61*float(self.width)),y=(0.576*float(self.height)))
        self.axis.set_axisbelow(True)
        self.axis.grid(color='black', linestyle='dashed',linewidth=0.3)
        self.canvas_fig.draw()
        self.canvas_fig.get_tk_widget().pack()

        mplcursors.cursor(self.fig)

    def export_to_csv(self):
        '''Export table values to excel to continue working with selected data'''

        archivo=fd.asksaveasfilename(filetype=(('xls files','*xls*'),('All files','*.*')))
        archivo = archivo + '.xlsx'
        graph_sheet = []
        row_list = []
        sheet_names = []
        columns = self.columns
        i=0
        for row in self.table2.get_children():
            values = self.table2.item(row)["values"]
            for value in values:
                if type(value) is str:
                    name = self.column0[i]
                    name_v = (name).split('/')[0]
                    name_o = (name).split('/')[1]
                    vehicle = self.data_base.vehicle[self.data_base.name_list.index(name_v)]
                    if value in vehicle.sheet:
                        index= values.index(value)
                        if name_o in vehicle.BOGIE_CONFIG['value']:
                            bogie = vehicle.bogie[vehicle.BOGIE_CONFIG['value'].index(name_o)]
                            atr = getattr(bogie, self.columns[index])

                        elif name_o in vehicle.CARBODY_CONFIG['value']:
                            carbody = vehicle.carbody[vehicle.CARBODY_CONFIG['value'].index(name_o)]
                            atr = getattr(carbody, self.columns[index])


                        elif name_o in vehicle.carbody_links_names:
                            link = vehicle.carbody_links[vehicle.carbody_links_names.index(name_o)]
                            atr = getattr(link, self.columns[index])

                        dic = atr['value']
                        lista = list(dic.values())
                        col_index = [lista[1],lista[2]]
                        df = pd.DataFrame(lista[0], index =None, columns = col_index)
                        graph_sheet.append(df)
                        sheet_names.append((list(dic.keys()))[0])

            i=i+1
            row_list.append(values)


        treeview_df = pd.DataFrame(row_list, columns = columns, index = self.column0)
        graph_sheet.insert(0,treeview_df)
        sheet_names.insert(0,'Main')
        Excelwriter = pd.ExcelWriter(archivo, engine="xlsxwriter")

        for i,df in enumerate(graph_sheet):
            df.to_excel(Excelwriter,sheet_name='{}'.format(sheet_names[i]),index=self.column0)

        Excelwriter.save()

    def plot_column(self,tree, col):
        ''' Method to take columns values, to plot them'''

        self.attributes_axis(tree, col)

        if self.two_atr.get() is True:
            pass
        else:
            x=''
            ylabel=''
            numpy_detect = False

            values = []
            data = [(tree.set(child, col), child) for child in tree.get_children('')]
            num = (int(str(col[1:])))
            num = num-1
    
            title = self.columns[num]
    
            attributes = self.data_base.attributes
            for atr in attributes:
                lista = list(atr.keys())
                if title in lista:
                    value = atr[title]
                    units = value['units']
                    self.units = units

                elif 'QZ' in title:
                    self.units = 'kN'

            if self.hold_var.get() is False:
                self.ploted_bars.clear()
                self.ploted_bars.append(title)
                self.plot_to_bar(data,values,title,numpy_detect, ylabel)
            else:

                if (self.units == self.hold_units):
                    if title not in self.ploted_bars:
                        self.ploted_bars.append(title)
                        self.plot_to_bar(data,values,title,numpy_detect, ylabel)

    def plot_to_bar (self, data,values,title, numpy_detect, ylabel):
        ''' Data to figure'''

        string_detect = False
        numpy_detect = False

        for tuples in data:
            values.append((tuples[0]))

        for val in values:
            try:
                if val == 'N/A':
                    pass
                else:
                    float(val)
            except:
                string_detect = True

        if string_detect is True:
            i=0
            for val in values:
                name = (self.column0[i].split('/'))[0]
                self.train = self.data_base.vehicle[self.data_base.name_list.index(name)]
                sheet = self.train.sheet 
                if val in sheet:
                    numpy_detect = True
                i=i+1

        if (string_detect is False) & (numpy_detect is False):
            values = []
            for tuples in data:
                if 'N/A' in tuples[0]:
                    pass
                else:
                    values.append(float(tuples[0]))
    
            if self.hold_var.get() is False:
                self.multiple_ylabel =  title
                self.axis.cla()
                self.canvas_fig.draw()
                zip_iter = zip(self.column0,values)
                dict_ = dict(zip_iter)
                self.df = pd.DataFrame(dict_,index=['{}'.format(title)])
                
            else:
                self.multiple_ylabel = self.multiple_ylabel + ' / ' + title
                self.axis.cla()
                self.canvas_fig.draw()
                zip_iter = zip(self.column0,values)
                dict_ = dict(zip_iter)
                df = pd.DataFrame(dict_,index=['{}'.format(title)])
                df_new = self.df.append(df)
                self.df = df_new

            self.df.plot(kind='bar',ax=self.axis, edgecolor='white', linewidth=2, width=0.8)  

            plt.setp(self.axis.get_xticklabels(), rotation=0)
        
            self.legend = self.axis.legend(prop={"size":8},loc='upper center', bbox_to_anchor=(1.16, 1),fancybox=True, shadow=True, ncol=1)
    
            self.train = self.data_base.vehicle[self.data_base.name_list.index((self.column0[0].split('/'))[0])]
            objec = (self.column0[0].split('/'))[1]

            if objec in self.train.BOGIE_CONFIG['value']:
                self.new_bogie = self.train.bogie[self.train.BOGIE_CONFIG['value'].index(objec)]
                if hasattr(self.new_bogie, title):
                    atr = getattr(self.new_bogie,title)
                    ylabel = atr['units']
                    

            elif objec in self.train.CARBODY_CONFIG['value']:
                self.new_carbody = self.train.carbody[self.train.CARBODY_CONFIG['value'].index(objec)]
                if hasattr(self.new_carbody, title):
                    atr = getattr(self.new_carbody,title)
                    ylabel = atr['units']
     
            elif objec  in self.train.carbody_links_names:
                self.new_link = self.train.carbody_links_names[self.train.carbody_links_names.index(objec)]
                if hasattr(self.new_link, title):
                    atr = getattr(self.new_link,title)
                    ylabel = atr['units']

            elif objec in self.train.TRAIN_CONFIG['value']:
                index = self.train.TRAIN_CONFIG['value'].index(objec)
                bogie = self.train.bogie[index]
                if hasattr(bogie, title):
                    atr = getattr(bogie,title)
                    ylabel = atr['units']

            self.axis.text(-0.15, 0.63, '{} [{}]'.format(self.multiple_ylabel,ylabel), transform=self.axis.transAxes, fontsize=10, verticalalignment='top',rotation=90)

        if numpy_detect  is True:
          self.axis.cla()
          self.axis.set_axisbelow(True)
          self.axis.grid(color='black', linestyle='dashed',linewidth=0.3)
          self.canvas_fig.draw()
          i=0
          for val in values:
              name = (self.column0[i].split('/'))[0]
              self.train = self.data_base.vehicle[self.data_base.name_list.index(name)]
              sheet = self.train.sheet 
              if val in sheet:
                  name2 = ((self.column0[i]).split('/'))[1]

                  if name2 in self.train.BOGIE_CONFIG['value']:
                      self.new_bogie = self.train.bogie[self.train.BOGIE_CONFIG['value'].index(name2)]
                      objec = self.new_bogie
                  elif name2 in self.train.carbody_links_names:
                      self.new_link = self.train.carbody_links[self.train.carbody_links_names.index(name2)]
                      objec = self.new_link
                  elif name2 in self.train.TRAIN_CONFIG['value']:
                      real_bogie = self.train.real_bogie[self.train.TRAIN_CONFIG['value'].index(name2)]
                      objec = getattr(real_bogie, 'bogie_object')
  
                  atr_dict = getattr(objec,title)
                  array = atr_dict['value']

                  if type(array) is dict:
                      array_val = array['{}'.format(val)]
                      self.plt, = self.axis.plot(array_val[:,1],array_val[:,0],label = self.column0[i])
                      self.legend = self.axis.legend(prop={"size":8},loc='upper center', bbox_to_anchor=(1.16, 1),fancybox=True, shadow=True, ncol=1)
                      self.axis.set_title('{}'.format(title))
                      y=array['y']
                      x=array['x']
                      self.axis.set_ylabel('{}'.format(y))
                      self.axis.set_xlabel('{}'.format(x))
                      self.canvas_fig.draw()
                      self.toolbar.update()

              elif type(array) is str:
                  pass

              i=i+1
        if (numpy_detect is False) & (string_detect is True):
            Tk.messagebox.showinfo(title = 'Information' , message = 'You can not graph Strings')

        self.canvas_fig.draw()
        self.toolbar.update()

    def clear_all(self):
        '''Clear the figure'''

        for item in self.table1.get_children():
            self.table1._uncheck_ancestor(item)
            self.table1._uncheck_descendant(item)
            self.table1.collapse_all()

        for item in self.table3.get_children():
            self.table3._uncheck_ancestor(item)
            self.table3._uncheck_descendant(item)
            self.table3.collapse_all()

        self.search_box_val.delete(0, END)
        self.search_box_atr.delete(0, END)

        for col in self.table2['columns']:
            self.table2.heading(col, text = '')


        self.values.clear()
        self.axis.cla()
        self.canvas_fig.get_tk_widget().pack_forget()
        self.create_fig()
        self.column0.clear()
        self.columns.clear()
        self.names.clear()
        self.checkbox.clear()
        self.boxes.clear()
        self.ploted_bars.clear()

        self.i =0
        
        for i in self.table2.get_children():
            self.table2.delete(i)

    def import_attributes(self):    ########## IMPORTAR VEHICULOS Y SUS PARTES####################
        '''Import vehicle attributes to the treeview'''

        vehicles = self.data_base.vehicle

        for typ in self.types:
            atr = self.table3.insert('',END,text = '{}'.format(typ))
            self.atr_type.append(atr)

        for vehicle in vehicles:
            vehicle_name = self.data_base.name_list[vehicles.index(vehicle)]
            if hasattr(vehicle, 'VEHICLE_TYPE'):
                value = getattr(vehicle,'VEHICLE_TYPE')['value']
                atr = self.atr_type[self.types.index(value)]
                atr2 = self.table3.insert(atr,END,text = '{}'.format(vehicle_name), value=value)
                atr3 = self.table3.insert(atr2, END, text = 'Bogies')
                atr4 = self.table3.insert(atr2, END, text = 'Carbodies')
                atr5 = self.table3.insert(atr2, END, text = 'Carbody Links')
                atr6 = self.table3.insert(atr2, END, text = 'Track')

            # for bogie in vehicle.BOGIE_CONFIG['value']:
            #     self.table3.insert(atr3,END,text = '{}'.format(bogie))
            for carbody in vehicle.CARBODY_CONFIG['value']:
                self.table3.insert(atr4, END, text = '{}'.format(carbody))
            for link in vehicle.carbody_links_names:
                self.table3.insert(atr5,END, text = '{}'.format(link))
            i=0
            for real_bogie  in vehicle.TRAIN_CONFIG['value']:
                if (i!=0) & (vehicle.TRAIN_CONFIG['value'][i] == vehicle.TRAIN_CONFIG['value'][i-1]):
                    real_bogie = real_bogie + '-2'
                self.table3.insert(atr3, END, text = '{}'.format(real_bogie))
                i=i+1

    def atribute_seleted(self):
        '''Method to move attribute values to table'''

        if self.table_no_empty:
            self.table2_values = []
            self.table2_columns = []
            # self.columns = []
            rows = []
            # self.clear_all()
            
            for col in self.table2['columns']:
                self.table2.heading(col, text = '')
            for item in self.table2.get_children():
               self.table2.delete(item)
            
            vehicles = self.table3.get_checked()
            atributes = self.table1.get_checked()
            for atr in atributes:
                self.all_columns.append(atr)

            self.table2.pack_forget()
            columns = []

            while len(self.all_columns) < 12:
                self.all_columns.append('a')

            if len(self.all_columns) > 12:
                for index,col in enumerate(self.all_columns):
                    if col == 'a':
                        self.all_columns.pop(index)

            for i in range(len(self.all_columns)):
                columns.append('c{}'.format(i))
                
            self.table2=ttk.Treeview(self.frame2,columns = columns,yscrollcommand= self.scroll,xscrollcommand= self.scrollx)
            self.table2.pack(expand=1,fill=Y)
            self.scroll.config(command=self.table2.yview)
            self.scrollx.config(command=self.table2.xview)
            self.table2.column("#0", width=200)

            self.i =1
    
            self.table2.bind('<Double-Button-1>', self.selectItem)

            for vehicle in vehicles:
                part = self.table3.item(vehicle)['text']
                parent = self.table3.item(self.table3.parent(self.table3.parent(vehicle)))
                name_vehicle = parent['text']
    
                if name_vehicle in self.types: #### Proteccion de plotear el track ####
                    name_vehicle = self.table3.item(self.table3.parent(vehicle))
                    name_vehicle = name_vehicle['text']
    
                row_name = '{}/{}'.format(name_vehicle,part)
                values = []
    
                for atr in atributes:
                    
                    if row_name not in rows:
                        rows.append(row_name)
                        if row_name not in self.column0:
                            self.column0.append(row_name)

                    col_atr = self.table1.item(atr)['text']
                    if col_atr not in  self.columns:
                        units = self.search_units(col_atr)
                        self.table2.column('#{}'.format(self.i), width = 120, anchor=CENTER,stretch=True)
                        self.table2.heading('#{}'.format(self.i), text = '{} [{}]'.format(col_atr,units),command=lambda c='# {}'.format(self.i): self.plot_column(self.table2, c))
                        self.i = self.i+1
                        self.columns.append(col_atr)

            for row in rows:
                values = []
                for col in  self.columns:
                    name = (row.split('/'))[-1]
                    name2 = name
                    if '-' in name:
                        name = name.split('-')[0]
                    name_vehicle = (row.split('/'))[0]
    
                    self.train = self.data_base.vehicle[self.data_base.name_list.index(name_vehicle)]
    
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
    
                self.table2.insert('', END, values = values, text = '{}'.format(row))
                self.table2_values.append(values)
                self.table_no_empty = False
                self.checkbox.clear()
            self.table2_columns = self.columns
        else:
            self.add_data_table(self.table2_values, self.table2_columns)

    def add_data_table(self,values,columns):

        column0 = deepcopy(self.column0)
        columns = deepcopy(self.columns)
        all_col = deepcopy(self.all_columns)
        self.clear_table()
        self.all_columns = all_col
        self.column0 = column0
        self.columns = columns
        self.table_no_empty= False

        attributes = self.table1.get_checked()
        vehicles = self.table3.get_checked()
        for vehicle in vehicles:
            new_vehicle = False
            name_project =(self.table3.item(self.table3.parent(self.table3.parent(vehicle))))['text']
            name_part = self.table3.item(vehicle)['text']
            name_group = name_project + '/' + name_part

            if name_group not in self.column0:
                self.column0.append(name_group)
                new_vehicle = True

            if new_vehicle is True:
                ret_values = self.search_atr_database(name_project, self.columns, name_part)
                values.append(ret_values)

            for atr in attributes:
                new_atr = False
                item = (self.table1.item(atr))['text']
                if item not in self.columns:
                    new_atr = True
                    self.columns.append(item)
                    self.all_columns.append(item)

        if len(self.all_columns) > 12:
            for index,col in enumerate(self.all_columns):
                if col == 'a':
                    self.all_columns.pop(index)
        values= []      
        self.table2.column("#0", width=200)
        columns = []
        for i in range(len(self.all_columns)):
            columns.append('c{}'.format(i))
        self.table2['columns'] = columns

        for name_group in self.column0:
            name_project = (name_group.split('/'))[0]
            name_part =  (name_group.split('/'))[-1]

            ret_val = self.search_atr_database(name_project, self.columns, name_part)
            values.append(ret_val)
                    
        for index,col in enumerate(self.columns):

            units = self.search_units(col)
            self.table2.column('# {}'.format(index+1), width = 120, anchor=CENTER,stretch=True)
            self.table2.heading('# {}'.format(index+1), text = '{} [{}]'.format(col,units),command=lambda c='# {}'.format(index+1): self.plot_column(self.table2, c))

        for index,val in enumerate(values):
            self.table2.insert('', END, values = val, text = '{}'.format(self.column0[index]))


    def selectItem(self,event):
        '''Create canvas to write attribute values there'''

        train_config  = False 
        if self.list_canvas !=[]:
            for canv in self.list_canvas:
                canv.place_forget()

        curItem = self.table2.item(self.table2.focus())
        col = (self.table2.identify_column(event.x))
        col = col.replace('#','')

        try:
            value = curItem['values'][int(col)-1]
            text = curItem['text']
            column = self.columns[int(col)-1]

            vehicle = (text.split('/'))[0]
            part = (text.split('/'))[1]

            self.train = self.data_base.vehicle[self.data_base.name_list.index(vehicle)]
            if '-' in part:
                part = part.split('-')[0]
            if part in self.train.BOGIE_CONFIG['value']:
                object_ = self.train.bogie[self.train.BOGIE_CONFIG['value'].index(part)]

            elif part in self.train.CARBODY_CONFIG['value']:
                object_ = self.train.carbody[self.train.CARBODY_CONFIG['value'].index(part)]

            elif part in self.train.carbody_links_names:
                object_ = self.train.carbody_links[self.train.carbody_links_names.index(part)]

            elif part in self.train.TRAIN_CONFIG['value']:
                object_ = self.train.real_bogie[self.train.TRAIN_CONFIG['value'].index(part)]
                train_config = True
            elif part == 'Track':
                object_ = self.train.track[0]
                train_config = True

            if train_config is True:
                try:
                    atr_value = getattr(object_, column)
                except(AttributeError):
                    object_ = object_.bogie_object
                    atr_value = getattr(object_, column)
            else:
                atr_value = getattr(object_, column)

            self.canvas = Canvas(self.frame_compare_parameter, width=400, height=400, bg="white")
            self.list_canvas.append(self.canvas)

            self.x = (0.75*float(self.width))
            self.y = (0.36*float(self.height))
            self.canvas.place( x=self.x ,y=self.y)
            frame = Frame(self.canvas,bg="ivory2",highlightbackground="black", highlightthickness=1)
            frame.configure(width=400,height=400)

            frame.bind("<B1-Motion>", self.move)
            frame.grid(row=0, column=0, sticky=N+S+E+W)

            frame.pack()

            label2 = self.import_image(16, 16, "png_library\\cerrar.png", frame)
            label2.configure(bg="ivory2")
            # label2.place( x= (0.87*300),y=(0.01*200))
            label2.bind("<Button-1>", lambda e: self.canvas.place_forget())

            name = '{} / {} / {}'.format(vehicle,part,column)
            lbl1 = Label(frame, text = '{}'.format(name),bg="ivory2",font= ('Helvetica', 10, "bold",'underline')).grid(row=0, column=0, columnspan=2)

            values = list(atr_value.values())
            keys= list(atr_value.keys())
            i=1
            for val in values:
                if str(val) == 'nan':
                    pass
                else:
                    index = values.index(val)
                    Label(frame, text = '{}'.format(keys[index]) + ': ',bg="ivory2").grid(row=i, column=0, sticky = 'w')
                    Label(frame, text = '"' + str(val) + '"',bg="ivory2").grid(row=i, column=1, sticky = 'w')
                    i=i+1
            label2.grid(row=0, column=2)
        except IndexError:
            pass

    def move(self,e):
        x=0
        y=0
        if int(e.x) <-10:
            x=-5
            y=0
            pass
        elif int(e.x)>10:
            x = 5
            y = 0
        elif int(e.y)<-10:
            x = 0
            y = -5
        elif int(e.y)>10:
            x = 0
            y = 5
        
        self.x = self.x +x
        self.y = self.y+y
        self.canvas.place_forget()
        # time.sleep(0.0000001)
        self.canvas.place(x=self.x, y=self.y)

    def import_parameters(self): ############### IMPORTAR ATRIBUTOS DE TODO EL VEHICULO###############
        '''Import vehicles to the vehicle treeview'''

        self.i=0
        names= self.data_base.name_list
        self.table1.selection_clear()
        self.list_blocks_names =  []
        self.blocks = []

        item1 = self.table1.insert('',END,text='Vehicle')

        self.train = tools.class_vehicle.Vehicle('a',{})
        vehicle_atr = list(self.train.__dict__.keys())
        vehicle_atr = [e for e in vehicle_atr if e not in ('bogie_config','carbody_config','sheet','carbody_links_names','excel','name')]

        for atr in vehicle_atr:
            item2 = self.table1.insert(item1,END, text='{}'.format(atr))
            if atr == 'carbody_links':
                 self.links = tools.class_carbody_links.CarbodyLinks('p',self.data_base.attributes[3])
                 atr_dict = list(self.links.__dict__.keys())
                 objec = self.links

            elif atr == 'carbody':
                 self.carbody = tools.class_carbody.Carbody('f',self.data_base.attributes[2])
                 atr_dict = list(self.carbody.__dict__.keys())
                 objec = self.carbody

            elif atr == 'bogie':
                 self.bogie = tools.class_bogie.Bogie('u',self.data_base.attributes[1])
                 atr_dict = list(self.bogie.__dict__.keys())
                 objec = self.bogie

            elif atr == 'real_bogie':
                 self.table1.delete(item2)
                 self.real_bogie = tools.class_real_bogie.RealBogie('gf','fg','u')
                 atr_dict = list(self.real_bogie.__dict__.keys())
                 objec = self.real_bogie

            elif atr == 'track':
                self.track = tools.class_track.Track(self.data_base.attributes[4])
                atr_dict = list(self.track.__dict__.keys())
                objec = self.track

            else:
                atr_dict = []

            for atr in atr_dict:
                value = getattr(objec, atr)

                if type(value) is dict:
                    block = value['block']
                    if block not in self.list_blocks_names:
                        self.bogie_item = item2
                        item3 = self.table1.insert(item2, END,text = '{}'.format(block))
                        self.list_blocks_names.append(block)
                        self.blocks.append(item3)

                    if block in self.list_blocks_names:
                        index = self.list_blocks_names.index(block)
                        item  = self.blocks[index]
                        self.table1.insert(item,END,text = '{}'.format(atr))

                elif type(value) is float:
                    block = 'Loads'
                    if block not in self.list_blocks_names:              
                        item3 = self.table1.insert(self.bogie_item, END,text = '{}'.format(block))
                        self.list_blocks_names.append(block)
                        self.blocks.append(item3)

                    if block in self.list_blocks_names:
                        self.table1.insert(item3,END,text = '{}'.format(atr))
                    
                    
                    
                    
                    
                    
                    
                    