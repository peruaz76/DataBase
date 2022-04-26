# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:39:14 2022

@author: Peru _Alana
"""

from tkinter import ttk, END, Label
from tkinter import Frame,W, E, S, N, Entry, Scrollbar,RIGHT,Y, Canvas
from tkinter import filedialog as fd
import pandas as pd
import tkinter as tk
from copy import deepcopy

import tools.interface_add
import tools.interface_base


class ScrollableFrame(ttk.Frame,tools.interface_base.Base_interface):
    """
    class ScrollableFrame:
        
    """
    def __init__(self, container,width,height):
        super().__init__(container)
        canvas = Canvas(self,width=width, height=height)
        # canvas.configure(bg= 'blue')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollx = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)


        self.scrollable_frame = ttk.Frame(canvas)
        for row_index in range(60):
            self.scrollable_frame.rowconfigure(row_index, weight=1,minsize=25)
            for col_index in range(40):
                self.scrollable_frame.columnconfigure(col_index, weight=1,minsize=25)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((100, 100), window=self.scrollable_frame,anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand = scrollx.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(fill="both",expand=True)
        scrollx.pack(side ='bottom', fill = 'x')


class ViewAnyData(tools.interface_base.Base_interface):
    """
    class ViewAnyData:
        Window to see all the vehicle values imported before

    Properties
    ----------
    tabs: list
        This list has been initialied to save creted tabs for the notebook

    Methods
    -------
    create_widgets(self):
    create_sheets(self):
    compare_nan(self,value):
    insert_data (self):
    carbody_data(self):
    bogie_data(self):
    import_data(self,tab_index,keys,dicti):
    button_to_graph(self,btn_name,values,all_data):
    carbody_links_data(self):
    hide_tabs(self):

    """
    def __init__(self, master,data_base,vehicle_name, admin):
        super().__init__(master)

        # Call to Base interface to crate new frame
        self.frame_view_data = self.new_frame('View Any Data')

        self.frame_view_data.tkraise()

        self.data_base = data_base
        self.vehicle_name = vehicle_name
        self.tabs = []
        self.font_title =('Helvetica', 11, "bold",'underline')
        self.admin = admin
        self.create_widgets()

    def create_widgets(self):
        '''General widgets to the frame'''

        self.sheet = ttk.Notebook(self.frame_view_data, style='TNotebook',width=1900, height=1000)
        self.sheet.grid(row=0 ,column=0, columnspan=20, rowspan=15)
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', background="OliveDrab1")
        self.create_sheets()

    def create_sheets(self):
        '''Create notebook sheets, and general widgets for each sheet'''

        self.train = self.data_base.vehicle[self.data_base.name_list.index(self.vehicle_name)]
        tabs = self.train.sheet
        
        for tab in tabs:
            bogies= Frame(self.sheet)
            bogies.grid(row=0, column=0, sticky=N+S+E+W)
            for row_index in range(30):
                bogies.rowconfigure(row_index, weight=1,minsize=25)
                for col_index in range(20):
                    bogies.columnconfigure(col_index, weight=1,minsize=25)

            self.menu= ttk.Button(bogies, text = 'Main Menu', style='secondary.TButton',
                                   command = lambda:[self.frame_view_data.pack_forget(),
                                                     tools.interface_add.WindowMain(self.master,
                                                                                self.data_base, self.admin)])
            self.menu.place( x= (0.02*float(self.width)),y=(0.86*float(self.height)))

            self.close = ttk.Button(bogies, text = 'EXIT',
                                    style='danger.TButton',
                                    command = lambda:[self.master.destroy()])
            self.close.place( x= (0.96*float(self.width)),y=(0.86*float(self.height)))

            label2 = self.import_image(150, 60, "png_library\\caf_id.png", bogies)
            label2.place( x= (0.9*float(self.width)),y=(0.01*float(self.height)))

            excel = ttk.Button(bogies,text = 'Data To Excel',
                                style='success.Outline.TButton',
                                command= lambda:[self.data_to_excel(self.train)])
            excel.place( x= (0.08*float(self.width)),y=(0.86*float(self.height)))

            self.tabs.append(bogies)
            self.sheet.add(bogies, text = '{}'.format(str(tab)))

        self.hide_tabs()
        self.insert_data()
        self.carbody_links_data()
        opt = tk.StringVar()

        self.wheeload_values('a',opt)

    def compare_nan(self,value):
        '''Comapare if the attribute value is NaN'''
        if type(value) is float:
            value = round(value,1)
        if str(value) == 'nan':
            value = ' '
        return value

    def insert_data (self):

        '''Import vehicle general data to the first notebook sheet'''
        tab_index = self.train.sheet.index('LOADS')
        tab = self.tabs[tab_index]

        options = ['Wheel Load', 'Primary Load', 'Secondary Load']
        QZ012 = tk.StringVar()
 
        s = ttk.Style()
        s.configure("option1.TMenubutton", background="royal blue", foreground = 'white')
 
        mass_options = ttk.OptionMenu(tab, QZ012, options[0], *options,style = 'option1.TMenubutton', command=lambda evt :[ self.wheeload_values(evt, QZ012)])
        mass_options.grid(row=3, column=9, columnspan=3,pady=5)

        tab = self.tabs[0]
        frame = ScrollableFrame(tab,1550,700)
        frame.grid(row=0, column=0, columnspan=23, rowspan=28)

        units = ['','']
        description = ['','']
        source = ['','']
        comments = ['','']
        dic = vars(self.train)
        labels = list(dic.keys())
        values = dic.values()
        values  = [e for e in values if (type(e) is dict) & (len(e)<6)]

        for val in values:
            units.append(val['units'])
            description.append(val['Description'])
            source.append(val['Source'])
            comments.append(val['Comments'])

        labels = [e for e in labels if e not in ('bogie','carbody','sheet','carbody_links','carbody_links_name','excel','real_bogie','track')]
        i=1

        Label(frame.scrollable_frame, text = 'PARAMETERS',font= self.font_title).grid(row=0, column=2)
        Label(frame.scrollable_frame, text = 'VALUE',font= self.font_title).grid(row=0, column=3)
        Label(frame.scrollable_frame, text = 'UNITS',font= self.font_title).grid(row=0, column=4)
        Label(frame.scrollable_frame, text = 'DESCRIPTION',font= self.font_title).grid(row=0, column=5)
        Label(frame.scrollable_frame, text = 'SOURCE',font= self.font_title).grid(row=0, column=6)
        Label(frame.scrollable_frame, text = 'COMMENTS',font= self.font_title).grid(row=0, column=7)

        for label in labels:
            name= (label.upper()).replace('_',' ')
            lbl = Label(frame.scrollable_frame, text= '{}'.format(name))
            lbl.grid(row=i,column=2,sticky=W)
            units_lbl = Label(frame.scrollable_frame, text = '{}'.format(units[i-1]))
            units_lbl.grid(row = i, column=4)

            description_lbl = Label(frame.scrollable_frame, text = '{}'.format(description[i-1]))
            description_lbl.grid(row=i, column=5)

            source_lbl = Entry(frame.scrollable_frame)
            source_lbl.grid(row=i, column=6)
            source_lbl.insert(END,source[i-1])
            source_lbl.configure(state='disabled')

            comments_lbl = Entry(frame.scrollable_frame)
            comments_lbl.grid(row = i, column=7)
            comments_lbl.insert(END,comments[i-1])
            comments_lbl.configure(state='disabled')

            entry = Entry(frame.scrollable_frame)
            entry.grid(row=i,column=3)
            value = dic[('{}'.format(label))]

            if type(value) is dict:
                value = value['value']
            if type(value) is list:
                string = ''
                for config in value:
                    string = string + '{}-'.format(config)
                value = string[:-1]
            entry.insert(END,value)
            entry.configure(state='disabled')
            i=i+1
            
        row = deepcopy(i)
        carbody = self.train.CARBODY_CONFIG['value']
        self.canvas = Canvas(frame.scrollable_frame, width=400, height=400, bg="white")

        self.x = (0.02*float(self.width))
        self.y = (0.55*float(self.height))
        self.canvas.place( x=self.x ,y=self.y)
        legend = Frame(self.canvas,bg="white",highlightbackground="black", highlightthickness=2)
        legend.configure(width=400,height=400)

        legend.grid(row=0, column=0, sticky=N+S+E+W)
        legend.pack()
        bogies = self.train.BOGIE_CONFIG['value']
        colors = ['spring green','yellow','coral','blue violet','gray68','khaki1', 'orchid1', 'DarkGolderrod1']
        l=0
        for bogie in bogies:
            label1 = Label(legend, text = bogie,bg = colors[l]).grid(row=l, column=0, rowspan=2, pady=10)
            l=l+1
        i=0

        while i<len(carbody):

            if i != len(carbody):
                Label(frame.scrollable_frame, text = '{}'.format(carbody[i]), font= ('Helvetica',14)).grid(row=row+3, column=i+2)   
            if i== 0:
                image = 'cabina4'
            elif i== len(carbody)-1:
                image = 'cabina6'
            else:
                image = 'cabina5'
            label2 = self.import_image(200, 43, "png_library\\{}.png".format(image), frame.scrollable_frame)
            label2.grid(row=row+4, column=i+2)
            i=i+1

        train_config = self.train.TRAIN_CONFIG['value']

        i=0    
        while i<(len(carbody)):
            car = carbody[i]
            j=0
            for real_b  in train_config:
                if car in real_b:
                    label1 = self.import_image(38, 16, "png_library\\bogie1.png", frame.scrollable_frame)
                    label2 = Label(frame.scrollable_frame, text = '{}'.format(real_b),font=("Arial",7),borderwidth=1, relief="solid")
                    color = self.define_bogie_bg_color(real_b, colors, bogies)

                    if (j!=0)&(real_b == train_config[j-1]):
                        label1.configure(bg =color)
                        label1.grid(row=row+5, column=i+2, sticky='e', padx=30)
                        label2.grid(row=row+6, column=i+2, sticky='e', padx=30)
                    elif i<(len(carbody)-1):
                        if carbody[i+1] in real_b:
                            label1.configure(bg =color)
                            label1.grid(row=row+5, column=i+2, columnspan=2, padx=50)
                            label2.grid(row=row+6, column=i+2, columnspan=2, padx=50)
                        else:
                            label1.configure(bg =color)
                            label1.grid(row=row+5, column=i+2, sticky='w', padx=67)
                            label2.grid(row=row+6, column=i+2, sticky='w', padx=60)
                    else:
                        label1.configure(bg =color)
                        label1.grid(row=row+5, column=i+2, sticky='w', padx = 67)
                        label2.grid(row=row+6, column=i+2, sticky='w', padx = 60)
                j=j+1
            i=i+1
        self.carbody_data()
        self.track_data()

    def track_data(self):
        tab = self.tabs[1]
        frame = ScrollableFrame(tab,1550,700)
        frame.grid(row=0, column=0, columnspan=23, rowspan=28)
        track = self.train.track[0]
        track_dict = vars(track)
        labels = list(track_dict.keys())

        Label(frame.scrollable_frame, text = 'PARAMETERS',font= self.font_title).grid(row=0, column=0)
        Label(frame.scrollable_frame, text = 'VALUE',font= self.font_title).grid(row=0, column=1)
        Label(frame.scrollable_frame, text = 'UNITS',font= self.font_title).grid(row=0, column=2)
        Label(frame.scrollable_frame, text = 'DESCRIPTION',font= self.font_title).grid(row=0, column=5)
        Label(frame.scrollable_frame, text = 'SOURCE',font= self.font_title).grid(row=0, column=6, columnspan=7)
        Label(frame.scrollable_frame, text = 'COMMENTS',font= self.font_title).grid(row=0, column=12, columnspan=2)

        for num,label in enumerate(labels):
            Label(frame.scrollable_frame, text = label).grid(row = int(num)+2, column=0, sticky='w')
            values = track_dict[label]
            val = Entry(frame.scrollable_frame)
            val.grid(row = int(num)+2, column=1, sticky='w')
            val.insert(END,values['value'])
            val.configure(state='disabled')

            Label(frame.scrollable_frame, text= values['units']).grid(row = int(num)+2, column=2, sticky='w')
            Label(frame.scrollable_frame, text= values['Description']).grid(row = int(num)+2, column=4, columnspan=6, sticky='w')

            source = Entry(frame.scrollable_frame)
            source.grid(row = int(num)+2, column=11, sticky='w')
            source.insert(END,values['Source'])
            source.configure(state='disabled')

            comments = Entry(frame.scrollable_frame)
            comments.grid(row = int(num)+2, column=12,columnspan=2,padx=10, sticky='w')
            comments.insert(END,values['Comments'])
            comments.configure(state='disabled')

    def carbody_data(self):
        '''Import Carbody Data to the notebook'''

        tab = self.tabs[2]
        frame = ScrollableFrame(tab,1550,700)
        frame.grid(row=0, column=0, columnspan=23, rowspan=28)
                
        label2 = self.import_image(150, 60, "png_library\\caf_id.png", frame.scrollable_frame)
        label2.grid(row=0, column=38)

        carbody = self.train.carbody
        col = len(carbody)

        Label(frame.scrollable_frame, text = 'PARAMETERS',font=self.font_title).grid(row=0,column=2)
        Label(frame.scrollable_frame, text = 'VALUES',font= self.font_title).grid(row=0, column=4)
        Label(frame.scrollable_frame, text = 'UNITS',
              font= self.font_title).grid(row=0, column=col+5,sticky=W, columnspan = 2)
        Label(frame.scrollable_frame, text = 'DESCRIPTION',
              font= self.font_title).grid(row=0, column=col+7, columnspan=2)
        Label(frame.scrollable_frame, text = 'SOURCE',
              font= self.font_title).grid(row=0, column=col+12,sticky=W, columnspan=2)
        Label(frame.scrollable_frame, text = 'COMMENTS',
              font= self.font_title).grid(row=0, column=col+17,sticky=W, columnspan=5)

        j=3
        for car in carbody:
            i=0
            dicti =vars(car)
            keys = list(dicti.keys())

            for key in keys:

                variable = dicti[key]
                if type(variable)== str:
                    name = str(key)
                    value = variable
                    units = ''
                    description = ''
                    source = ''
                    comment = ''
                    can_view=1

                elif type(variable) is dict:
                    name = str(key)
                    value = variable['value']
                    value = self.compare_nan(value)
                    units = variable['units']
                    units = self.compare_nan(units)
                    description = variable['Description']
                    description = self.compare_nan(description)
                    source = variable['Source']
                    source = self.compare_nan(source)
                    comment = variable['Comments']
                    comment = self.compare_nan(comment)
                    can_view=1

                else:
                    can_view=0

                if can_view == 1:
                    entry = Entry(frame.scrollable_frame)
                    entry.grid(row=i+1,column=j+1,pady=4, padx=3)
                    entry.insert(END,value)
                    entry.configure(state='disabled')
                    name = Label(frame.scrollable_frame, text= '{}'.format(name))
                    name.grid(row=i+1,column=1,sticky=W, columnspan=2)
                    unit = Label(frame.scrollable_frame, text= '{}'.format(units))
                    unit.grid(row=i+1,column=5+len(carbody),sticky=W, columnspan=2)
                    descrip_lbl = Label(frame.scrollable_frame, text = '{}'.format(description))
                    descrip_lbl.grid(row=i+1,column=7+len(carbody),sticky=W, columnspan=4)

                    source_lbl = Entry(frame.scrollable_frame, width=45)
                    source_lbl.grid(row=i+1,column=12+len(carbody),sticky=W, columnspan=2)
                    source_lbl.insert(END, source)
                    source_lbl.configure(state='disabled')

                    comment_lbl = Entry(frame.scrollable_frame, width=45)
                    comment_lbl.grid(row=i+1,column=17+len(carbody),sticky=W, columnspan=5)
                    comment_lbl.insert(END,comment)
                    comment_lbl.configure(state='disabled')

                i=i+1
            j=j+1
        self.bogie_data()

    def bogie_data(self):
        '''Method to iterate bogies, to create diferent sheets to each one'''

        index=0
        bogies = self.train.bogie
        for bogie in bogies:
            bogie_name = self.train.BOGIE_CONFIG['value'][index]
            index = index+1
            tab_index = self.train.sheet.index(bogie_name)

            dicti =vars(bogie)
            keys = list(dicti.keys())


            fc = lambda dicti=dicti,keys=keys,tab_index=tab_index :[
                self.import_data(tab_index, keys, dicti)]
            fc(dicti,keys,tab_index)


    def import_data(self,tab_index,keys,dicti):
        '''Improt bogie data in the notebook'''

        tab = self.tabs[tab_index]
        frame = ScrollableFrame(tab,1500,700)
        frame.grid(row=0, column=0, columnspan=21, rowspan=28)

        Label(frame.scrollable_frame, text = 'PARAMETERS',font=self.font_title).grid(row=0,column=2)
        Label(frame.scrollable_frame, text = 'VALUES',font= self.font_title).grid(row=0, column=5)
        Label(frame.scrollable_frame, text = 'UNITS',
              font= self.font_title).grid(row=0, column=8,sticky=W, columnspan = 2)
        Label(frame.scrollable_frame, text = 'DESCRIPTION',
              font= self.font_title).grid(row=0, column=12, columnspan=2)
        Label(frame.scrollable_frame, text = 'SOURCE',
              font= self.font_title).grid(row=0, column=17,sticky=W, columnspan=2)
        Label(frame.scrollable_frame, text = 'COMMENTS',
              font= self.font_title).grid(row=0, column=22,sticky=W, columnspan=5)

        i=0
        for key in keys:
            variable = dicti[key]
            if type(variable)== str:
                name = str(key)
                value = variable
                units = ''
                description = ''
                source = ''
                comment = ''

                can_view=1
            elif type(variable) is dict:
                name = str(key)
                value = variable['value']
                value = self.compare_nan(value)
                units = variable['units']
                units = self.compare_nan(units)
                description = variable['Description']
                description = self.compare_nan(description)
                source = variable['Source']
                source = self.compare_nan(source)
                comment = variable['Comments']
                comment = self.compare_nan(comment)

                can_view=1
            else:
                can_view=0
                if i==0:
                    i=-1
                else:
                    i=i-1

            if can_view == 1:
                name = Label(frame.scrollable_frame, text= '{}'.format(name))
                name.grid(row=i+1,column=2,sticky=W, columnspan=2)

                if type(value) is dict:
                    values = list(value.values())
                    btn_name = list(value.keys())[0]
                    btn = ttk.Button(frame.scrollable_frame, text = '{}'.format(btn_name),
                                     command = lambda btn_name= btn_name, values=values, value=value
                                     :[self.button_to_graph(btn_name,values)])
                    btn.grid(row=i+1,column=5,pady=4)

                else:
                    entry = Entry(frame.scrollable_frame)
                    entry.grid(row=i+1,column=5,pady=4)
                    entry.insert(END,value)
                    entry.configure(state='disabled')

                unit = Label(frame.scrollable_frame, text= '{}'.format(units))
                unit.grid(row=i+1,column=8,sticky=W, columnspan=2)
                descrip_lbl = Label(frame.scrollable_frame, text = '{}'.format(description))
                descrip_lbl.grid(row=i+1,column=12,sticky=W, columnspan=4)

                source_lbl = Entry(frame.scrollable_frame, width=35)
                source_lbl.grid(row=i+1,column=17,sticky=W, columnspan=4)
                source_lbl.insert(END, source)
                source_lbl.configure(state='disabled')

                comment_lbl = Entry(frame.scrollable_frame, width=25)
                comment_lbl.grid(row=i+1,column=22,sticky=W, columnspan=5)
                comment_lbl.insert(END,comment)
                comment_lbl.configure(state='disabled')


            i=i+1

    def button_to_graph(self,btn_name,values):
        '''Create button if the values is a Numpy, using this to graph the numpy'''
        tabs = self.train.sheet
        if btn_name in tabs:
            current_tab = self.tabs[tabs.index(btn_name)]
            self.sheet.select(tabs.index(btn_name))

        frame= Frame(current_tab)
        frame.grid(row=2, column=0,columnspan=15,rowspan=24,sticky='ns')
        scroll = Scrollbar(frame)
        scroll.pack(side=RIGHT, fill=Y)

        table=ttk.Treeview(frame,yscrollcommand=scroll)
        table.pack(expand=1,fill=Y)
        scroll.config(command=table.yview)
        table['columns']= ('x','y')
        table.column("#0", width=0)
        table.column('x',anchor=W, width=130,stretch=True)
        table.column('y',anchor=W, width=188,stretch=True)
        table.heading("x",text = '{}'.format(values[1]),anchor=W)
        table.heading("y",text = '{}'.format(values[2]),anchor=W)

        for value in values[0]:
            table.insert('',END,values=('{}'.format(round(value[1],3)),
                                        '{}'.format(round(value[0],3))))


        self.fig, self.axis, self.toolbar, self.canvas = self.create_figure(20,110,
                                                                             '{}'.format(btn_name),
                                                                             '{}'.format(values[1]),
                                                                             '{}'.format(values[2]),
                                                                             current_tab,'')
        self.canvas.draw()
        self.toolbar.place( x= (0.57*float(self.width)),y=(0.8*float(self.height)))
        self.canvas.get_tk_widget().grid(row=0,column=18, rowspan=27)
        pt1, = self.axis.plot(values[0][:,1],values[0][:,0])
        label2 = self.import_image(150, 60, "png_library\\caf_id.png", current_tab)
        label2.place( x= (0.9*float(self.width)),y=(0.01*float(self.height)))
        ttk.Button(current_tab, text = 'Close Tab', style ='danger.Outline.TButton',
                   command = lambda:[self.sheet.hide(self.sheet.select())]).grid(row=29, column=18)

    def carbody_links_data(self):
        '''Import carbody data to the sheet'''

        links = self.train.carbody_links

        tab_index = self.train.sheet.index('Carbody_links')
        tab = self.tabs[tab_index]
        frame = ScrollableFrame(tab,1500,700)
        frame.grid(row=0, column=0, columnspan=21, rowspan=28)

        col = len(links)
        Label(frame.scrollable_frame, text = 'PARAMETERS',font=self.font_title).grid(row=0,column=2)
        Label(frame.scrollable_frame, text = 'VALUES',font= self.font_title).grid(row=0, column=4)
        Label(frame.scrollable_frame, text = 'UNITS',
              font= self.font_title).grid(row=0, column=col+5,sticky=W)
        Label(frame.scrollable_frame, text = 'DESCRIPTION',
              font= self.font_title).grid(row=0, column=col+6, columnspan=2)
        Label(frame.scrollable_frame, text = 'SOURCE',
              font= self.font_title).grid(row=0, column=col+12,sticky=W, columnspan=2)
        Label(frame.scrollable_frame, text = 'COMMENTS',
              font= self.font_title).grid(row=0, column=col+14,sticky=W, columnspan=2)

        j=2

        for link in links:
            dicti =vars(link)
            keys = list(dicti.keys())
            i=1

            for key in keys:
                variable = dicti[key]
                if type(variable)== str:
                    name = str(key)
                    value = variable
                    units = ''
                    description = ''
                    source = ''
                    comment = ''
                    can_view=1

                elif type(variable) is dict:
                    name = str(key)
                    value = variable['value']
                    value = self.compare_nan(value)
                    units = variable['units']
                    units = self.compare_nan(units)
                    description = variable['Description']
                    description = self.compare_nan(description)
                    source = variable['Source']
                    source = self.compare_nan(source)
                    comment = variable['Comments']
                    comment = self.compare_nan(comment)
                    can_view=1
                else:
                    can_view=0
                    if i==0:
                        i=-1
                    else:
                        i=i-1

                if can_view == 1:
                    name = Label(frame.scrollable_frame, text= '{}'.format(name))
                    name.grid(row=i+1,column=2,sticky=W, columnspan=2)

                    if type(value) is dict:
                        values = list(value.values())
                        btn_name = list(value.keys())[0]
                        btn = ttk.Button(frame.scrollable_frame, text = '{}'.format(btn_name),
                                          command = lambda btn_name= btn_name,
                                          values=values :[self.button_to_graph(btn_name,values)])
                        btn.grid(row=i+1,column=j+2,pady=4)

                    else:
                        entry = Entry(frame.scrollable_frame)
                        entry.grid(row=i+1,column=j+2,pady=4, padx=3)
                        entry.insert(END,value)
                        entry.configure(state='disabled')

                        unit = Label(frame.scrollable_frame, text= '{}'.format(units))
                        unit.grid(row=i+1,column=4+len(links),sticky=W, columnspan=2)
                        descrip_lbl = Label(frame.scrollable_frame, text = '{}'.format(description))
                        descrip_lbl.grid(row=i+1,column=7+len(links),sticky=W, columnspan=4)
                        source_lbl = Entry(frame.scrollable_frame)
                        source_lbl.grid(row=i+1,column=12+len(links),sticky=W, columnspan=2)
                        source_lbl.insert(END, source)
                        source_lbl.configure(state='disabled')

                        comment_lbl = Entry(frame.scrollable_frame)
                        comment_lbl.grid(row=i+1,column=17+len(links),sticky=W, columnspan=5)
                        comment_lbl.insert(END,comment)
                        comment_lbl.configure(state='disabled')

                i=i+1
            j=j+1

    def hide_tabs(self):
        '''Method to hide, numpy tabs'''

        tabs  = self.train.sheet
        can_show = ['Main','Carbody_links','Carbody_data','Track', 'LOADS']
        bogi = self.train.BOGIE_CONFIG['value']
        for tab in tabs:
            if tab in can_show:
                pass
            elif tab in bogi:
                pass
            else:
                bogies = self.tabs[tabs.index(tab)]
                self.sheet.hide(bogies)

    def wheeload_values(self,evt,opt):

        dict_load_opt = {'':'QZ0', 'Wheel Load':'QZ0', 'Primary Load':'QZ1','Secondary Load':'QZ2'}
        self.load_select = dict_load_opt[opt.get()]
        tab_index = self.train.sheet.index('LOADS')
        tab = self.tabs[tab_index]
        frame = ScrollableFrame(tab,1500,400)
        frame.grid(row=11, column=1, columnspan=23, rowspan=17)

        table_excel = ttk.Button(tab, text = 'Table to Excel',style='success.Outline.TButton',command=lambda:[self.loads_to_excel()])
        table_excel.grid(row=4, column=3, columnspan=2)
        label2 = self.import_image(100, 140, "png_library\\axle_num.png", tab)
        label2.grid(row=0, column=1, columnspan=2, rowspan=5)
        real_bogies = self.train.real_bogie
        self.empty = []
        self.load = []
        self.exceptional = []
        self.names = tuple(['{}_1 \n rt \n yu'.format(self.load_select),'{}_2'.format(self.load_select),'{}_3'.format(self.load_select),'{}_4'.format(self.load_select),'MAX','AVG','MIN']*(len(real_bogies)))
        text = ['EMPTY: MASS IN WORKING ORDER', 'LOADED: NORMAL PAYLOAD', 'EXCEPTIONAL: EXCEPTIONAL PAYLOAD']

        for bogie in real_bogies:
            values = list(vars(bogie).values())
            keys  = list(vars(bogie).keys())
            values = values[3:]
            keys = keys[3:]

            for num, key in enumerate(keys):
                val = values[int(num)]
                val = val['value']
                if self.load_select in key:
                    if 'WOP' in key:
                        self.empty.append(val)
                    elif 'NP' in key:
                        self.load.append(val)
                    elif 'EP' in key:
                        self.exceptional.append(val)
        
        self.frame2= Frame(tab)
        self.frame2.grid(row=5, column=1, columnspan=21,rowspan=6)
        scroll = Scrollbar(self.frame2)
        scroll.pack(side=RIGHT, fill=Y)
 
        scrollx = Scrollbar(self.frame2,orient='horizontal')
        scrollx.pack(side= 'bottom',fill='x')
        
        s = ttk.Style()
        s.configure("tabla1.Treeview.Heading",rowheight=20,foreground="White", background="SkyBlue4",lightcolor="#ffc61e", bordercolor="#ffc61e",darkcolor="#ffc61e")


        columns = []
        for i in range(len(self.names)):
            columns.append('c{}'.format(i))
            
        self.table2=ttk.Treeview(self.frame2,columns = columns,yscrollcommand=scroll,xscrollcommand=scrollx,style = 'tabla1.Treeview', height=8)
        self.table2.pack(fill=Y)
        scroll.config(command=self.table2.yview)
        scrollx.config(command=self.table2.xview)
        self.table2.column("#0", width=270)
        self.table2.heading('#0',text = '{}'.format(opt.get()),anchor = 'center')
        for index,col in enumerate(columns):
            self.table2.column(col, anchor = 'center', width=60)
            self.table2.heading(col,text = self.names[index],anchor = 'center')
        
        self.table2.insert('','end',text = text[0], values = self.empty)
        self.table2.insert('','end',text = text[1], values = self.load)
        self.table2.insert('','end',text = text[2], values = self.exceptional)
        
        self.options = ['Mass in Woking Order', 'Normal Payload', 'Exceptional Payload']
        load_options = tk.StringVar()
 
        s2 = ttk.Style()
        s2.configure("option1.TMenubutton", background="SkyBlue3", foreground = 'white')
 
        mass_options = ttk.OptionMenu(frame.scrollable_frame, load_options, self.options[0], *self.options,style = 'option1.TMenubutton', command=lambda evt :[ self.wheel_load_update(evt, load_options,frame.scrollable_frame,self.options)])
        mass_options.grid(row=8, column=3, columnspan=3,pady=5)
 
        carbody = self.train.CARBODY_CONFIG['value']
        train_config = self.train.TRAIN_CONFIG['value']
        bogies = self.train.BOGIE_CONFIG['value']
        colors = ['spring green','yellow','coral','blue violet','gray68','khaki1', 'orchid1', 'DarkGolderrod1']
 
        self.canvas = Canvas(frame.scrollable_frame, width=400, height=400, bg="white")
 
        self.x = (0.02*float(self.width))
        self.y = (0.3*float(self.height))
        self.canvas.place( x=self.x ,y=self.y)
        legend = Frame(self.canvas,bg="white",highlightbackground="black", highlightthickness=2)
        legend.configure(width=400,height=400)
 
        legend.grid(row=0, column=0, sticky=N+S+E+W)
        legend.pack()
        
        l=0
        for bogie in bogies:
            label1 = Label(legend, text = bogie,bg = colors[l]).grid(row=l, column=0, rowspan=2, pady=10)
            l=l+1
        i=0
        while i<len(carbody):
 
            if i != len(carbody):
                Label(frame.scrollable_frame, text = '{}'.format(carbody[i]), font= ('Helvetica',14)).grid(row=2, column=i+2)   
            if i== 0:
                image = 'cabina4'
            elif i== len(carbody)-1:
                image = 'cabina6'
            else:
                image = 'cabina5'
            label2 = self.import_image(275, 60, "png_library\\{}.png".format(image), frame.scrollable_frame)
            label2.grid(row=3, column=i+2)
            i=i+1
        i=0    
        while i<(len(carbody)):
            car = carbody[i]
            j=0
            for real_b  in train_config:
                if car in real_b:
                    label1 = self.import_image(58, 22, "png_library\\bogie1.png", frame.scrollable_frame)
                    label2 = self.import_image(65,80,"png_library\\WOP.png", frame.scrollable_frame)
                    color = self.define_bogie_bg_color(real_b, colors, bogies)
 
                    if (j!=0)&(real_b == train_config[j-1]):
                        label1.configure(bg =color)
                        label1.grid(row=4, column=i+2, sticky='e', padx=43)
                        label2.grid(row=6, column=i+2, sticky='e', padx=43)
 
                    elif i<(len(carbody)-1):
                        if carbody[i+1] in real_b:
                            label1.configure(bg =color)
                            label1.grid(row=4, column=i+2, columnspan=2, padx=40)
                            label2.grid(row=6, column=i+2, columnspan=2, padx=50)
                        else:
                            label1.configure(bg =color)
                            label1.grid(row=4, column=i+2, sticky='w', padx=90)
                            label2.grid(row=6, column=i+2, sticky='w', padx=90)
                    else:
                        label1.configure(bg =color)
                        label1.grid(row=4, column=i+2, sticky='w', padx=90)
                        label2.grid(row=6, column=i+2, sticky='w', padx=90) 
                j=j+1
            i=i+1
        self.wheel_load_update('a', load_options,frame.scrollable_frame,self.options)

    def define_bogie_bg_color(self,real_bogie,colors, bogies):
        j=0
        color= 'red'
        for bogie in bogies:
             if str(bogie) in str(real_bogie):
                 color = colors[j]
             j=j+1
        return color
        
    def wheel_load_update(self,evt,opt,frame,options):
        option_dict = {'Mass in Woking Order':'WOP', 'Normal Payload':'NP', 'Exceptional Payload':'EP'}
        color_dict = {'Mass in Woking Order':'green', 'Normal Payload':'DarkOrange3', 'Exceptional Payload':'red'}
        carbody = self.train.CARBODY_CONFIG['value']
        train_config = self.train.TRAIN_CONFIG['value']
        image = option_dict[opt.get()]
        i=0
        while i<len(carbody):
            car = carbody[i]
            k=0
            for real_b  in train_config:
                if car in real_b:
                    index = train_config.index(real_b)
                    real_bogie = self.train.real_bogie[index]
                    dict_bogie = vars(real_bogie)
                    keys = list(dict_bogie.keys())

                    new_keys = []
                    for key in keys:
                        if self.load_select in key:
                            if ('MAX' in key)|('MIN' in key)|('MED' in key):
                                pass
                            else:
                                new_keys.append(key)   
                    name = option_dict[opt.get()]
                    data = []
                    for key in new_keys:
                        if name  in key:
                           data.append(dict_bogie[key]['value'])
                    label2 = self.import_image(65,80,"png_library\\{}.png".format(image), frame)
                    right = Label(frame, text = '{}     {}'.format(data[0],data[2]), font = ('Arial',13,'bold'),borderwidth=1, relief="solid",fg=color_dict[opt.get()])
                    left = Label(frame, text = '{}     {}'.format(data[1],data[3]), font = ('Arial',13,'bold'),borderwidth=1, relief="solid",fg=color_dict[opt.get()])

                    if (k!=0)&(real_b == train_config[k-1]):
                        label2.grid(row=6, column=i+2, sticky='e', padx=43)
                        right.grid(row=5, column=i+2, sticky='e', padx=45)
                        left.grid(row=7, column=i+2, sticky='e', padx=45)

                    elif i<(len(carbody)-1):
                        if carbody[i+1] in real_b:
                            label2.grid(row=6, column=i+2, columnspan=2, padx=50)
                            right.grid(row=5, column=i+2, columnspan=2, padx=55)
                            left.grid(row=7, column=i+2, columnspan=2, padx=55)
                        else:
                            label2.grid(row=6, column=i+2, sticky='w', padx=90)
                            right.grid(row=5, column=i+2, sticky='w', padx=90)
                            left.grid(row=7, column=i+2, sticky='w', padx=90)
                            
                    else:
                        label2.grid(row=6, column=i+2, sticky='w', padx=90)
                        right.grid(row=5, column=i+2, sticky='w', padx=90)
                        left.grid(row=7, column=i+2, sticky='w', padx=90)
                k=k+1
            i=i+1


    def loads_to_excel(self):
        archivo=fd.asksaveasfilename(filetype=(('xls files','*xls*'),('All files','*.*')))
        archivo = archivo + '.xlsx'

        Excelwriter = pd.ExcelWriter(archivo, engine="xlsxwriter")

       
        # datafr.to_excel(Excelwriter,sheet_name='Load',index=self.options)

        # Excelwriter.save()
        # pass
        real_bogies = self.train.real_bogie
        self.empty = []
        self.load = []
        self.exceptional = []
        
        text = ['EMPTY: MASS IN WORKING ORDER', 'LOADED: NORMAL PAYLOAD', 'EXCEPTIONAL: EXCEPTIONAL PAYLOAD']
        loads = ['QZ0', 'QZ1', 'QZ2']
        load_rows = [2,8,14]

        for load in loads:
            temp_emp = []
            temp_load = []
            temp_exce = []
            for bogie in real_bogies:
                values = list(vars(bogie).values())
                keys  = list(vars(bogie).keys())
                values = values[3:]
                keys = keys[3:]
    
                for num, key in enumerate(keys):
                    val = values[int(num)]
                    val = val['value']
                    if load in key:
                        if 'WOP' in key:
                            temp_emp.append(val)
                        elif 'NP' in key:
                            temp_load.append(val)
                        elif 'EP' in key:
                            temp_exce.append(val)
            self.empty.append(temp_emp)
            self.load.append(temp_load)
            self.exceptional.append(temp_exce)

        names1 = tuple(['{}_1'.format(loads[0]),'{}_2'.format(loads[0]),'{}_3'.format(loads[0]),'{}_4'.format(loads[0]),'MAX','AVG','MIN']*(len(real_bogies)))
        names2 = tuple(['{}_1'.format(loads[1]),'{}_2'.format(loads[1]),'{}_3'.format(loads[1]),'{}_4'.format(loads[1]),'MAX','AVG','MIN']*(len(real_bogies)))
        names3 = tuple(['{}_1'.format(loads[2]),'{}_2'.format(loads[2]),'{}_3'.format(loads[2]),'{}_4'.format(loads[2]),'MAX','AVG','MIN']*(len(real_bogies)))
        df1 = pd.DataFrame([self.empty[0], self.load[0],self.exceptional[0]], columns= names1, index = self.options)
        df2 = pd.DataFrame([self.empty[1], self.load[1],self.exceptional[1]], columns= names2, index = self.options)
        df3 = pd.DataFrame([self.empty[2], self.load[2],self.exceptional[2]], columns= names3, index = self.options)
        print(df1)
        print(df2)
        print(df3)
        loads_df = [df1, df2, df3]

        for index, dataframe in enumerate(loads_df):
            print(index)
            dataframe.to_excel(Excelwriter, sheet_name='Loads',startrow=load_rows[index], startcol=0, index = True)

        workbook  = Excelwriter.book
        worksheet = Excelwriter.sheets['Loads']
        
        
        # Add a format. Light red fill with dark red text.
        format1 = workbook.add_format({'bg_color': '#FFC7CE'})
        format2 = workbook.add_format({'bg_color': '#349A86'})
        format3 = workbook.add_format({'bg_color': '#DCCB3B'})
        
        # Set the conditional format range.
        start_row = 0
        start_col = 0
        end_row = 100
        end_cold = 100
        
        # Apply a conditional format to the cell range.
        worksheet.conditional_format(start_row, start_col, end_row, end_cold,
                                     {'type':     'text',
                                      'criteria': 'containing',
                                      'value':    'QZ0',
                                      'format':   format1})
        worksheet.conditional_format(start_row, start_col, end_row, end_cold,
                                     {'type':     'text',
                                      'criteria': 'containing',
                                      'value':    'QZ1',
                                      'format':   format2})
        worksheet.conditional_format(start_row, start_col, end_row, end_cold,
                                     {'type':     'text',
                                      'criteria': 'containing',
                                      'value':    'QZ2',
                                      'format':   format3})
        Excelwriter.save()