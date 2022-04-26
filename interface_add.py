# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:20:27 2022

@author: Peru _Alana
"""

import os
from tkinter import ttk,Label,END,CENTER, StringVar, messagebox,Frame,Canvas, Scrollbar,Checkbutton
import tkinter as Tk
from ttkwidgets import CheckboxTreeview
from copy import deepcopy
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)



import tools.interface_base
import tools.class_vehicle
import tools.class_bogie
import tools.class_carbody
import tools.class_carbody_links
import tools.class_real_bogie
import tools.interface_view_data
import tools.interface_compare_parameter
import tools.dynamic_atr
import tools.class_track


FONT = ('Helvetica', 12)
FONT_TITLE = ('Helvetica', 20, "bold")
FONT_TITLE2 = ('Helvetica', 16, "italic")
FONT_TITLE3 = ('Helvetica', 13, "italic")
STYLE_LABEL = 'primary.TLabel'
STYLE_ENTRY = 'info.TEntry'
FONT_EXAMPLE = ('Helvetica', 10, "italic")
current_path = os.getcwd()


class WindowMain(tools.interface_base.Base_interface):
    """
    class Window_main():
        In this class the frame main menu has been initialized

    Properties
    ----------

    frame_main: Frame
        Tkinter frame is stored and configured

    data_base: Data base
        This value has been imported or created for the aplication

    Methods
    -------
    add_window(self):
        Send the Tkinter window to another class to import its window add frame

    delete_window(self):
        Send the Tkinter window to another class to import its window edit frame

    edit_window(self):
        Send the Tkinter window to another class to import its window delete frame

    view_window(self):
        Send the Tkinter window to another class to import its window view & compare frame

    export_csv(self):
        Export all the information to .csv


    """

    def __init__(self, master, data_base,admin):
        super().__init__(master)
        self.master = master
        # Call to Base interface to crate new frame
        self.frame_main = self.new_frame('Main menu')
        self.frame_main.tkraise()
        self.filter = StringVar()
        # Import the data base to the class
        self.data_base = data_base
        self.list_add_atr = []
        self.list_del_atr = []
        self.list_del_object = []
        self.admin = admin
        
        self.widgets_window_main()

    def widgets_window_main(self):
        '''Create widgets for the frame main'''

        admin_btn = ttk.Button(self.frame_main, text = 'ADMINISTRADOR MODE',
                                style='primary.Outline.TButton',command=lambda:
                                [self.admin_mode_options()])
        admin_btn.grid(row=4, column=0, columnspan=2, pady=4)
        heading = ttk.Label(self.frame_main, text='Data Base Options:',
                            style='primary.TLabel', font=FONT_TITLE2)
        heading.grid(row=1, column=0, columnspan=2, pady=4)

        compare_atr = ttk.Button(self.frame_main, text='COMPARE PARAMETER',
                                 style='primary.Outline.TButton',command=lambda:
                                [self.compare_parameter(),self.frame_main.pack_forget()])

        compare_atr.grid(row=2, column=0, columnspan=2, pady=4)

        self.update_atr_btn = ttk.Button(self.frame_main, text='UPDATE ATTRIBUTES',
                                  style='primary.Outline.TButton', command=lambda: [
                                      self.update_attributes()])


        self.delete_vehicle = ttk.Button(self.frame_main, text='Delete Vehicle',
                                    style='primary.Outline.TButton', command=lambda: [
                                    self.delete_window()])

        import_all_btn = ttk.Button(self.frame_main, text = 'IMPORT PROJECT FROM EXCEL',
                                    style ='primary.Outline.TButton',
                                    command = lambda:[self.import_all_the_proyect(),
                                                      self.frame_main.pack_forget(),
                                                      WindowMain(self.master, self.data_base,self.admin)])
        import_all_btn.grid(row=3, column=0, columnspan=2, pady=4)

        self.atr_delete = ttk.Button(self.frame_main, text = 'DELETE ATTRIBUTE', style='primary.Outline.TButton', command = lambda:[self.delete_attributes()])

        sep2 = ttk.Separator(
            self.frame_main, style='info.secondary.Horizontal.TSeparator')
        sep2.grid(row=7, column=0, columnspan=2, pady=4, ipadx=150)

        self.search_entry = ttk.Entry(self.frame_main,textvariable= self.filter,
                                      width=15,font= FONT, style='info.TEntry')
        self.search_entry.grid(row=9, column=0, columnspan=2, pady=4)

        search_btn = ttk.Button(self.frame_main, text="Search", width=10,
                                style='primary.Outline.TButton',
                                command=lambda:[self.search_table(self.search_entry.get())])
        search_btn.grid(row=10, column=0, columnspan=5, pady=4)

        view_btn = ttk.Button(self.frame_main, text="View Data", width=10,
                                style='primary.Outline.TButton',
                                command=lambda:[self.view_data()])
        view_btn.grid(row=11, column=0, columnspan=2, pady=4)

        reset_btn = ttk.Button(self.frame_main, text="Reset", width=10,
                               style='danger.Outline.TButton',
                               command= lambda:[self.travel_menu(self.frame_main)] )
        reset_btn.grid(row=10, column=0)

        search_label = ttk.Label(self.frame_main, text = 'Table Options:',
                                 style= STYLE_LABEL, font=FONT_TITLE2)
        search_label.grid(row=8, column=0, columnspan=2, pady=4)

        title_label = ttk.Label(self.frame_main, text = 'Dynamics Data Base',
                                style= STYLE_LABEL, font= ('Helvetica', 27, "bold",'underline'))
        title_label.grid(row=0, column=7, columnspan=9)

        table_title = ttk.Label(self.frame_main, text ='View Vehicle Data',
                                font= FONT_TITLE2, style='primary.TLabel')
        table_title.grid(row=7, column=7, rowspan=1)
        self.close_button(self.frame_main)

        # Define position of the frame in the window
        self.frame_main.grid_columnconfigure(0, minsize=10)

        # Create table to summarizes the database information
        self.columns=('code','name','type','bogie configuration','carbody configuration')
        self.table = ttk.Treeview(self.frame_main, column=self.columns, show = 'headings')

        if self.admin is True:
            self.update_atr_btn.grid(row=5, column=0, columnspan=2, pady=4)
            self.delete_vehicle.grid(row=12, column=0, columnspan=2, pady=4)
            self.atr_delete.grid(row=6, column=0, columnspan=2, pady=4)

        self.create_table()

    def delete_attributes(self):
        self.frame = self.new_frame('Attribute delete')
        self.frame1= Frame(self.frame)
        self.frame1.grid(row=2, column=3,rowspan=12,sticky='nswe')

        scroll = Scrollbar(self.frame1)
        scroll.pack(side='right', fill='y')

        scrollx = Scrollbar(self.frame1,orient='horizontal')
        scrollx.pack(side= 'bottom', fill='x')
        
        self.table1= CheckboxTreeview(self.frame1,yscrollcommand=scroll,xscrollcommand=scrollx)
        self.table1.pack(expand=1,fill='y')
        scroll.config(command=self.table1.yview)
        scrollx.config(command=self.table1.xview)
        self.table1.column("#0", width=500)
        self.table1.heading('#0', text ='Attributes')
        title = ttk.Label(self.frame, text = 'Choose attribute to delete:',font=FONT_TITLE2)
        title.grid(row=1, column=3)

        frame2 = Frame(self.frame,highlightbackground="black", highlightthickness=2)
        frame2.grid(row=2, column=5)

        search_box_atr = ttk.Entry(frame2, style = STYLE_ENTRY)
        search_box_atr.grid(row=0, column=0,pady=5,padx=5)
        search_button = ttk.Button(frame2,text = 'Search Attribute', style = 'primary.Outline.TButton', command= lambda:[self.search_text(search_box_atr.get())])
        search_button.grid(row=1, column=0,pady=5,padx=5)

        tools.interface_compare_parameter.CompareParameter.import_parameters(self) ############### Import attributes using another function ##############

    def search_text(self,filt):
        ''' Search attributes '''

        self.selected_attributes = []
        filt = filt.lower()
        for item in self.table1.get_children():
            if filt in (self.table1.item(item)['text']).lower():
                self.table1.change_state(item,'checked')
                self.selected_attributes.append(self.table1.item(item)['text'])
            else:
                self.table1.item(item, open=True)
                for subitem in self.table1.get_children(item):
                    if filt in (self.table1.item(subitem)['text']).lower():
                        self.table1.change_state(subitem,'checked')
                        self.selected_attributes.append(self.table1.item(subitem)['text'])
                        self.table1._check_ancestor(subitem)
                        self.table1._check_descendant(subitem)
                    else:
                        self.table1.item(subitem, open=True)
                        for subsubitem in self.table1.get_children(subitem):
                            if filt in (self.table1.item(subsubitem)['text']).lower():
                                self.table1.change_state(subsubitem,'checked')
                                self.selected_attributes.append(self.table1.item(subsubitem)['text'])
                                self.table1._check_ancestor(subsubitem)
                                self.table1._check_descendant(subsubitem)
                            else:                  
                                for subsubsubitem in self.table1.get_children(subsubitem):
                                    if filt in (self.table1.item(subsubsubitem)['text']).lower():
                                        self.table1.item(subsubitem, open=True)
                                        self.table1.change_state(subsubsubitem,'checked')
                                        self.selected_attributes.append(self.table1.item(subsubsubitem)['text'])
                                        self.table1._check_ancestor(subsubsubitem)
                                        self.table1._check_descendant(subsubsubitem)
        self.view_attributes()
        
    def view_attributes(self):

        try:
            if self.frame3.winfo_exists():
                self.frame3.grid_forget()

        except AttributeError:
            pass 

        self.frame3 = Frame(self.frame,highlightbackground="black", highlightthickness=2)
        self.frame3.grid(row=2, column=7, rowspan=13,columnspan=9)
        for index, atr in enumerate(self.selected_attributes):
            description = self.search_description(atr)
            variab = Tk.BooleanVar(self.frame3)
            check = Checkbutton(self.frame3, text = '{} : {}'.format(atr,description), variable = variab ).grid(row=index, column=0, sticky='w')

        delete_button = ttk.Button(self.frame3, text = 'Delete', style= 'danger.Outline.TButton')
        delete_button.grid(row=100, column=0, pady=6, padx=5, sticky='w')
        select_all = ttk.Button(self.frame3, text = 'Select All', style= 'primary.Outline.TButton')
        select_all.grid(row=100, column=0, pady=6, padx=5, sticky='e')
    def compare_parameter(self):
        '''Navegate to compare parameter frame'''

        tools.interface_compare_parameter.CompareParameter(self.master,self.data_base,self.admin)

    def delete_window(self):
        ''' Navigate to delete vehicle menu'''
        for selected_item in self.table.selection():
            item = self.table.item(selected_item)
            record = item['values']
            vehicle_name = record[1]

        confirm = messagebox.askokcancel(message="¿ You want to delete '{}'?".format(vehicle_name),
                                         title="Warning!")
        print(confirm)
        if confirm is True:
            index = self.data_base.name_list.index(vehicle_name)
            del self.data_base.name_list[index]
            del self.data_base.vehicle[index]
            self.table.delete(*self.table.get_children())
            self.table.grid_forget()
            self.create_table()

    def create_table(self):
        '''Create summary table'''

        for col in self.columns:
            self.table.heading(col, text=col.title(),
                               command=lambda c=col: self.sortby(self.table, c, 0))
            if (('bogie' in col) is True) |(('carbody'in col) is True):
                width=340
            else:
                width=150
            self.table.column(col, width=width, stretch=True, anchor=CENTER)


        self.table.grid(row=2, column=3,columnspan=16,rowspan=12,sticky='nsew')
        data = self.import_data_to_table()

        for value in data:
            self.table.insert('',END,values=value)

    def sortby_len(self,e):
        '''Sort by length'''

        length=e[0].count('-')
        return length

    def sortby(self,tree, col, descending):
        '''Sort table '''
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        if (('bogie' in col) is True) |(('carbody'in col) is True):
            data.sort(reverse=descending,key=self.sortby_len)
        else:
            data.sort(reverse=descending)
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

        tree.heading(col,command=lambda col=col: self.sortby(tree, col, int(not descending)))

    def search_table(self,filt):
        '''Take out values from table'''

        search = filt.lower()
        for child in self.table.get_children():
            lista = self.table.item(child)['values']
            search_time=0
            if search in self.table.item(child)['values']:
                pass
            else:
                for value in lista:
                    if (search in str(value).lower())  is True:
                        pass
                    else:
                        search_time=search_time+1
            if search_time == len(lista):
                self.table.delete(child)

    def view_data (self):
        '''Travel to view data frame'''

        for selected_item in self.table.selection():
            item = self.table.item(selected_item)
            record = item['values']
            vehicle_name = record[1]
            tools.interface_view_data.ViewAnyData(self.master,self.data_base,vehicle_name,self.admin)

    def update_attributes(self):
        '''Update general attributes of the database'''

        if self.data_base.attributes != []:
            self.temp_attributes = deepcopy(self.data_base.attributes)

        self.list_add_atr.clear()
        self.list_del_atr.clear()
        self.list_del_object.clear()
        vehi_atr, bogie_atr, car_atr, link_atr, track_atr= tools.dynamic_atr.atr_ini()
        tools.class_vehicle.Vehicle('',vehi_atr)
        self.data_base.add_attributes(vehi_atr, bogie_atr, car_atr, link_atr,track_atr)
        self.update_vehicles()

    def update_atr_add(self,lista_objetos,objeto_atr_inicial,objeto_inicial):
        '''Iterate object to add new attribute'''

        list_add_object = []
        for objeto in lista_objetos:
            proyect_atr = list(objeto.__dict__.keys())
            if objeto_atr_inicial == proyect_atr:
                pass
            else:
                for ini_atr in objeto_atr_inicial:
                    if hasattr(objeto,ini_atr):
                        pass
                    else:
                        if ini_atr not in self.list_add_atr:
                            self.list_add_atr.append(ini_atr)
                            list_add_object.append(str(objeto_inicial))

                        atr = getattr(objeto_inicial,ini_atr)
                        setattr(objeto, ini_atr,atr)

        return lista_objetos

    def update_atr_rest(self,lista_objetos,objeto_atr_inicial,objeto_inicial):
        '''Iterate object to delete attribute'''

        for objeto in lista_objetos:
            object_atr = list(objeto.__dict__.keys())
            if object_atr == objeto_atr_inicial:
                pass
            else:
                for atr in object_atr:
                    if hasattr(objeto_inicial, atr):
                        pass
                    else:
                        self.list_del_atr.append(atr)
                        self.list_del_object.append(objeto)
        return lista_objetos

    def update_vehicles(self):
        '''Range all the vehicle and his objects'''

        vehicles = self.data_base.vehicle
        ini_vehicle = tools.class_vehicle.Vehicle('a',self.data_base.attributes[0])
        vehi_ini_atr = list(ini_vehicle.__dict__.keys())
        objects = self.update_atr_add(vehicles, vehi_ini_atr,ini_vehicle)
        objects = self.update_atr_rest(objects, vehi_ini_atr, ini_vehicle)
        self.data_base.vehicle = objects

        for vehicle in vehicles:
            bogies = vehicle.bogie
            ini_bogie = tools.class_bogie.Bogie('b',self.data_base.attributes[1])
            bogi_ini_atr = list(ini_bogie.__dict__.keys())
            objects = self.update_atr_add(bogies,bogi_ini_atr,ini_bogie)
            objects = self.update_atr_rest(objects, bogi_ini_atr,ini_bogie)
            vehicle.bogie = objects

            carbodies = vehicle.carbody
            ini_car = tools.class_carbody.Carbody('c',self.data_base.attributes[2])
            carbody_ini_atr = list(ini_car.__dict__.keys())
            objects = self.update_atr_add(carbodies, carbody_ini_atr,ini_car)
            objects = self.update_atr_rest(objects, carbody_ini_atr,ini_car)
            vehicle.carbody = objects

            carbody_links = vehicle.carbody_links
            ini_link = tools.class_carbody_links.CarbodyLinks('d',self.data_base.attributes[3])
            link_ini_atr =list(ini_link.__dict__.keys())
            objects = self.update_atr_add(carbody_links, link_ini_atr,ini_link)
            objects = self.update_atr_rest(objects, link_ini_atr,ini_link)
            vehicle.carbody_links = objects

            track = vehicle.track
            ini_track = tools.class_track.Track(self.data_base.attributes[4])
            track_ini_atr = list(ini_track.__dict__.keys())
            objects = self.update_atr_add(track, track_ini_atr, ini_track)
            objects = self.update_atr_rest(track, track_ini_atr, ini_track)
            vehicle.track = objects
        self.data_base.vehicle = vehicles

        if self.list_del_atr != []:
            string=''
            list_messagebox = []
            for x in self.list_del_atr:
                if x not in list_messagebox:
                    list_messagebox.append(x)
                    string += '-' + x + '\n'
    
            recep = messagebox.askyesno(message = "¿You want to delete the attributes?"
                                   + '\n' + string, title = "Updating data base" )

            if recep is True:
                i=0
                for objeto in self.list_del_object:
                    atr = self.list_del_atr[i]
                    delattr(objeto,atr)
                    i=i+1
            else:
                self.data_base.attributes = self.temp_attributes

        string = ''
        if self.list_add_atr != []:
            for x in self.list_add_atr:
                string += '-' + x + '\n'
            messagebox.showinfo(message = "These attributes have been added "
                                + '\n' + string,
                                title = "Updating data base" )

    def admin_mode_options(self):
        self.labels = []
        self.admin_dict = {'peru':'peru123',
                      'joseba':'joseba123',
                      'sara':'sara123',
                      'maialen':'maialen123',
                      }

        self.canvas = Canvas(self.frame_main, width=500, height=500, bg="white")
        self.x = (0.5*float(self.width))
        self.y = (0.1*float(self.height))
        self.canvas.place( x=self.x ,y=self.y)
        self.admin_frame = Frame(self.canvas,bg="white",highlightbackground="black", highlightthickness=1)
        self.admin_frame.configure(width=500,height=500)
        for row_index in range(5):
            self.admin_frame.rowconfigure(row_index, weight=1,minsize=40)
            for col_index in range(4):
                self.admin_frame.columnconfigure(col_index, weight=1,minsize=40)
        self.admin_frame.grid(row=0, column=0, sticky='nsew')

        self.admin_frame.pack()
        label2 = self.import_image(16, 16, "png_library\\cerrar.png", self.admin_frame)
        label2.configure(bg="white")
        label2.grid(row=0, column=4, sticky='ne')
        label2.bind("<Button-1>", lambda e: self.canvas.place_forget())

        self.see_pass_var = Tk.BooleanVar(self.admin_frame)
        self.see_pass = ttk.Checkbutton(self.admin_frame, text = 'PW Visible',variable = self.see_pass_var, style= 'toggle.TCheckbutton', command = lambda:[self.password_visible()])
        self.see_pass.grid(row=2, column=3, columnspan=2)

        title = ttk.Label(self.admin_frame, text = 'Admin Mode', style = 'primary.TLabel',  font= ('Helvetica',11,'underline'))
        title.grid(row=0, column=1, columnspan=2)

        user = ttk.Label(self.admin_frame,text = 'User:', style = 'primary.TLabel')
        user.grid(row=1, column=0)
        password = ttk.Label(self.admin_frame,text = 'Password:', style = 'primary.TLabel')
        password.grid(row=2, column=0)
        

        user_entry = ttk.Entry(self.admin_frame, style= 'info.TEntry')
        user_entry.grid(row=1, column=1, columnspan=2)
        self.password_entry = ttk.Entry(self.admin_frame,style= 'info.TEntry', show='*')
        self.password_entry.grid(row=2, column=1, columnspan=2)
        
        cancel_btn = ttk.Button(self.admin_frame, text = 'Cancel',style='danger.Outline.TButton', command=lambda: [self.canvas.destroy()])
        cancel_btn.grid(row=3, column=0, columnspan=2)
        confirm_btn = ttk.Button(self.admin_frame, text = 'Confirm',style='success.Outline.TButton', command=lambda: [self.confirm_admin(user_entry.get(), self.password_entry.get())])
        confirm_btn.grid(row=3, column=2, columnspan=4)

    def password_visible(self):
        if self.see_pass_var.get() is False:
            self.password_entry.config(show='*')
        else:
            self.password_entry.config(show='')
        pass
    def confirm_admin(self, user_txt, password_txt):
        for label in self.labels:
            label.grid_forget()

        admin_users = list(self.admin_dict.keys())
        admin_passwords = list(self.admin_dict.values())
        if (user_txt in admin_users):
            index = admin_users.index(user_txt)

            if password_txt == admin_passwords[index]:
                self.correct = Label(self.admin_frame, text = 'Welcome {}'.format(user_txt))
                self.correct.config(fg='green')
                self.correct.grid(row=4, column=0, columnspan=4)
                self.labels.append(self.correct)
                self.update_atr_btn.grid(row=5, column=0, columnspan=2, pady=4)
                self.delete_vehicle.grid(row=12, column=0, columnspan=2, pady=4)
                self.atr_delete.grid(row=6, column=0, columnspan=2, pady=4)
                self.admin = True

        else:
            self.incorrect = Label(self.admin_frame, text = 'Username or Password Incorrect')
            self.incorrect.config(fg='red')
            self.incorrect.grid(row=4, column=0, columnspan=4)
            self.labels.append(self.incorrect)
        pass

        