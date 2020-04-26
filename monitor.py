#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
temp_monitor.py
written by Joseph Metrailler
2019-2020
to display and graph our house temperatures
"""

import tkinter as tk
from tkinter import *

from datetime import datetime, timedelta
from math import *

from lib.mysql_lib_logger import Mysql
import pdb

class Main:
    
    """ Cette classe permet d'afficher les graphiques des températures
    """
    
    def __init__(self, tk_root):

        # version infos
        self.VERSION_NO = "0.01.01" 
        self.VERSION_DATE = "25.04.2020"
        self.VERSION_DESCRIPTION = "start of the new version 'logger'"
        self.VERSION_STATUS = "in development"
        self.VERSION_AUTEUR = "Joseph metrailler"
        
        # variables de controle
        self._job = None
        self.t_pause = 5000 # 60 secondes 
        self.n_passe = 0
        # initialize self.t_elapsed to 0 seconds
        self.t_elapsed = datetime.now() - datetime.now() 

        # variables de dimensions ecran
        self.max_width = 1920
        self.max_height = 1080
        screen_width = tk_root.winfo_screenwidth()  
        screen_height = tk_root.winfo_screenheight()  
        self.win_width_th = min(self.max_width, screen_width)
        self.win_height_th = min(self.max_height, screen_height)


        # reduire de pc_red la taille utilisée par l'application
        win_reduction_factor = 0.9
        self.win_width =  int(self.win_width_th * win_reduction_factor)
        self.win_height = int(self.win_height_th * win_reduction_factor)

        self.win_pos_x = (self.win_width_th - self.win_width) / 2
        self.win_pos_y = (self.win_height_th - self.win_height) / 20
#         pdb.set_trace()
        print("win size :" , self.win_width, "x", self.win_height)
        
        # main windows
        self.tk_root = tk_root
        self.tk_root.geometry("%dx%d+%d+%d" % (self.win_width, self.win_height, self.win_pos_x, self.win_pos_y))
        
        
        self.ip_db_server = "192.168.1.139"
        self.mysql_logger = Mysql(self.ip_db_server)
#         self.local_ip = self.mysql_logger.local_ip

        # initialisations
        self.NBRE_DAYS_ON_GRAPH = 0.5
        self.nbre_hours_on_graph = self.NBRE_DAYS_ON_GRAPH * 24
        
        # etendue de l'axe du temps (x)
        self.nbre_days_on_display = IntVar(self.tk_root)
        if self.NBRE_DAYS_ON_GRAPH == 0.25: self.nbre_days_on_display.set(0)
        elif self.NBRE_DAYS_ON_GRAPH == 0.5: self.nbre_days_on_display.set(1)
        elif self.NBRE_DAYS_ON_GRAPH == 1: self.nbre_days_on_display.set(2)
        elif self.NBRE_DAYS_ON_GRAPH == 2: self.nbre_days_on_display.set(3)
        elif self.NBRE_DAYS_ON_GRAPH == 4: self.nbre_days_on_display.set(4)
        elif self.NBRE_DAYS_ON_GRAPH == 7: self.nbre_days_on_display.set(5)
        elif self.NBRE_DAYS_ON_GRAPH == 14: self.nbre_days_on_display.set(6)
        elif self.NBRE_DAYS_ON_GRAPH == 30: self.nbre_days_on_display.set(7)
        else: self.nbre_days_on_display.set(2)

        self.TRACE_WIDTH = 2

        # variable de commande pour l'affichage des différentes traces
        # afficheurs
        self.display_trace_salon = IntVar(self.tk_root)
        self.display_trace_bureau = IntVar(self.tk_root)
        self.display_trace_ext = IntVar(self.tk_root)
        
        # PAC
        self.display_trace_from_pac = IntVar(self.tk_root)
        self.display_trace_from_accu = IntVar(self.tk_root)
        self.display_trace_to_pac = IntVar(self.tk_root)
        self.display_trace_pac_ft = IntVar(self.tk_root)
        
        #Home
        self.display_trace_on_bypass = IntVar(self.tk_root)
        self.display_trace_from_home = IntVar(self.tk_root)
        self.display_trace_from_home_rez = IntVar(self.tk_root)
        self.display_trace_from_home_1er = IntVar(self.tk_root)
        self.display_trace_to_home = IntVar(self.tk_root)
        self.display_trace_from_bypass = IntVar(self.tk_root)
        self.display_trace_home_ft = IntVar(self.tk_root)
        
        # Boiler
        self.display_trace_from_boiler = IntVar(self.tk_root)
        self.display_trace_to_boiler = IntVar(self.tk_root)
        self.display_trace_in_boiler = IntVar(self.tk_root)
        self.display_trace_boiler_ft = IntVar(self.tk_root)
        
        # ON/OFF pac et boiler
        self.display_trace_pac_on_off = IntVar(self.tk_root)
        self.display_trace_boiler_on_off = IntVar(self.tk_root)
        
        # affichages des valeurs sur le curseur de la souris
        self.display_valeur_x = IntVar(self.tk_root)
        self.display_valeur_y = IntVar(self.tk_root)
        
        # choix de la source pour la database
        self.selected_ip = IntVar(self.tk_root)
        self.selected_ip.set(self.ip_db_server)

        # initialisation des variables
        # afficheurs
        self.display_trace_salon.set(True)
        self.display_trace_bureau.set(True)
        self.display_trace_ext.set(True)
        
        # PAC
        self.display_trace_from_pac.set(False)
        self.display_trace_from_accu.set(False)
        self.display_trace_to_pac.set(False)
        self.display_trace_pac_ft.set(False)
        
        #Home
        self.display_trace_on_bypass.set(False)
        self.display_trace_from_home.set(False)
        self.display_trace_from_home_rez.set(False)
        self.display_trace_from_home_1er.set(False)
        self.display_trace_to_home.set(False)
        self.display_trace_from_bypass.set(False)
        self.display_trace_home_ft.set(False)
        
        # Boiler
        self.display_trace_from_boiler.set(False)
        self.display_trace_to_boiler.set(False)
        self.display_trace_in_boiler.set(False)
        self.display_trace_boiler_ft.set(False)
        
        # ON/OFF PAC et boiler
        self.display_trace_pac_on_off.set(False)
        self.display_trace_boiler_on_off.set(False)
        
        # valeurs sur curseur souris
        self.display_valeur_x.set(False)
        self.display_valeur_y.set(True)
        self.mouse_info = None # pour placer le texte sur le curseur de la sourtis
        
        # memoire de l'ancienne position de la souris
        self.mouse_x = 0
        self.mouse_y = 0
        
        # axe des x curseurs et zoom 
        # création des curseurs dot line sur l'ecran
        self.mouse_events_x = [] # liste des dot lines utiles pendant la création
        self.mouse_cursors_x = [] # liste des dot lines verticales placées
        self.mouse_pos_cursors_x = [] # liste de la position des dot lines verticales
        self.old_date_start = datetime.now() # utiliser pour vérifier que la souris a bougé
        
        #variables pour les différents zooms
        self.zoom_active = False # scale xy amnuel ou automatique
        # entrée de menu pour initialiser le zoom sur une zone
        self.mouse_place_cursor_or_select_area = IntVar(self.tk_root)
        self.mouse_place_cursor_or_select_area.set(False)
        # variables pour les coordonnées de la zone
        self.select_area_x1 = 0
        self.select_area_x2 = 0
        self.select_area_y1 = 0
        self.select_area_y2 = 0
        # utilisé pendant la sélection de la zone
        self.added_rectangle = []
        # index des datas a afficher en cas de zoom x
        self.index_first_displayed_record = 0
        self.index_last_displayed_record = 0
        
        # axe des y curseurs
        self.mouse_events_y = [] # liste des dot lines utiles pendant la création
        self.mouse_cursors_y = [] # liste des dot lines horizontales placées
        self.mouse_pos_cursors_y = [] # liste de la position des dot lines horizontales

        # variables de dimensions
        self.graduation_step = 2
        self.V_PADX = 100 * self.win_width / self.max_width
        self.V_PADY = 75 * self.win_width / self.max_width
        # initialisations pour le graph
        self.X_MIN = self.V_PADX
        self.X_MAX = self.win_width - self.V_PADX
        self.Y_MAX = self.V_PADY
        self.Y_MIN = self.win_height * 0.8 - self.V_PADY
        
        # variables pour les échelles x et y
        self.echelle_x_min = 0
        self.echelle_x_max = 0
        self.echelle_y_min = 0
        self.echelle_y_max = 0

        # variables pour le grid de tkinter
        self.n_col = 32
        self.col_width = int(self.win_width / self.n_col)

        # pad x et y pour les afficheurs
        self.padx = 0
        self.pady = 0

        # Polices 
        self.FONT_LABEL = "".join(["Helvetica ",str(int(13*self.win_width/self.max_width))])
        self.FONT_TEXT = "".join(["Helvetica ",str(int(26*self.win_width/self.max_width))])
        self.FONT_TEXT_MEDIUM = "".join(["Helvetica ",str(int(12*self.win_width/self.max_width))])
        self.FONT_TEXT_SMALL = "".join(["Helvetica ",str(int(10*self.win_width/self.max_width))])
        self.FONT_TEMP = "".join(["Helvetica ",str(int(70*self.win_width/self.max_width))])

        # couleurs
        self.FG_COLOR_TEXT = "black"
        self.FG_COLOR_WAIT = "gray10"
        
        self.COLOR_SALON = "blue"
        self.COLOR_BUREAU = "DarkOrange3"
        self.COLOR_EXT = "green"
        self.COLOR_PAC_VAL = "gray33"
        self.COLOR_PAC = "darkred"
        self.COLOR_PAC_FROM_TO = "purple"
        self.COLOR_PAC_FROM = "fuchsia"
        self.COLOR_ACCU_FROM = "dark orchid"
        self.COLOR_BYPASS_FROM = "light slate blue"
        self.COLOR_BYPASS_TO = "dark slate blue"
        self.COLOR_PAC_TO = "deeppink"
        self.COLOR_BOILER = "chocolate" # "olivedrab"
        self.COLOR_FROM_BOILER = "sandybrown" # "olivedrab"
        self.COLOR_BOILER_FT = "saddlebrown" #"yellowgreen"
        self.COLOR_HOME = "cadetblue"
        self.COLOR_FROM_HOME = "deepskyblue"
        self.COLOR_HOME_FT = "steelblue"
        self.GRID_COLOR = "silver"
        self.RECTANGLE_COLOR = "purple"
        
        self.BG_COLOR = "gray80"
        self.BG_COLOR_DAYS = "snow2"
        self.BG_COLOR_PAC = "lavender"
        self.BG_COLOR_SELECTED = "red"
        self.BG_COLOR_UNUSED = "gray75"
        
        self.CURSOR_X_COLOR = "red" # "gray25"
        self.CURSOR_Y_COLOR = "blue" # "gray50"

        # 1ere ligne de la GRID : les etiquettes des afficheurs de température 
        # salon
        v_column_span = 16
        v_row = 0
        v_column = 0
        tk.Label(self.tk_root,
                 text="Salon",
                 fg = self.FG_COLOR_TEXT,
                 font = self.FONT_TEXT,
                 padx = self.padx,
                 pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        # bureau
        tk.Label(self.tk_root,
                 text="Bureau",
                 fg = self.FG_COLOR_TEXT,
                 font = self.FONT_TEXT,
                 padx = self.padx,
                 pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        # extérieur
        tk.Label(self.tk_root,
                 text="Extérieur",
                 fg = self.FG_COLOR_TEXT,
                 font = self.FONT_TEXT,
                 padx = self.padx,
                 pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        # pac on-off
        tk.Label(self.tk_root,
                 text="PAC on-off",
                 fg = self.FG_COLOR_TEXT,
                 font = self.FONT_TEXT,
                 padx = self.padx,
                 pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        
        # 2eme ligne de la GRID : les afficheurs de température
        v_row = 1
        v_column = 0
        # Paramétrer les afficheurs de température en temps réel
        # Salon
        self.val_temp_salon = StringVar()
        tk.Label(self.tk_root,
                 textvariable=self.val_temp_salon,
                 fg = self.COLOR_SALON,
                 bg = self.BG_COLOR,
                 font = self.FONT_TEMP,
                 padx = self.padx,
                 pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        # Bureau
        v_column += v_column_span
        self.val_temp_bureau = StringVar()
        tk.Label(self.tk_root,
                 textvariable=self.val_temp_bureau,
                 fg = self.COLOR_BUREAU,
                 bg = self.BG_COLOR,
                 font = self.FONT_TEMP,
                 padx = self.padx,
                 pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        # Extérieur
        v_column += v_column_span
        self.val_temp_ext = StringVar()
        tk.Label(self.tk_root,
                 textvariable=self.val_temp_ext,
                 fg = self.COLOR_EXT,
                 bg = self.BG_COLOR,
                 font = self.FONT_TEMP,
                 padx = self.padx,
                 pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        # PAC
        v_column += v_column_span
        self.val_pac = StringVar()
        tk.Label(self.tk_root,
                 textvariable=self.val_pac,
                 fg = self.COLOR_PAC_VAL,
                 bg = self.BG_COLOR,
                 font = self.FONT_TEMP,
                 padx = self.padx,
                 pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        
        # initialisations pour la 3ème ligne de la GRID : les étiquettes des courbes
        v_row = 2
        v_column_span = 4
        v_column = 2
        v_pady = 20
        
        # Afficheurs
        tk.Label(self.tk_root, text = "   --- Salon", pady = v_pady, fg = self.COLOR_SALON, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        tk.Label(self.tk_root, text = "--- Bureau", pady = v_pady, fg = self.COLOR_BUREAU, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        tk.Label(self.tk_root, text = "--- Extérieur", pady = v_pady, fg = self.COLOR_EXT, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        
        tk.Label(self.tk_root, text = " | ", pady = v_pady, fg = 'black', font = self.FONT_LABEL).grid(row=v_row, column=v_column)
        v_column += 1
        
        # PAC
        tk.Label(self.tk_root, text = "--- Fr. PAC", pady = v_pady, fg = self.COLOR_PAC_FROM, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        tk.Label(self.tk_root, text = "--- Fr. accu", pady = v_pady, fg = self.COLOR_ACCU_FROM, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        tk.Label(self.tk_root, text = "--- To PAC", pady = v_pady, fg = self.COLOR_PAC_TO, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        tk.Label(self.tk_root, text = "--- PAC f-t", pady = v_pady, fg = self.COLOR_PAC_FROM_TO, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        
        tk.Label(self.tk_root, text = " | ", pady = v_pady, fg = 'black', font = self.FONT_LABEL).grid(row=v_row, column=v_column)
        v_column += 1
        
        # Home
        tk.Label(self.tk_root, text = "--- Fr. home", pady = v_pady, fg = self.COLOR_FROM_HOME, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        tk.Label(self.tk_root, text = "--- Fr. bypass", pady = v_pady, fg = self.COLOR_BYPASS_FROM, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        tk.Label(self.tk_root, text = "--- To home", pady = v_pady, fg = self.COLOR_HOME, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        tk.Label(self.tk_root, text = "--- Home f-t", pady = v_pady, fg = self.COLOR_HOME_FT, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        
        tk.Label(self.tk_root, text = " | ", pady = v_pady, fg = 'black', font = self.FONT_LABEL).grid(row=v_row, column=v_column)
        v_column += 1
        
        # Boiler
        tk.Label(self.tk_root, text = "--- Fr. boiler", pady = v_pady, fg = self.COLOR_FROM_BOILER, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        tk.Label(self.tk_root, text = "--- To boiler", pady = v_pady, fg = self.COLOR_BOILER, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        tk.Label(self.tk_root, text = "--- Boiler f-t", pady = v_pady, fg = self.COLOR_BOILER_FT, font = self.FONT_LABEL).grid(row=v_row, column=v_column, columnspan=v_column_span)
 
        # initialize le canvas pour le graphique des températures
        self.cnv = tk.Canvas(bg = "azure", height = 0.8 * self.win_height, width = self.win_width)

        # create the menus
        menubar = Menu(self.tk_root)
        filemenu = Menu(menubar, font = self.FONT_LABEL, tearoff=0)
        filemenu.add_command(label="Exit", font = self.FONT_LABEL, command=self.on_exit)
        menubar.add_cascade(label="File", font = self.FONT_LABEL, menu=filemenu)
        
        # menu time
        timemenu = Menu(menubar, tearoff=0)
        timemenu.add_radiobutton(label="6 hours", font = self.FONT_LABEL, variable = self.nbre_days_on_display, value = 0, command = lambda: self.change_days_on_display(0.25))
        timemenu.add_radiobutton(label="12 hours", font = self.FONT_LABEL, variable = self.nbre_days_on_display, value = 1, command = lambda: self.change_days_on_display(0.5))
        timemenu.add_separator()
        timemenu.add_radiobutton(label="1 day", font = self.FONT_LABEL, variable = self.nbre_days_on_display, value = 2, command = lambda: self.change_days_on_display(1))
        timemenu.add_radiobutton(label="2 days", font = self.FONT_LABEL, variable = self.nbre_days_on_display, value = 3, command = lambda: self.change_days_on_display(2))
        timemenu.add_radiobutton(label="4 days", font = self.FONT_LABEL, variable = self.nbre_days_on_display, value = 4, command = lambda: self.change_days_on_display(4))
        timemenu.add_radiobutton(label="7 days", font = self.FONT_LABEL, variable = self.nbre_days_on_display, value = 5, command = lambda: self.change_days_on_display(7))
        timemenu.add_radiobutton(label="14 days", font = self.FONT_LABEL, variable = self.nbre_days_on_display, value = 6, command = lambda: self.change_days_on_display(14))
        timemenu.add_radiobutton(label="30 days", font = self.FONT_LABEL, variable = self.nbre_days_on_display, value = 7, command = lambda: self.change_days_on_display(30))
        menubar.add_cascade(label="X-axis", font = self.FONT_LABEL, menu=timemenu)
        
        # menu courbes de température
        curvesmenu = Menu(menubar, tearoff=0)
        curvesmenu.add_checkbutton(label="Salon", font = self.FONT_LABEL, variable = self.display_trace_salon, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="Bureau", font = self.FONT_LABEL, variable = self.display_trace_bureau, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="Extérieur", font = self.FONT_LABEL, variable = self.display_trace_ext, command = self.change_curves_on_display)
        curvesmenu.add_command(label="Toggle", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("temp"))
        curvesmenu.add_separator()
        curvesmenu.add_checkbutton(label="From PAC", font = self.FONT_LABEL, variable = self.display_trace_from_pac, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="To PAC", font = self.FONT_LABEL, variable = self.display_trace_to_pac, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="From accu", font = self.FONT_LABEL, variable = self.display_trace_from_accu, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="PAC from-to", font = self.FONT_LABEL, variable = self.display_trace_pac_ft, command = self.change_curves_on_display)
        curvesmenu.add_command(label="PAC toggle", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("pac"))
        curvesmenu.add_separator()
        curvesmenu.add_checkbutton(label="On bypass", font = self.FONT_LABEL, variable = self.display_trace_on_bypass, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="To home", font = self.FONT_LABEL, variable = self.display_trace_to_home, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="From home rez", font = self.FONT_LABEL, variable = self.display_trace_from_home_rez, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="From home 1er", font = self.FONT_LABEL, variable = self.display_trace_from_home_1er, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="From home", font = self.FONT_LABEL, variable = self.display_trace_from_home, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="From bypass", font = self.FONT_LABEL, variable = self.display_trace_from_bypass, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="Home from-to", font = self.FONT_LABEL, variable = self.display_trace_home_ft, command = self.change_curves_on_display)
        curvesmenu.add_command(label="Home toggle", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("home"))
        curvesmenu.add_separator()
        curvesmenu.add_checkbutton(label="To boiler", font = self.FONT_LABEL, variable = self.display_trace_to_boiler, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="In boiler", font = self.FONT_LABEL, variable = self.display_trace_in_boiler, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="From boiler", font = self.FONT_LABEL, variable = self.display_trace_from_boiler, command = self.change_curves_on_display)
        curvesmenu.add_checkbutton(label="Boiler from-to", font = self.FONT_LABEL, variable = self.display_trace_boiler_ft, command = self.change_curves_on_display)
        curvesmenu.add_command(label="Boiler toggle", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("boiler"))
        curvesmenu.add_separator()
#         curvesmenu.add_checkbutton(label="PAC on/off", font = self.FONT_LABEL, variable = self.display_trace_pac_on_off, command = self.change_curves_on_display)
#         curvesmenu.add_checkbutton(label="Boiler on/off", font = self.FONT_LABEL, variable = self.display_trace_boiler_on_off, command = self.change_curves_on_display)
#         curvesmenu.add_command(label="On/off toggle", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("on/off"))
#         curvesmenu.add_separator()
        curvesmenu.add_command(label="All", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("all"))
        curvesmenu.add_command(label="Zero", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("zero"))
        menubar.add_cascade(label="Curves", font = self.FONT_LABEL, menu=curvesmenu)
        
        # menu mesures 
        mesuremenu = Menu(menubar, tearoff=0)
        mesuremenu.add_checkbutton(label="Temps", font = self.FONT_LABEL, variable = self.display_valeur_x)
        mesuremenu.add_checkbutton(label="Température", font = self.FONT_LABEL, variable = self.display_valeur_y)
#         mesuremenu.add_separator()
#         mesuremenu.add_command(label="Remove cursors", font = self.FONT_LABEL, command=self.remove_cursors)
        menubar.add_cascade(label="Mesures", font = self.FONT_LABEL, menu=mesuremenu)
        
        # menu zooms
        self.zoommenu = Menu(menubar, tearoff=0)
        self.zoommenu.add_command(label="Zoom x", font = self.FONT_LABEL, command=self.set_x_scale_change)
        self.zoommenu.add_command(label="Zoom y", font = self.FONT_LABEL, command=self.set_y_scale_change)
        self.zoommenu.add_separator()
        self.zoommenu.add_checkbutton(label="Zoom selection", font = self.FONT_LABEL, variable = self.mouse_place_cursor_or_select_area, command=self.select_xy_scale_change)
        self.zoommenu.add_separator()
        self.zoommenu.add_command(label="Supress all zooms", font = self.FONT_LABEL, command=self.supress_all_zooms)
        menubar.add_cascade(label="Zooms", font = self.FONT_LABEL, menu=self.zoommenu)
        
        # menu database
        databasemenu = Menu(menubar, tearoff=0)
        databasemenu.add_radiobutton(label="192.168.1.139", font = self.FONT_LABEL, variable = self.selected_ip,  command=lambda: self.select_database_ip("192.168.1.139"))
        databasemenu.add_radiobutton(label="192.168.1.109", font = self.FONT_LABEL, variable = self.selected_ip, command=lambda: self.select_database_ip("192.168.1.109"))
        databasemenu.add_radiobutton(label="192.168.1.142", font = self.FONT_LABEL, variable = self.selected_ip, command=lambda: self.select_database_ip("192.168.1.142"))
        menubar.add_cascade(label="Data sce", font = self.FONT_LABEL, menu=databasemenu)
        
        # menu aide
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", font = self.FONT_LABEL, command=self.aide)
        helpmenu.add_command(label="About...", font = self.FONT_LABEL, command=self.about)
        menubar.add_cascade(label="Help", font = self.FONT_LABEL, menu=helpmenu)

        # on crée le menu
        self.tk_root.config(menu=menubar)
        print("Initializations completed")

        # initialisation des afficheurs de températures
        t = self.mysql_logger.get_last_mesured_temperature()
        self.time_acquis = t[0]
        self.t_salon = t[1]
        self.t_bureau = t[2]
        self.t_ext = t[3]
        self.pac_on_off = 0 # any value before the first calculus
            
        # Affichage des températures actuelles
        # Salon
        self.val_temp_salon.set("".join([str(round(self.t_salon, 1)), "°C"]))
        # Bureau
        self.val_temp_bureau.set("".join([str(round(self.t_bureau, 1)), "°C"]))
        # Extérieur
        self.val_temp_ext.set("".join([str(round(self.t_ext, 1)), "°C"]))
        # PAC
        self.val_pac.set("".join([str(int(self.pac_on_off)), " %"]))


        # read the database for data's for graph
        print("Loading data's")
        self.refresh_data_and_display(self.NBRE_DAYS_ON_GRAPH)

    # read the new data's and reresh the display
    def refresh_data_and_display(self, nbre_days):

        # interrompre les répétitions        
        self.kill_repetition_job()
        
        self.NBRE_DAYS_ON_GRAPH = nbre_days
        self.nbre_hours_on_graph = self.NBRE_DAYS_ON_GRAPH * 24
        
        # read the database for data's for graph
        self.data_from_db = self.mysql_logger.get_temp_for_graph(self.nbre_hours_on_graph) # nbre_hours_on_graph
        self.data_from_db = list(self.data_from_db)
        
#         # initialize the last id in the graph_data
#         self.last_id = self.data_from_db[len(self.data_from_db) - 1][19]
        self.refresh_display()
        

    # Rafraichissement des valeurs toutes les minutes (l'intevalle peut être égal ou supérieur à celui entre deux acquisitions)
    def refresh_display(self):
        
        t_start = datetime.now() # par défault le graphique se termine à l'instant présent
        row = self.mysql_logger.get_last_mesured_temperature()
#         pdb.set_trace()
#         t_start = row[0]
        # affichage des passes
        self.n_passe += 1
        self.tk_root.title("".join(["TMON on ", self.ip_db_server,": ", "passe:", str(self.n_passe), "--> t=", "{0:.2f}".format(self.t_elapsed.total_seconds()), "[s])"])) 
        
        # initialisation des variables internes
        data_for_graph = []
        # créer la list data_for_graph -> parcourir tous les data's de data_from_db
        for row in self.data_from_db:
            # ajouter à data_for_graph
            
            # ------------------------------------------------------------
            # index dans data_from_db et data_for_graph et noms des champs
            # ------------------------------------------------------------
            # index   db name     designation
            # 0       t0          from pac
            # 1       t1          to pac
            # 2       t2          from accu
            # 3       t3          on bypass
            # 4       t4          to home
            # 5       t5          from home rez
            # 6       t6          from home 1er
            # 7       t7          from home
            # 8       t8          from bypass
            # 9       t9          to boiler
            # 10      t10         in boiler
            # 11      t11         from boiler
            # 12      t12         salon
            # 13      t13         bureau
            # 14      t14         exterieur
            # 15      s10         pump boiler
            # 16      s11         pump home
            # 17      s20         pac on-pff
            # 18      time_stamp
            # 19      id
            # ------------------------------------------------------------
        
            data_for_graph.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                   row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19]])

        # index du dernier enregistrement
        self.last_id = data_for_graph[len(data_for_graph)-1][19]
        
#         old_t_to_boiler = 0 # row[9]
#         old_t_to_home = 0 # row[6]
        
#         # s'il n'y a pas de zoom actif, initialiser les index pour first et last data record
#         if not self.zoom_active:
#             self.index_first_displayed_record = 0
#             self.index_last_displayed_record = len(self.data_from_db)-1
#         
#         # parcourir tous les data's
#         for i, row in enumerate(self.data_from_db):
#             # vérifier si l'index du record est dans la plage des records à afficher
#             
#             if i >= self.index_first_displayed_record and i <= self.index_last_displayed_record:
#                 
#                 # algorithmes pour PAC ON-OFF et boiler on-off
#                 pac_on_off = 0
#                 boil_on_off = 0
# 
#                 # boiler on/off:  en fonction de la pente de la courbe de la temperature 'to_boiler'
#                 if i > 0:
#                     delta_t_to_boiler = row[9] - old_t_to_boiler
#                     if delta_t_to_boiler > 0.25 and abs(delta_t_to_boiler) < 2:
#                         # la valeur correspond à une graduation sur l'affichage
#                         boil_on_off = self.graduation_step
#                 
#                 # PAC on/off : en fonction de la différence de température entre 'pac_from' et 'pac_to'
#                     pac_ft_t = row[2] - row[3] 
#                     delta_t_to_home = row[4] - old_t_to_home
#                     if pac_ft_t > 4 and (boil_on_off == 0): # from pac - to pac > 3 => pac = on
#                         pac_on_off = self.graduation_step
# 
#                     # ajouter à data_for_graph
#                     data_for_graph.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
#                                            row[11], row[12], row[13], row[14], row[15], pac_on_off, boil_on_off, delta_t_to_home * 10, delta_t_to_boiler * 5])
#                     # memorise valeur actuelles pour calcul d/dt    
#                     old_t_to_boiler = row[9]
#                     old_t_to_home = row[4]
#                     
#                 else:
#                     # memorise premières valeur pour calcul d/dt    
#                     old_t_to_boiler = row[9]
#                     old_t_to_home = row[4]
#             
#         # Calcul % PAC ON
#         count_on = 0
#         count_tot = 0
#         for p in data_for_graph:
#             count_tot += 1
#             if p[16] > 0:
#                 count_on += 1
#         if count_tot > 0:
#             self.pac_on_off = count_on / count_tot * 100
#         else:
#             self.pac_on_off = 0
            

        # Affichage des températures actuelles
        # prendre les valeurs du dernier record
        i_last = len(data_for_graph) - 1
        self.t_salon = float(data_for_graph[i_last][12])
        self.t_bureau = float(data_for_graph[i_last][13])
        self.t_ext = float(data_for_graph[i_last][14])
        # Afficher les valeurs
        # Salon
        self.val_temp_salon.set("".join([str(round(self.t_salon, 1)), "°C"]))
        # Bureau
        self.val_temp_bureau.set("".join([str(round(self.t_bureau, 1)), "°C"]))
        # Extérieur
        self.val_temp_ext.set("".join([str(round(self.t_ext, 1)), "°C"]))
        # PAC
        self.val_pac.set("".join([str(int(self.pac_on_off)), " %"]))

        # echelles min et max pour les ordonnées
        if not self.zoom_active:
            self.echelle_y_min , self.echelle_y_max = self.get_minmax_echelle_y(data_for_graph)
        # clculer les graduation pour les labels sur l'axe des y (températures)
        self.graduation_step = self.get_y_graduation_step(self.echelle_y_min , self.echelle_y_max)

        # initialize date and time
        datetime_start_plot = data_for_graph[0][18]
        datetime_start_plot_str = "".join([str(datetime_start_plot.year),"-",str(datetime_start_plot.month),"-", str(datetime_start_plot.day)," ",
                             str(datetime_start_plot.hour),":",str(datetime_start_plot.minute),":",str(datetime_start_plot.second)]) 
        datetime_obj_start_plot = datetime.strptime(datetime_start_plot_str, '%Y-%m-%d %H:%M:%S')

        # initialize canvas
        self.cnv.delete("all")
        self.cnv.grid(row = 3, column = 0, columnspan = 64)
        self.cnv.configure(cursor = "tcross black")

        # prendre en compte les events de la souris pour les zooms et les curseur de mesure
        # bouton gauche
        self.cnv.bind("<ButtonPress-1>", self.on_mouse_manage)
        self.cnv.bind("<ButtonRelease-1>", self.on_mouse_manage)
        self.cnv.bind("<B1-Motion>", self.on_mouse_manage)
        # bouton droit
        self.cnv.bind("<ButtonPress-3>", self.on_mouse_manage)
        self.cnv.bind("<ButtonRelease-3>", self.on_mouse_manage)
        self.cnv.bind("<B3-Motion>", self.on_mouse_manage)
        # bouton du centre
        self.cnv.bind("<ButtonPress-2>", self.on_mouse_manage)
        # mouvement de la souris pour afficher les valeurs sur le curseur de la souris
        self.cnv.bind("<Motion>", self.on_mouse_move)
        
        # create the y axis
        self.cnv.create_line(self.X_MIN, self.Y_MIN, self.X_MIN, self.Y_MAX - self.V_PADX / 2, arrow = tk.LAST) 
        self.cnv.create_text(self.X_MIN / 2, self.Y_MAX / 3, font = self.FONT_LABEL, text = "°C")

        # get the correlation between pixels and celsius
        y_val_to_pix = (self.Y_MAX - self.Y_MIN) / (self.echelle_y_max - self.echelle_y_min)
        
        # PAC label only if PAC or boiler is displayed
        if self.display_trace_pac_on_off.get() or self.display_trace_boiler_on_off.get():
            y_pos = self.echelle_y_min + self.graduation_step / 3
            y_sur_axe =  y_val_to_pix * (y_pos - self.echelle_y_min) + self.Y_MIN
            self.cnv.create_text(self.X_MIN - self.X_MIN / 2, y_sur_axe, font = self.FONT_LABEL, fill=self.COLOR_PAC, text = "PAC\nBoiler")
        
        # temperature labels on the y axe
        y_pos = self.echelle_y_min 
        while y_pos <= self.echelle_y_max:
            y_sur_axe =  y_val_to_pix * (y_pos - self.echelle_y_min) + self.Y_MIN
            self.cnv.create_text(self.X_MIN / 2, y_sur_axe, font = self.FONT_LABEL, text = '{0:.2f}'.format(y_pos))
            self.cnv.create_line(self.X_MIN, y_sur_axe, self.X_MAX, y_sur_axe, dash = (2,2), fill = self.GRID_COLOR)
            y_pos += self.graduation_step

        # draw the x axis, grid and labels
        self.cnv.create_line(self.X_MIN, self.Y_MIN, self.X_MAX + self.V_PADX / 2, self.Y_MIN, arrow = tk.LAST) # axe des abcisses
        
        # labels and grid for x axis
        # allways 12 mark on this axis
        tic_space = self.nbre_hours_on_graph / 12
        # get the correlation between pixels and hours 
        x_val_to_pix = (self.X_MAX - self.X_MIN) / self.nbre_hours_on_graph
        
        # draw the x_axis
        h_count = 0 
        while h_count <= self.nbre_hours_on_graph:
            # draw the grid
            x_pos = h_count * x_val_to_pix + self.X_MIN
            if h_count > 0:
                self.cnv.create_line(x_pos, self.Y_MIN, x_pos, self.Y_MAX, dash = (2,2), fill = self.GRID_COLOR)
            # draw the labels
            tic_date = datetime_obj_start_plot + timedelta(hours = h_count)
            # time
            hm_graph_txt = ":".join([str(tic_date.hour).zfill(2), str(tic_date.minute).zfill(2)])
            self.cnv.create_text(x_pos, self.Y_MIN + 0.66 * self.V_PADY, font = self.FONT_LABEL, text = str(hm_graph_txt))
            # date
            dm_graph_txt = ".".join([str(tic_date.day).zfill(2), str(tic_date.month).zfill(2), str(tic_date.year)[2:]])
            self.cnv.create_text(x_pos, self.Y_MIN + 0.33 * self.V_PADY, font = self.FONT_LABEL, text = str(dm_graph_txt))
            # increment = tic_space
            h_count += tic_space

        # draw the graph
        n_mes = len(data_for_graph)
        x_data_to_pix = (self.X_MAX - self.X_MIN) / n_mes

        # find the x scale min and max for the graph
        no_last_record = len(data_for_graph) - 1
        date_start = data_for_graph[0][18]
        date_end = data_for_graph[no_last_record][18]
        self.echelle_x_min = date_start.timestamp()
        self.echelle_x_max = date_end.timestamp()
        
        # initialize the old_values to 0
        old_y_salon, old_y_bureau, old_y_ext, old_y_from_pac, old_y_to_pac, old_y_from_accu, old_y_to_home, old_y_to_boiler, old_y_home_ft, \
                 old_y_from_bypass, old_y_boiler_ft, old_y_pac_ft, old_y_from_home, old_y_from_boiler = [0.0 for _ in range(14)]
        old_x, old_x,  old_y_onoff = [0.0 for _ in range(3)]
        
        y = 0
        # draw the curves
        for i, mes in enumerate(data_for_graph):
            # but not for the first pass because old value are not correct
            if i > 0: 
                x = i * x_data_to_pix + self.V_PADX
               
                # afficheurs
                if self.display_trace_salon.get() and mes[12] != -333:
                    t_salon = mes[12]
                    y = y_val_to_pix * (t_salon - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_salon, x, y + self.TRACE_WIDTH, width = self.TRACE_WIDTH, fill = self.COLOR_SALON)
                    old_y_salon = y
                if self.display_trace_bureau.get() and mes[13] != -333:
                    t_bureau = mes[13]
                    y = y_val_to_pix * (t_bureau - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_bureau, x, y + self.TRACE_WIDTH, width = self.TRACE_WIDTH, fill = self.COLOR_BUREAU)
                    old_y_bureau = y
                if self.display_trace_ext.get() and mes[14] != -333:
                    t_ext = mes[14]
                    y = y_val_to_pix * (t_ext - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_ext, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_EXT)
                    old_y_ext = y

                # PAC
                if self.display_trace_from_pac.get() and mes[0] != -333:
                    t_from_pac = mes[0]
                    y = y_val_to_pix * (t_from_pac - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_from_pac, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_PAC_FROM)
                    old_y_from_pac = y
                    
                if self.display_trace_to_pac.get() and mes[1] != -333:
                    t_to_pac = mes[1]
                    y = y_val_to_pix * (t_to_pac - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_to_pac, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_PAC_TO)
                    old_y_to_pac = y
         
                if self.display_trace_from_accu.get() and mes[2] != -333:
                    t_from_accu = mes[2]
                    y = y_val_to_pix * (t_from_accu - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_from_accu, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_ACCU_FROM)
                    old_y_from_accu = y
                    
                if self.display_trace_pac_ft.get() and mes[0] != -333 and mes[1] != -333:
                    t_pac_ft = mes[0] - mes[1]
                    y = y_val_to_pix * (t_pac_ft - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_pac_ft, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_PAC_FROM_TO)
                    old_y_pac_ft = y
                    
                # Home
                    
                if self.display_trace_on_bypass.get() and mes[3] != -333:
                    t_on_bypass = mes[3]
                    y = y_val_to_pix * (t_on_bypass - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_on_bypass, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_PAC_TO)
                    old_y_on_bypass = y
                    
                if self.display_trace_to_home.get() and mes[4] != -333:
                    t_to_home = mes[4]
                    y = y_val_to_pix * (t_to_home - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_to_home, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_HOME)
                    old_y_to_home = y
                    
                if self.display_trace_from_home_rez.get() and mes[5] != -333:
                    t_from_home_rez = mes[5]
                    y = y_val_to_pix * (t_from_home_rez - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_from_home_rez, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_HOME)
                    old_y_from_home_rez = y
                    
                if self.display_trace_from_home_1er.get() and mes[6] != -333:
                    t_from_home_1er = mes[6]
                    y = y_val_to_pix * (t_from_home_1er - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_from_home_1er, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_HOME)
                    old_y_from_home_1er = y
                    
                if self.display_trace_from_home.get() and mes[7] != -333:
                    t_from_home = mes[7]
                    y = y_val_to_pix * (t_from_home - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_from_home, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_FROM_HOME)
                    old_y_from_home = y
                    
                if self.display_trace_from_bypass.get() and mes[8] != -333:
                    t_from_bypass = mes[8]
                    y = y_val_to_pix * (t_from_bypass - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_from_bypass, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_BYPASS_FROM)
                    old_y_from_bypass = y
                    
                if self.display_trace_home_ft.get() and mes[4] != -333 and mes[7] != -333:
                    t_to_home = mes[4] - mes[7]
                    y = y_val_to_pix * (t_to_home - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_home_ft, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_HOME_FT)
                    old_y_home_ft = y

                # Boiler
                if self.display_trace_to_boiler.get() and mes[9] != -333:
                    t_to_boiler = mes[9]
                    y = y_val_to_pix * (t_to_boiler - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_to_boiler, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_BOILER)
                    old_y_to_boiler = y
                    
                if self.display_trace_in_boiler.get() and mes[10] != -333:
                    t_in_boiler = mes[10]
                    y = y_val_to_pix * (t_in_boiler - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_in_boiler, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_BOILER)
                    old_y_in_boiler = y
                    
                if self.display_trace_from_boiler.get() and mes[11] != -333:
                    t_from_boiler = mes[11]
                    y = y_val_to_pix * (t_from_boiler - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_from_boiler, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_FROM_BOILER)
                    old_y_from_boiler = y
                    
                if self.display_trace_boiler_ft.get() and mes[9] != -333 and mes[11] != -333:
                    t_to_boiler = mes[9] - mes[11]
                    y = y_val_to_pix * (t_to_boiler - self.echelle_y_min) + self.Y_MIN
                    self.cnv.create_line(old_x, old_y_boiler_ft, x, y + self.TRACE_WIDTH, width=self.TRACE_WIDTH, fill=self.COLOR_BOILER_FT)
                    old_y_boiler_ft = y
                
#                 # graphique PAC ON/OFF
#                 if self.display_trace_pac_on_off.get():
#                     pac_on_off = mes[16]
#                     if pac_on_off != 0:
#                         y = self.Y_MIN + self.graduation_step * y_val_to_pix
#                     else:
#                         y = self.Y_MIN
# 
#                     if i > 0:
#                         self.cnv.create_line(old_x,  old_y_onoff, x, y, width=self.TRACE_WIDTH, fill=self.COLOR_PAC)
#                 
#                 # graphique BOILER ON/OFF
#                 if self.display_trace_boiler_on_off.get():
#                     boil_on_off = mes[17]
#                     if boil_on_off != 0:
#                         y = self.Y_MIN + self.graduation_step * y_val_to_pix
#                         self.cnv.create_line(x, self.Y_MIN, x, y + self.TRACE_WIDTH, width=2*self.TRACE_WIDTH, fill=self.COLOR_BOILER)
#                         
#                 old_y_onoff = y
                old_x = x

            else: # this is the first pass also initialize the old values
                
                old_x = i * x_data_to_pix + self.V_PADX
                
                # afficheurs
                if self.display_trace_salon.get():
                    t_salon = mes[12]
                    old_y_salon = y_val_to_pix * (t_salon - self.echelle_y_min) + self.Y_MIN
                
                if self.display_trace_bureau.get():
                    t_bureau = mes[13]
                    old_y_bureau = y_val_to_pix * (t_bureau - self.echelle_y_min) + self.Y_MIN

                if self.display_trace_ext.get():
                    t_ext = mes[14]
                    old_y_ext = y_val_to_pix * (t_ext - self.echelle_y_min) + self.Y_MIN

                # PAC
                if self.display_trace_from_pac.get():
                    t_from_pac = mes[0]
                    old_y_from_pac = y_val_to_pix * (t_from_pac - self.echelle_y_min) + self.Y_MIN

                if self.display_trace_to_pac.get():
                    t_to_pac = mes[1]
                    old_y_to_pac = y_val_to_pix * (t_to_pac - self.echelle_y_min) + self.Y_MIN
 
                if self.display_trace_from_accu.get():
                    t_from_accu = mes[2]
                    old_y_from_accu = y_val_to_pix * (t_from_accu - self.echelle_y_min) + self.Y_MIN

                if self.display_trace_pac_ft.get():
                    t_pac_ft = mes[0] - mes[1]
                    old_y_pac_ft = y_val_to_pix * (t_pac_ft - self.echelle_y_min) + self.Y_MIN
         
                # home
                if self.display_trace_on_bypass.get():
                    t_on_bypass = mes[3]
                    old_y_on_bypass = y_val_to_pix * (t_on_bypass - self.echelle_y_min) + self.Y_MIN
                    
                if self.display_trace_to_home.get():
                    t_to_home = mes[4]
                    old_y_to_home = y_val_to_pix * (t_to_home - self.echelle_y_min) + self.Y_MIN
                    
                if self.display_trace_from_home_rez.get():
                    t_from_home_rez = mes[5]
                    old_y_from_home_rez = y_val_to_pix * (t_from_home_rez - self.echelle_y_min) + self.Y_MIN
                    
                if self.display_trace_from_home_1er.get():
                    t_from_home_1er = mes[6]
                    old_y_from_home_1er = y_val_to_pix * (t_from_home_1er - self.echelle_y_min) + self.Y_MIN
                    
                if self.display_trace_from_home.get():
                    t_from_home = mes[7]
                    old_y_from_home = y_val_to_pix * (t_from_home - self.echelle_y_min) + self.Y_MIN
                    
                if self.display_trace_from_bypass.get():
                    t_from_bypass = mes[8]
                    old_y_from_bypass = y_val_to_pix * (t_from_bypass - self.echelle_y_min) + self.Y_MIN

                if self.display_trace_home_ft.get():
                    t_to_home = mes[4] - mes[7]
                    old_y_home_ft = y_val_to_pix * (t_to_home - self.echelle_y_min) + self.Y_MIN

                # boiler
                if self.display_trace_to_boiler.get():
                    t_to_boiler = mes[9]
                    old_y_to_boiler = y_val_to_pix * (t_to_boiler - self.echelle_y_min) + self.Y_MIN

                if self.display_trace_in_boiler.get():
                    t_in_boiler = mes[10]
                    old_y_in_boiler = y_val_to_pix * (t_in_boiler - self.echelle_y_min) + self.Y_MIN

                if self.display_trace_from_boiler.get():
                    t_from_boiler = mes[11]
                    old_y_from_boiler = y_val_to_pix * (t_from_boiler - self.echelle_y_min) + self.Y_MIN

                if self.display_trace_boiler_ft.get():
                    t_boiler_ft = mes[9] - mes[11]
                    old_y_boiler_ft = y_val_to_pix * (t_boiler_ft - self.echelle_y_min) + self.Y_MIN
                
#                 # graphique PAC ON/OFF
#                 pac_on_off = mes[16]
#                 if pac_on_off != 0:
#                     old_y_from_home = self.Y_MIN + self.graduation_step * y_val_to_pix
#                 else:
#                     old_y_from_home = self.Y_MIN
#                 
#                 # graphique BOILER ON/OFF
#                 boil_on_off = mes[17]
#                 if boil_on_off != 0:
#                     old_y_from_boiler = self.Y_MIN + self.graduation_step * y_val_to_pix
#                     
#                 old_y_onoff = self.Y_MIN
                old_x = old_x

# tbd #2    --> revoir le calcul de la position des curseur en fonction de l'étendue de l'échelle du temp
#           --> pour le moment les curseurs ne sont pas recréés
#           --> voir tbd #2 dans on_mouse_manage()
#
        # calculate pixels par minute on the x axis 
#         xaxis_secondes = timedelta.total_seconds(date_end - date_start)
#         xaxis_minutes = xaxis_secondes / 60
#         xaxis_pixels = self.X_MAX - self.X_MIN
#         pixels_par_minute = xaxis_pixels / xaxis_minutes
        
        # recréer les curseurs x
#         for i_mouse_pos_cursor, x_pos_cursor in enumerate(self.mouse_pos_cursors_x):
#             
#             if self.n_passe > 2 and (self.old_date_start != date_start):
#                 x_new = x_pos_cursor - pixels_par_minute
#             else:
#                 x_new = x_pos_cursor
#                 
#             self.mouse_cursors_x.append(self.cnv.create_line(x_new, self.Y_MIN, x_new, self.Y_MAX, fill=self.CURSOR_X_COLOR, dash=(2, 4), width = 2))
#             self.mouse_pos_cursors_x[i_mouse_pos_cursor] = x_new
#         
#         # recréer les curseurs y
#         for i_mouse_pos_cursor, y_pos_cursor in enumerate(self.mouse_pos_cursors_y):
#             
#             if self.n_passe > 2 and (self.old_date_start != date_start):
#                 y_new = y_pos_cursor - pixels_par_minute
#             else:
#                 y_new = y_pos_cursor
#                 
#             self.mouse_cursors_y.append(self.cnv.create_line(self.X_MIN, y_new, self.X_MAX, y_new, fill=self.CURSOR_Y_COLOR, dash=(2, 4), width = 2))
#             self.mouse_pos_cursors_y[i_mouse_pos_cursor] = y_new
#             
#         self.old_date_start = date_start
# tbd #2 end
            
        self.t_elapsed = datetime.now() - t_start
        secondes_decimales_str = str(self.t_elapsed).split(".")[1]
        secondes_decimales_float = float(secondes_decimales_str)/1E6
        t_elapsed = int((self.t_elapsed.seconds + secondes_decimales_float) * 1000)
        t_pause = self.t_pause - t_elapsed
                
        # read the database for data's to append to the graph
        # but stop the changes in the daabase while zoom is active
        if not self.zoom_active:
            
            # read the new(s) record(s) in the database
            self.read_data = self.mysql_logger.get_temp_to_complete_graph(self.last_id) # id's bigger than self.last_id
            n_row = len(self.read_data)
            n_removed = 0

            p_str = "".join(["passe:", str(self.n_passe)])
            p_str += "".join([" n_row:", str(n_row), " removed:"])

#             pdb.set_trace()

            # remove the old(s) record(s) in the data_from_db list
            while n_removed < n_row:
                record_to_remove = self.data_from_db[0]
                self.data_from_db.remove(record_to_remove)
                n_removed += 1
                p_str += "".join([str(record_to_remove[0]), "/"])
                
            # and add the now(s) record(s) in the data_from_db list
            p_str += " added:"
            for row in self.read_data:
                self.data_from_db.append(row)
                p_str += "".join([str(row[0]), "/"])
            
            # adapt the id of the last recors
            self.last_id = self.data_from_db[len(self.data_from_db) - 1][1]
            
            p_str += "".join([" last_id:", str(self.last_id)])
            p_str += "".join([" t_pause:", str(t_pause), "ms t_elapsed:", str(t_elapsed), "ms"])
            
            # if more then one record print a message
            if n_row > 1 : print(p_str)

        # pause the program for a while (t_pause) and after that restat it
#         print("".join(["Timer restarted -> Passe:", str(self.n_passe), " - t_elapsed:", str(t_elapsed),
#                        "ms - t_pause:", "{0:.2f}".format(t_pause/1000), "s"]))
        self._job = self.tk_root.after(t_pause, self.refresh_display)


    def select_xy_scale_change(self):
        
        # zoom active --> disable all zoom menu
        # no zoom on zoom possible actualy
        self.zoommenu.entryconfig(0,state=DISABLED)
        self.zoommenu.entryconfig(1,state=DISABLED)
        self.zoommenu.entryconfig(3,state=DISABLED)
        
        if self.mouse_place_cursor_or_select_area.get():
            self.cnv.configure(cursor = "dotbox green")
        else:
            self.cnv.configure(cursor = "tcross black")

    def set_x_scale_change(self):
        
        # open a window
        ask_window = tk.Toplevel(self.tk_root)
        ask_window.geometry("+%d+%d" % (self.win_width/2, self.win_height/2))
        ask_window.title("x_axis")
        
        # initialize the default values
        x_min_date = datetime.fromtimestamp(self.echelle_x_min).strftime('%Y-%m-%d %H:%M:%S')
        x_max_date = datetime.fromtimestamp(self.echelle_x_max).strftime('%Y-%m-%d %H:%M:%S')
        get_x_min = StringVar(ask_window, value = x_min_date)
        get_x_max = StringVar(ask_window, value = x_max_date)
        
        # configure the fileds
        tk.Label(ask_window, text="x min").grid(row = 0, column = 0)
        tk.Entry(ask_window, textvariable = get_x_min).grid(row = 0, column = 1)
        tk.Label(ask_window, text="x max").grid(row = 1, column = 0)
        tk.Entry(ask_window, textvariable = get_x_max).grid(row = 1, column = 1)
        # configure the buttons
        tk.Button(ask_window, text='cancel', command = lambda: self.apply_x_scale_change("cancel", ask_window, \
                                             get_x_min.get(), get_x_max.get())).grid(row = 3)
        tk.Button(ask_window, text='Default', command = lambda: self.apply_x_scale_change("default", ask_window, \
                                             get_x_min.get(), get_x_max.get())).grid(row = 3, column = 1)
        tk.Button(ask_window, text='OK', default = "active",  command = lambda: self.apply_x_scale_change("ok", ask_window, \
                                             get_x_min.get(), get_x_max.get())).grid(row = 3, column = 0, columnspan = 2, sticky = tk.E)

        # show the window
        ask_window.focus_set()
        # trap events
        ask_window.mainloop()

    # apply the x zoom
    def apply_x_scale_change(self, v_choice, ask_window, get_x_min, get_x_max): #, get_graduation_step):
        
        ask_window.destroy()
        
        # convert the date in the appropriate format
        time_begin_mesure = datetime.strptime(get_x_min, '%Y-%m-%d %H:%M:%S')
        time_end_mesure = datetime.strptime(get_x_max, '%Y-%m-%d %H:%M:%S')
        self.nbre_hours_on_graph = abs(time_end_mesure - time_begin_mesure).seconds / 3600

        # set the default value for the zoom
        self.zoom_active = False
        # set the default value for the zoom's menu entry
        menu_state = tk.NORMAL
        
        # ok button pressed
        if v_choice == "ok":
            self.remove_cursors()
            # do not accept x_min > x_max
            if get_x_min > get_x_max:
                msg = "la valeur de x min doit être plus petite que x max"
                tk.messagebox.showwarning("Erreur", msg)
            else:
                # read the database for data's for graph
#                 self.read_data = self.mysql_jo.get_temp_for_graph_begin_end(time_begin_mesure, time_end_mesure) # nbre_hours_on_graph
#                 self.data_from_db: list = []
#                 for row in self.read_data:
#                     self.data_from_db.append(row)
#                 # initialize the last id in the graph_data
#                 self.last_id = self.data_from_db[len(self.data_from_db) - 1][1]
                # values seems to be good so search indexes for min and max
                min_found = False
                max_found = False
                for i, row in enumerate(self.data_from_db):
                    
                    if row[0] >= time_begin_mesure and not min_found:
                        self.index_first_displayed_record = i
                        min_found = True
                        
                    if row[0] >= time_end_mesure and not max_found:
                        self.index_last_displayed_record  = i
                        max_found = True
                # set the zoom indicator
                self.zoom_active = True
                # to disable the zooms menus
                menu_state = tk.DISABLED
                self.refresh_display()
                
        elif v_choice == "default":
            self.refresh_data_and_display(self.NBRE_DAYS_ON_GRAPH)
            self.remove_cursors()
            
        self.zoommenu.entryconfig(0,state=menu_state)
        self.zoommenu.entryconfig(1,state=menu_state)
        self.zoommenu.entryconfig(3,state=menu_state)

    # define the y axis zoom
    def set_y_scale_change(self):
        
        # zoom active --> disable all zoom menu
        # no zoom on zoom possible actualy
        self.zoommenu.entryconfig(0,state=DISABLED)
        self.zoommenu.entryconfig(1,state=DISABLED)
        self.zoommenu.entryconfig(3,state=DISABLED)

        # create the window
        ask_window = tk.Toplevel(self.tk_root)
        ask_window.geometry("+%d+%d" % (self.win_width/2, self.win_height/2))
        ask_window.title("y_axis")
        # initilize the default values
        get_y_min = DoubleVar(ask_window, value = "{0:.2f}".format(self.echelle_y_min))
        get_y_max = DoubleVar(ask_window, value = "{0:.2f}".format(self.echelle_y_max))
        get_graduation_step = DoubleVar(ask_window, value = self.graduation_step)
        # configure the fields
        # y_min
        tk.Label(ask_window, text="y min").grid(row = 0, column = 0)
        tk.Entry(ask_window, textvariable = get_y_min).grid(row = 0, column = 1)
        # y_max
        tk.Label(ask_window, text="y max").grid(row = 1, column = 0)
        tk.Entry(ask_window, textvariable = get_y_max).grid(row = 1, column = 1)
        # y_unit
        tk.Label(ask_window, text="y unite").grid(row = 2, column = 0)
        tk.Entry(ask_window, textvariable = get_graduation_step).grid(row = 2, column = 1)#.selection_range(0, END)
        
        # configure the buttons
        tk.Button(ask_window, text='cancel', command = lambda: self.apply_y_scale_change("cancel", ask_window, \
                                             get_y_min.get(), get_y_max.get(), get_graduation_step.get())) \
                                            .grid(row = 3)
        tk.Button(ask_window, text='Default', command = lambda: self.apply_y_scale_change("default", ask_window, \
                                             get_y_min.get(), get_y_max.get(), get_graduation_step.get())) \
                                            .grid(row = 3, column = 1)
        tk.Button(ask_window, text='OK', default = "active",  command = lambda: self.apply_y_scale_change("ok", ask_window, \
                                             get_y_min.get(), get_y_max.get(), get_graduation_step.get())) \
                                             .grid(row = 3, column = 0, columnspan = 2, sticky = tk.E)
        ask_window.bind('<Return>', lambda x: self.apply_y_scale_change("ok", ask_window, \
                                             get_y_min.get(), get_y_max.get(), get_graduation_step.get()))
        # shoe the formular
        ask_window.focus_set()
        ask_window.mainloop()

    def select_database_ip(self, ip_adress):
        
#         pdb.set_trace()
        self.ip_db_server = ip_adress
        self.mysql_logger = Mysql(self.ip_db_server)
        self.refresh_data_and_display(self.NBRE_DAYS_ON_GRAPH)        

    # fonction appelée par le menu 'curvesmenu' et par la fonction 'select_trace_on_display'
    def change_curves_on_display(self):

        # tuer la tache en cours
        self.kill_repetition_job()
        
        # efface le graphique et affiche working pendant le travail
        self.cnv.delete("all")
        self.cnv.create_text(int(self.win_width/2.25), int(self.win_height/3), font = self.FONT_TEXT, fill = self.FG_COLOR_WAIT, text = "... working ...")
        self.cnv.update()
        
        # mettre à jour l'affichage
        self.refresh_data_and_display(self.NBRE_DAYS_ON_GRAPH)


    # fonction appelée par le menu 'timemenu'
    def change_days_on_display(self, nbre_days):
        
        # tuer la tache en cours
#         self.kill_repetition_job()
        
        # efface le graphique et affiche working pendant le travail
        self.cnv.delete("all")
        self.cnv.create_text(int(self.win_width/2.25), int(self.win_height/3), font = self.FONT_TEXT, fill = self.FG_COLOR_WAIT, text = "... working ...")
        self.cnv.update()
        
        # vider la mémoire des curseurs x
        self.mouse_pos_cursors_x.clear()
        self.mouse_cursors_x.clear()
        
        # vider la mémoire des curseurs y
        self.mouse_pos_cursors_y.clear()
        self.mouse_cursors_y.clear()

        # mettre à jour l'affichage
        self.refresh_data_and_display(nbre_days)


    # affiche les curves sélectionnées par le menu 'curvesmenu'
    def select_trace_on_display(self, who):
        
        if who == "temp": 
            self.display_trace_salon.set(not self.display_trace_salon.get())
            self.display_trace_bureau.set(not self.display_trace_bureau.get())
            self.display_trace_ext.set(not self.display_trace_ext.get())
        
        if who == "pac": 
            self.display_trace_from_pac.set(not self.display_trace_from_pac.get())
            self.display_trace_to_pac.set(not self.display_trace_to_pac.get())
            self.display_trace_from_accu.set(not self.display_trace_from_accu.get())
            self.display_trace_pac_ft.set(not self.display_trace_pac_ft.get())
            
        if who == "home": 
            self.display_trace_on_bypass.set(not self.display_trace_on_bypass.get())
            self.display_trace_to_home.set(not self.display_trace_to_home.get())
            self.display_trace_from_home_rez.set(not self.display_trace_from_home_rez.get())
            self.display_trace_from_home_1er.set(not self.display_trace_from_home_1er.get())
            self.display_trace_from_home.set(not self.display_trace_from_home.get())
            self.display_trace_from_bypass.set(not self.display_trace_from_bypass.get())
            self.display_trace_home_ft.set(not self.display_trace_home_ft.get())
            
        if who == "boiler": 
            self.display_trace_to_boiler.set(not self.display_trace_to_boiler.get())
            self.display_trace_in_boiler.set(not self.display_trace_in_boiler.get())
            self.display_trace_from_boiler.set(not self.display_trace_from_boiler.get())
            self.display_trace_boiler_ft.set(not self.display_trace_boiler_ft.get())

#         if who == "on/off":
#             self.display_trace_pac_on_off.set(not self.display_trace_pac_on_off.get())
#             self.display_trace_boiler_on_off.set(not self.display_trace_boiler_on_off.get())
            
        if who == "zero": 
            self.display_trace_salon.set(False)
            self.display_trace_bureau.set(False)
            self.display_trace_ext.set(False)
        
            self.display_trace_from_pac.set(False)
            self.display_trace_to_pac.set(False)
            self.display_trace_from_accu.set(False)
            self.display_trace_pac_ft.set(False)
            
            self.display_trace_on_bypass.set(False)
            self.display_trace_to_home.set(False)
            self.display_trace_from_home_rez.set(False)
            self.display_trace_from_home_1er.set(False)
            self.display_trace_from_home.set(False)
            self.display_trace_from_bypass.set(False)
            self.display_trace_home_ft.set(False)
            
            self.display_trace_to_boiler.set(False)
            self.display_trace_in_boiler.set(False)
            self.display_trace_from_boiler.set(False)
            self.display_trace_boiler_ft.set(False)
            
#             self.display_trace_pac_on_off.set(False)
#             self.display_trace_boiler_on_off.set(True)
            
        if who == "all": 
            self.display_trace_salon.set(True)
            self.display_trace_bureau.set(True)
            self.display_trace_ext.set(True)
        
            self.display_trace_from_pac.set(True)
            self.display_trace_to_pac.set(True)
            self.display_trace_from_accu.set(True)
            self.display_trace_pac_ft.set(True)
            
            self.display_trace_on_bypass.set(True)
            self.display_trace_to_home.set(True)
            self.display_trace_from_home_rez.set(True)
            self.display_trace_from_home_1er.set(True)
            self.display_trace_from_home.set(True)
            self.display_trace_from_bypass.set(True)
            self.display_trace_home_ft.set(True)
            
            self.display_trace_to_boiler.set(True)
            self.display_trace_in_boiler.set(True)
            self.display_trace_from_boiler.set(True)
            self.display_trace_boiler_ft.set(True)
        
        self.change_curves_on_display()


    # apply the y zoom
    def apply_y_scale_change(self, v_choice, ask_window, get_y_min, get_y_max, get_graduation_step):
        
        # close the window
        ask_window.destroy()
        self.zoom_active = False
        # set the default value for the zoom's menu entry
        menu_state = tk.NORMAL
        
        # ok 
        if v_choice == "ok":
            self.remove_cursors()
            # verify the limits
            if get_y_min > get_y_max:
                # the limits are not ok so cancel the changes
                msg = "la valeur de y min doit être plus petite que y max"
                tk.messagebox.showwarning("Erreur", msg)
            else:
                # the limits are ok so apply the zoom
                self.echelle_y_min = get_y_min
                self.echelle_y_max = get_y_max
                self.graduation_step = get_graduation_step
                self.zoom_active = True
                menu_state = tk.DISABLED
                self.refresh_display()
            
        elif v_choice == "default":
            # reset the graduation to default
            self.graduation_step = self.get_y_graduation_step(self.echelle_y_min, self.echelle_y_max)
            
        # apply the menu status
        self.zoommenu.entryconfig(0,state=menu_state)
        self.zoommenu.entryconfig(1,state=menu_state)
        self.zoommenu.entryconfig(3,state=menu_state)


    def supress_all_zooms(self):
        
        # enable all zooms
        self.zoommenu.entryconfig(0,state=NORMAL)
        self.zoommenu.entryconfig(1,state=NORMAL)
        self.zoommenu.entryconfig(3,state=NORMAL)

        # reinitialize the params ans the datas and display graph
        self.mouse_place_cursor_or_select_area.set(False)
        self.zoom_active = False
        self.graduation_step = self.get_y_graduation_step(self.echelle_y_min, self.echelle_y_max)
        self.refresh_data_and_display(self.NBRE_DAYS_ON_GRAPH)


    def on_mouse_manage(self, event):
        
        # LEFT MOUSE BUTTON
        # left mouse button in the graph --> cursor
        if str(event.type) == "ButtonPress" and event.num == 1 and event.x >= self.X_MIN and event.x <= self.X_MAX:
            
            self.mouse_x = event.x
            self.mouse_y = event.y
            
            if self.mouse_place_cursor_or_select_area.get():
                self.select_area_x1 = event.x
                self.select_area_y1 = event.y
                self.added_rectangle.append(self.cnv.create_rectangle(self.select_area_x1, self.select_area_y1, self.select_area_x1, self.select_area_y1, dash=(2, 4), outline=self.RECTANGLE_COLOR))
            else:
                self.mouse_events_x.append(self.cnv.create_line(event.x, self.X_MIN, event.x, self.X_MAX, fill=self.CURSOR_X_COLOR, dash=(2, 4), width = 2))
            
        # mouse move while left button pressed in the graph --> cursor
        if str(event.type) == "Motion"  and event.state == 272 and event.x >= self.X_MIN and event.x <= self.X_MAX: # state 272 = left button
                
            if self.mouse_place_cursor_or_select_area.get():
                if abs(event.x - self.mouse_x) > 2 or abs(event.y - self.mouse_y) > 2:
                    for rectangle in self.added_rectangle:
                        self.cnv.delete(rectangle)
                    self.select_area_x2 = event.x
                    self.select_area_y2 = event.y
                    self.added_rectangle.append(self.cnv.create_rectangle(self.select_area_x1, self.select_area_y1, self.select_area_x2, self.select_area_y2, dash=(2, 4), outline=self.RECTANGLE_COLOR))
            else:
                if abs(event.x - self.mouse_x) > 2:
                    for mouse_event in self.mouse_events_x:
                        self.cnv.delete(mouse_event)
                    self.mouse_events_x.append(self.cnv.create_line(event.x, self.Y_MIN, event.x, self.Y_MAX, fill=self.CURSOR_X_COLOR, dash=(2, 4), width = 2))
                    self.get_cursor_label(event)
                    self.mouse_x = event.x
                    self.mouse_y = event.y
            
        # mouse button release while left button pressed
        if str(event.type) == "ButtonRelease"  and event.num == 1 and event.x >= self.X_MIN and event.x <= self.X_MAX:
            
            if self.mouse_place_cursor_or_select_area.get():
                
                for rectangle in self.added_rectangle:
                    self.cnv.delete(rectangle)
                self.added_rectangle.clear()

# tbd #2    --> provisoirement on supprime tous les cuseurs de mesure
#           --> voir tbd #2 dans refresh_display()
                self.remove_cursors()
# fin tbd

                self.select_area_x2 = event.x
                self.select_area_y2 = event.y
                if self.select_area_x1 > self.select_area_x2:
                    self.select_area_x1, self.select_area_x2 = self.select_area_x2, self.select_area_x1
                if self.select_area_y1 > self.select_area_y2:
                    self.select_area_y1, self.select_area_y2 = self.select_area_y2, self.select_area_y1

                 # here the zoom to be designed   
                x_min_seconds = (self.select_area_x1 - self.X_MIN) * (self.echelle_x_max - self.echelle_x_min) / (self.X_MAX - self.X_MIN) + self.echelle_x_min
                x_min_date = datetime.fromtimestamp(x_min_seconds).strftime('%Y-%m-%d \n%H:%M:%S')
                x_max_seconds = (self.select_area_x2 - self.X_MIN) * (self.echelle_x_max - self.echelle_x_min) / (self.X_MAX - self.X_MIN) + self.echelle_x_min
                x_max_date = datetime.fromtimestamp(x_max_seconds).strftime('%Y-%m-%d \n%H:%M:%S')
                
                min_found = False
                max_found = False
                for i, row in enumerate(self.data_from_db):
                    
                    if row[0] >= datetime.strptime(x_min_date, '%Y-%m-%d %H:%M:%S') and not min_found:
                        self.index_first_displayed_record = i
                        min_found = True
                        
                    if row[0] >= datetime.strptime(x_max_date, '%Y-%m-%d %H:%M:%S') and not max_found:
                        self.index_last_displayed_record  = i
                        max_found = True
                y_min_celsius = (self.select_area_y1 - self.Y_MIN) * (self.echelle_y_max - self.echelle_y_min) / (self.Y_MAX - self.Y_MIN) + self.echelle_y_min
                y_max_celsius = (self.select_area_y2 - self.Y_MIN) * (self.echelle_y_max - self.echelle_y_min) / (self.Y_MAX - self.Y_MIN) + self.echelle_y_min
                self.echelle_y_min = y_max_celsius
                self.echelle_y_max = y_min_celsius
                self.graduation_step = self.get_y_graduation_step(self.echelle_y_min, self.echelle_y_max)








                self.mouse_place_cursor_or_select_area.set(False)
                self.cnv.configure(cursor = "tcross black")
                
#                 self.man_x_scale = True
#                 self.man_y_scale = True
                self.zoom_active = True
                
#                 self.display_trace_pac_on_off.set(False)
#                 self.display_trace_boiler_on_off.set(False)
                
                self.refresh_display()
            else:
                for mouse_event in self.mouse_events_x:
                    self.cnv.delete(mouse_event)
                self.mouse_events_x.clear()
                    
                self.mouse_cursors_x.append(self.cnv.create_line(event.x, self.Y_MIN, event.x, self.Y_MAX, fill=self.CURSOR_X_COLOR, dash=(2, 4), width = 2))
                self.mouse_pos_cursors_x.append(event.x)

        # RIGHT MOUSE BUTTON
        # right mouse button
        if str(event.type) == "ButtonPress" and event.num == 3 and event.y >= self.Y_MIN and event.y <= self.Y_MAX:
            self.mouse_y = event.y
            self.mouse_events_y.append(self.cnv.create_line(self.X_MIN, event.y, self.X_MAX, event.y, fill=self.CURSOR_Y_COLOR, dash=(2, 4), width = 2))

        # mouse move while right button pressed
        if str(event.type) == "Motion"  and event.state == 1040 and event.y <= self.Y_MIN and event.y >= self.Y_MAX: # state 1040 = right button
            
            if abs(event.y - self.mouse_y) > 2:
                
                for mouse_event in self.mouse_events_y:
                    self.cnv.delete(mouse_event)
                    
                self.mouse_events_y.append(self.cnv.create_line(self.X_MIN, event.y, self.X_MAX, event.y, fill=self.CURSOR_Y_COLOR, dash=(2, 4), width = 2))
                self.mouse_y = event.y

                self.get_cursor_label(event)
            
        # mouse button release while right button pressed
        if str(event.type) == "ButtonRelease"  and event.num == 3 and event.y <= self.Y_MIN and event.y >= self.Y_MAX:
            
            for mouse_event in self.mouse_events_y:
                self.cnv.delete(mouse_event)
            self.mouse_events_y.clear()
                
            self.mouse_cursors_y.append(self.cnv.create_line(self.X_MIN, event.y, self.X_MAX, event.y, fill=self.CURSOR_Y_COLOR, dash=(2, 4), width = 2))
            self.mouse_pos_cursors_y.append(event.y)

        #CENTER MOUSE BUTTOM
        # mouse center button pressed
        if str(event.type) == "ButtonPress" and event.num == 2:
            self.remove_cursors()

    
    def on_mouse_move(self, event):
        
        if abs(event.x - self.mouse_x) > 2:
            self.get_mouse_cursor_label(event)

    def get_mouse_cursor_label(self, event):
                
        shift = 0
        degres_celsius = (event.y - self.Y_MIN) * (self.echelle_y_max - self.echelle_y_min) / (self.Y_MAX - self.Y_MIN) + self.echelle_y_min
        date_heure_seconds = (event.x - self.X_MIN) * (self.echelle_x_max - self.echelle_x_min) / (self.X_MAX - self.X_MIN) + self.echelle_x_min
        date_heure = datetime.fromtimestamp(date_heure_seconds).strftime('%Y-%m-%d \n%H:%M:%S')
        if event.x >= self.X_MIN - 3 and event.x <= self.X_MAX + 3 and event.y >= self.Y_MAX - 3 and event.y <= self.Y_MIN + 3:
            if self.display_valeur_x.get() and self.display_valeur_y.get():
                lbl_text = "".join([date_heure, "\n", str("{0:.1f}".format(degres_celsius)), " °C"])
                shift = 40
            elif self.display_valeur_x.get():
                lbl_text = "".join([date_heure])
                shift = 30
            elif self.display_valeur_y.get():
                lbl_text = "".join([str("{0:.1f}".format(degres_celsius)), " °C"])
                shift = 20
            else:
                lbl_text = ""
        else:
            lbl_text = ""
        self.cnv.delete(self.mouse_info)
        self.mouse_info = self.cnv.create_text(event.x, event.y - shift, text = "", anchor='w')
        self.cnv.itemconfigure(self.mouse_info, text = lbl_text)
    
    def remove_cursors(self):
    
        for mouse_cursor in self.mouse_cursors_x:
            self.cnv.delete(mouse_cursor)
            
        self.mouse_pos_cursors_x.clear()
        self.mouse_cursors_x.clear()
        
        for mouse_cursor in self.mouse_cursors_y:
            self.cnv.delete(mouse_cursor)
            
        self.mouse_pos_cursors_y.clear()
        self.mouse_cursors_y.clear()
        
    def get_y_graduation_step(self, sc_y_min, sc_y_max):
        
        nbre_div = 10
        etendue_echelle = abs(sc_y_max - sc_y_min)
        division = etendue_echelle / nbre_div
        
        if division >= 1:
            n = floor(division)
        else:
            if division > 0.25 :
                n = 0.5
            else:
                n = 0.25
        return n
        

    # calcul arrondi pour echelle y
    def get_minmax_echelle_y(self, graph_data):

        # initialize  scale pour les ordonnées
        y_max = -99999
        y_min = 99999
        for t in graph_data:

        # [0] -> timeStamp [1] -> id [2] -> from PAC [3] -> to PAC [4] -> from accu [5] -> On bypass [6] -> to home [7] -> from home
        # [8] -> from bypass [9] -> to boiler [10] -> from boiler [11] -> salon [12] -> bureau [13] -> ext [14] -> from floor [15] -> from first
        # [16] -> pac on-off [17] -> boiler on-off

            # afficheurs
            if self.display_trace_salon.get() and t[12] != -333:
                y_min = min(y_min, t[12])
                y_max = max(y_max, t[12])
                
            if self.display_trace_bureau.get() and t[13] != -333:
                y_min = min(y_min, t[13])
                y_max = max(y_max, t[13])
                
            if self.display_trace_ext.get() and t[14] != -333:
                y_min = min(y_min, t[14])
                y_max = max(y_max, t[14])
            
            # PAC
            if self.display_trace_from_pac.get() and t[0] != -333:
                y_min = min(y_min, t[0])
                y_max = max(y_max, t[0])
                
            if self.display_trace_to_pac.get() and t[1] != -333:
                y_min = min(y_min, t[1])
                y_max = max(y_max, t[1])
                
            if self.display_trace_from_accu.get() and t[2] != -333:
                y_min = min(y_min, t[2])
                y_max = max(y_max, t[2])
                
            if self.display_trace_pac_ft.get() and t[0] != -333 and t[1] != -333:
                t_delta_pas = t[0] - t[1]
                y_min = min(y_min, t_delta_pas)
                y_max = max(y_max, t_delta_pas)
                
            # home
            if self.display_trace_on_bypass.get() and t[3] != -333:
                y_min = min(y_min, t[3])
                y_max = max(y_max, t[3])
                
            if self.display_trace_to_home.get() and t[4] != -333:
                y_min = min(y_min, t[4])
                y_max = max(y_max, t[4])
                
            if self.display_trace_from_home_rez.get() and t[5] != -333:
                y_min = min(y_min, t[5])
                y_max = max(y_max, t[5])
                
            if self.display_trace_from_home_1er.get() and t[6] != -333:
                y_min = min(y_min, t[6])
                y_max = max(y_max, t[6])
                
            if self.display_trace_from_home.get() and t[7] != -333:
                y_min = min(y_min, t[7])
                y_max = max(y_max, t[7])
                
            if self.display_trace_from_bypass.get() and t[8] != -333:
                y_min = min(y_min, t[8])
                y_max = max(y_max, t[8])
                
            if self.display_trace_home_ft.get() and t[4] != -333 and t[7] != -333:
                t_delta_home = t[4] - t[7]
                y_min = min(y_min, t_delta_home)
                y_max = max(y_max, t_delta_home)
                
            # boiler
            if self.display_trace_to_boiler.get() and t[9] != -333:
                y_min = min(y_min, t[9])
                y_max = max(y_max, t[9])
                 
            if self.display_trace_in_boiler.get() and t[10] != -333:
                y_min = min(y_min, t[10])
                y_max = max(y_max, t[10])
                
            if self.display_trace_from_boiler.get() and t[11] != -333:
                y_min = min(y_min, t[11])
                y_max = max(y_max, t[11])
                
            if self.display_trace_boiler_ft.get() and t[9] != -333 and t[11] != -333:
                t_delta_boiler = t[9] - t[11]
                y_min = min(y_min, t_delta_boiler)
                y_max = max(y_max, t_delta_boiler)
                
        if y_max < y_min:
            y_max = 20
            y_min = 0
                
        if self.display_trace_pac_on_off.get() or self.display_trace_boiler_on_off.get():
            y_min_ret = (y_min // self.graduation_step) * self.graduation_step  - 2 * self.graduation_step
            y_max_ret = (y_max // self.graduation_step) * self.graduation_step
        else:
            y_min_ret = (y_min // self.graduation_step) * self.graduation_step  
            y_max_ret = (y_max // self.graduation_step) * self.graduation_step
            
        if y_max > 0:
            y_max_ret += self.graduation_step
        return y_min_ret, y_max_ret


    def about(self):
        
        tk.messagebox.showinfo \
            ("TMON", "".join([ \
            "Température monitor", "\n\n" \
            "Version no : ", self.VERSION_NO, " du ", self.VERSION_DATE, "\n", \
            "Status : ", self.VERSION_STATUS, "\n", \
            "Auteur : ", self.VERSION_AUTEUR, "\n\n", \
            "Remarque : \n", self.VERSION_DESCRIPTION, "\n"])
            )

    def aide(self):
        
        tk.messagebox.showwarning ("TMON", "".join(["Température monitor", "\n\n", "Aide pas encore rédigée !"]))
        
    def versions(self):
        pass

    def kill_repetition_job(self):
        if self._job is not None:
            self.tk_root.after_cancel(main._job)
            self._job = None
    
    def on_exit(self):
        self.kill_repetition_job()
        self.tk_root.destroy()
        
#     def main(self):
# 
#         # Get screen width and height
#         screenWidth = self.tk_root.winfo_screenwidth()  # width of the screen
#         screenHeight = self.tk_root.winfo_screenheight()  # height of the screen
#         # Calculate the smaller dimention between screen and application
#         maxWidth = min(self.win_width, screenWidth)
#         maxHeight = min(self.win_height, screenHeight)
#         # open the application window in the center horizontaly and to the top verticaly
#         winPosX = (screenWidth / 2) - (int(maxWidth / 2))
#         winPosY = (screenHeight / 2) - (int(maxHeight / 2))
#         # fix the geometry os the formular
#         self.tk_root.geometry('%dx%d+%d+%d' % (maxWidth, maxHeight, winPosX, winPosY))
#         self.tk_root.title("TMON")
#         self.tk_root.protocol("WM_DELETE_WINDOW", self.on_exit)
#         img_tmp="/home/pi/Documents/projets_jo/tempLogger/nest.jpg"
#         img=ImageTk.PhotoImage(Image.open(img_tmp))
#         self.tk_root.call('wm','iconphoto',self.tk_root,img)

################################################################################################################################################################################

if __name__ == '__main__':

    tk_root = tk.Tk()
    main = Main(tk_root)
#     main.main()
        
    tk_root.mainloop()
    
    if main._job is not None:
        main.tk_root.after_cancel(main._job)
        main._job = None


