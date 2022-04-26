# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 12:27:48 2022

@author: Peru _Alana
"""
from tkinter import ttk, END, Label
from tkinter import Frame,W, E, S, N, Entry, Scrollbar,RIGHT,Y, Canvas
from tkinter import *
import tkinter as tk
from matplotlib.figure import Figure
from ttkbootstrap import Style
from PIL import ImageTk, Image
from copy import deepcopy


colors = ['white','spring green','yellow','coral','blue violet','gray68','khaki1', 'orchid1', 'DarkGolderrod1']
motor_bool = ['yes','no','yes']
bogie = ['ML8.001', 'ML9', 'ML8.101']

carbody = ['C1','S1','R','S2','C2']
config = []
names = deepcopy(bogie)
config_train = []

class ScrollableFrame(ttk.Frame):
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
        for row_index in range(30):
            self.scrollable_frame.rowconfigure(row_index, weight=1,minsize=42)
            for col_index in range(40):
                self.scrollable_frame.columnconfigure(col_index, weight=1,minsize=50)
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

def import_image(x,y,path,frame):
    '''Import image as label in a frame'''
    image2 = Image.open(path)
    image2 = image2.resize((x, y), Image.ANTIALIAS)
    photo2 = ImageTk.PhotoImage(image2)
    label2 = Label(frame, image = photo2)
    # , borderwidth=1, relief="solid"
    label2.image2 = photo2
    label2.configure
    return label2

def train_configuration(lista,bogie_dict):
    print(lista)
    name = ''
    if len(config) !=len(carbody):
        config.append(lista)

    if len(config) ==len(carbody):
        keys = list(bogie_dict.keys())
        keys.pop(0)
        i=0
        while i<len(config):
            car = config[i]
            for key in keys:
                if str(key) in car:
                    index = car.index(str(key))
                    count = car.count(str(key))
                    bogie_name = bogie_dict[key]
                    name = bogie_name

                    if index == 2:
                        carro= '('+ carbody[i] + '-' + carbody[i+1] + ')'
                    else:
                        carro= '('+ carbody[i] + ')'

                    print(carro)
                    string = name + carro
                    if count ==1:
                        config_train.append(string)
                    else:
                        for k in range(count):
                            if k==1:
                                string = '*' + string
                            config_train.append(string)
                    
            i=i+1
        print(config_train)
        config.clear()
        config_train.clear()


def confirm_configuration(vars_options,carbody,frame,num_bogie,bogie_dict):

    num_bogie.pop(0)
    bogie_position = bogie

    i=0
    while i<len(carbody):
        if i != len(carbody):
            Label(frame, text = '{}'.format(carbody[i]), font= ('Helvetica',14,'underline')).grid(row=11, column=i,padx=20)   
        if i== 0:
            image = 'cabina4'
        elif i== len(carbody)-1:
            image = 'cabina6'
        else:
            image = 'cabina5'
        label2 = import_image(230, 60, "png_library\\{}.png".format(image), frame)
        label2.grid(row=12, column=i,sticky='we')
        i=i+1
    j=0
    k=0
    while j <((len(carbody)*3)):
        if j != (len(carbody)*3)-3:
            val = vars_options[j+2].get()
        else:
            val = '(-)'

        lista = [vars_options[j].get(),vars_options[j+1].get(),val]

        train_configuration(lista,bogie_dict)

        lista_figure = []
        for value in lista:
            if value == '(-)':
                lista_figure.append('nada')
            else:
                index = num_bogie.index(int(value))
                motor_value = motor_bool[index]
                if motor_value == 'yes':
                    lista_figure.append('bogie2')
                else:
                    lista_figure.append('bogie1')
        label1 = import_image(62, 22, "png_library\\{}.png".format(lista_figure[0]), frame)
        if lista[0] != '(-)':
            label1.configure(bg = colors[int(lista[0])])
        label1.grid(row=12, column=k,rowspan=3,padx=50,sticky='w')

        label2 = import_image(62, 22,  "png_library\\{}.png".format(lista_figure[1]), frame)
        if lista[1] != '(-)':
            label2.configure(bg = colors[int(lista[1])])
        label2.grid(row=12, column=k,rowspan=3,padx=50, sticky='e')

        if k!=(len(carbody)-1):
            label3 = import_image(70, 22,  "png_library\\{}.png".format(lista_figure[2]), frame)
            if lista[2] != '(-)':
                label3.configure(bg = colors[int(lista[2])])
            label3.grid(row=12, column=k,rowspan=3,padx=40,columnspan=2)
        k=k+1
        j=j+3
    num_bogie.insert(0,'(-)')


def main():
    root = Tk()
    style = Style()
    root.state('zoomed')
    
    for row_index in range(20):
        root.rowconfigure(row_index, weight=1,minsize=20)
        for col_index in range(40):
            root.columnconfigure(col_index, weight=1,minsize=30)
            
    frame = ScrollableFrame(root,1500,700)
    frame.grid(row=0, column=0, columnspan=40, rowspan=20)

    vars_options = []
    for i in range((len(carbody)*3)-1):
        option = tk.StringVar()
        vars_options.append(option)

    bogie.insert(0,'None')
    bogie

    num_bogie= []
    for num,bogi in enumerate(bogie):
        num_bogie.append(num)

    num_bogie.insert(0,'(-)')
    num_bogie.pop(1)
    bogie_dict = {num_bogie[i]:bogie[i] for i in range(len(num_bogie))}
    
    btn_confirm = ttk.Button(frame.scrollable_frame, text = 'Confirm Configuration', command = lambda:[confirm_configuration(vars_options,carbody,frame.scrollable_frame,num_bogie,bogie_dict)]).grid(row=0, column=4)
    for i, bogi  in enumerate(bogie):
        if i == 0:
            Label(frame.scrollable_frame, text = '(-):   {}'.format(bogi)).grid(row=i, column=2)
        else:
            Label(frame.scrollable_frame, text = '{}:   {}'.format(i,bogi)).grid(row=i, column=2)
            Label(frame.scrollable_frame, text = '      ',bg=colors[i]).grid(row=i, column=2, columnspan=2)
    i=0
    j=0
    while i<len(carbody):
        if i== 0:
            image = 'cabina4'

        elif i== len(carbody)-1:
            image = 'cabina6'
        else:
            image = 'cabina5'
        label2 = import_image(230, 60, "png_library\\{}.png".format(image), frame.scrollable_frame)
        label2.grid(row=6, column=i)

        s = ttk.Style()
        s.configure("cabina1.TMenubutton", background="sandy brown", foreground = 'black')
        v = ttk.Style()
        v.configure("cabina2.TMenubutton", background="ivory2", foreground = 'black')

        if i != len(carbody):
            Label(frame.scrollable_frame, text = '{}'.format(carbody[i]), font= ('Helvetica',14,'underline')).grid(row=5, column=i,padx=20)

        option3 = ttk.OptionMenu(frame.scrollable_frame,vars_options[j],num_bogie[0],*num_bogie,style = 'cabina2.TMenubutton')
        option3.grid(row=7, column=i,padx=50,sticky='nw')
        j=j+1

        option2 = ttk.OptionMenu(frame.scrollable_frame,vars_options[j],num_bogie[0],*num_bogie,style = 'cabina2.TMenubutton')
        option2.grid(row=7, column=i,padx=50, sticky='ne')
        j=j+1
        
        if i!=(len(carbody)-1):
            option1 = ttk.OptionMenu(frame.scrollable_frame,vars_options[j],num_bogie[0],*num_bogie,style = 'cabina1.TMenubutton')
            option1.grid(row=7, column=i,padx=40,columnspan=2, sticky='n')
            j=j+1  
        i=i+1


    root.mainloop()

if __name__ == '__main__':
    main()