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
    
    """ Cette classe permet d'afficher les graphiques des températures enregistrée dans
        la base de donnée 'logger' (par defaut sur mysql server '192.168.1.139')
        ------------------------------------------------------------
        index : dans data_from_db et data_for_graph
        field name : nom du champ dans la base de donnée
        ------------------------------------------------------------
        index   field name  designation
        0       t0          from pac
        1       t1          to pac
        2       t2          from accu
        3       t3          on bypass
        4       t4          to home
        5       t5          from home rez
        6       t6          from home 1er
        7       t7          from home
        8       t8          from bypass
        9       t9          to boiler
        10      t10         in boiler
        11      t11         from boiler
        12      t12         salon
        13      t13         bureau
        14      t14         exterieur
        15      s10         pump boiler
        16      s11         pump home
        17      s20         pac on-off
        18      s21         boiler on-off
        19      time_stamp  date tiem acquisition
        20      id          id du record 
        ------------------------------------------------------------
    """
    
    def __init__(self, tk_root):

        # version infos
        self.VERSION_NAME = "Monitor" 
        self.VERSION_NO = "2.00.00" 
        self.VERSION_DATE = "06.05.2020"
        self.VERSION_DESCRIPTION = "Improved data processing, much better response times"
        self.VERSION_STATUS = "beta"
        self.VERSION_AUTEUR = "Joseph metrailler"
        
        self.DEBUG = True
        
        # variables de controle
        self._job = None
        self.t_pause = 60000 # 60 secondes 
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

        self.win_pos_x = (self.win_width_th - self.win_width) #/ 2
        self.win_pos_y = (self.win_height_th - self.win_height) / 20
        print("Window size" , self.win_width, "x", self.win_height)
        
        # main windows
        self.tk_root = tk_root
        self.tk_root.geometry("%dx%d+%d+%d" % (self.win_width, self.win_height, self.win_pos_x, self.win_pos_y))
        self.tk_root.configure(background='grey95')
        
        
        self.ip_db_server = "192.168.1.139"
        self.mysql_logger = Mysql(self.ip_db_server)

        # initialisations
        self.NBRE_DAYS_ON_GRAPH = .5/24
        self.nbre_hours_on_graph = self.NBRE_DAYS_ON_GRAPH * 24
        
        # etendue de l'axe du temps (x)
#         self.nbre_days_on_display = IntVar(self.tk_root)
#         if self.NBRE_DAYS_ON_GRAPH == 0.25: self.nbre_days_on_display.set(0)
#         elif self.NBRE_DAYS_ON_GRAPH == 0.5: self.nbre_days_on_display.set(1)
#         elif self.NBRE_DAYS_ON_GRAPH == 1: self.nbre_days_on_display.set(2)
#         elif self.NBRE_DAYS_ON_GRAPH == 2: self.nbre_days_on_display.set(3)
#         elif self.NBRE_DAYS_ON_GRAPH == 4: self.nbre_days_on_display.set(4)
#         elif self.NBRE_DAYS_ON_GRAPH == 7: self.nbre_days_on_display.set(5)
#         elif self.NBRE_DAYS_ON_GRAPH == 14: self.nbre_days_on_display.set(6)
#         elif self.NBRE_DAYS_ON_GRAPH == 30: self.nbre_days_on_display.set(7)
#         else: self.nbre_days_on_display.set(2)

        self.TRACE_WIDTH = 2

        # variable de commande pour l'affichage des différentes traces
        # afficheurs
        self.menu_val = [False if x <12 or x > 18 else True for x in range(22)]
        self.menu_list = [IntVar(tk_root) for i in range(22)]
        for i in range(22):
            self.menu_list[i].set(self.menu_val[i])
        # PAC, Home, Boiler, Afficheurs, States, f-t, toggle
        self.menu_label =['Fr. PAC','To PAC','Fr. accu',
                          'On bypass','To home','Fr. rez','Fr. 1er','Fr. home','Fr. bypass',
                          'To boiler','In boiler','Fr. boiler',
                          'Salon','Bureau','Extérieur',
                          'Pump boiler','Pump home','PAC on-off','Boiler on-off',
                          'PAC f-t','Home t-f','Boiler t-f',
                          'PAC toggle','Home toggle','Boiler toggle','Maison toggle','States toggle',
                          'All','Nothing']
        self.menu_separator =[2, 8, 11, 14, 18, 21, 26]
        self.label_separator =[2, 8, 11, 14, 18]
        # PAC, Home, Boiler, Afficheurs, States, f-t, toggle
        self.menu_color = [self.rgb_color((190, 118, 112)), self.rgb_color((207, 15, 110)), self.rgb_color((19, 36, 161)), self.rgb_color((199, 155, 117)),
                           self.rgb_color((38, 103, 191)), self.rgb_color((162, 41, 10)), self.rgb_color((124, 165, 155)), self.rgb_color((0, 136, 124)), self.rgb_color((242, 18, 44)),
                           self.rgb_color((251, 143, 136)), self.rgb_color((196, 42, 237)), self.rgb_color((174, 175, 150)),
                           self.rgb_color((199, 77, 127)), self.rgb_color((106, 150, 193)), self.rgb_color((32, 110, 224)),
                           self.rgb_color((35, 221, 253)), self.rgb_color((158, 153, 182)), self.rgb_color((255, 0, 0)), self.rgb_color((3, 55, 246)),
                           self.rgb_color((210, 165, 0)), self.rgb_color((239, 2, 193)), self.rgb_color((63, 54, 80)), self.rgb_color((199, 84, 29)), self.rgb_color((200, 200, 200))]
        

        # affichages des valeurs sur le curseur de la souris
        self.display_valeur_x = IntVar(self.tk_root)
        self.display_valeur_y = IntVar(self.tk_root)
        # valeurs sur curseur souris
        self.display_valeur_x.set(False)
        self.display_valeur_y.set(True)
        self.mouse_info = None # pour placer le texte sur le curseur de la sourtis
        
        # choix de la source pour la database
        self.selected_ip = IntVar(self.tk_root)
        self.selected_ip.set(self.ip_db_server)
        
        # memoire de l'ancienne position de la souris
        self.mouse_x = 0
        self.mouse_y = 0
        
        # axe des x curseurs et zoom 
        # création des curseurs dot line sur l'ecran
        self.mouse_events_x = [] # liste des dot lines utiles pendant la création
        self.mouse_cursors_x = [] # liste des dot lines verticales placées
        self.mouse_pos_cursors_x = [] # liste de la position des dot lines verticales
        self.old_date_start = datetime.now() # utiliser pour vérifier que la souris a bougé
        self.mouse_scroll_left = False
        self.mouse_scroll_right = False
        
        #variables pour les différents zooms
        self.zoom_active = False # scale xy amnuel ou automatique
        
        # variables pour les coordonnées de la zone
        self.select_area_x1 = 0
        self.select_area_x2 = 0
        self.select_area_y1 = 0
        self.select_area_y2 = 0
        # utilisé pendant la sélection de la zone
        self.added_rectangle = []
        # index des datas a afficher en cas de zoom x
        self.data_from_db = []
        self.data_for_graph = []
        self.data_for_graph_new = []
        self.id_first_displayed_record = 0
        self.id_last_displayed_record = 0
        self.nbre_records_in_data_from_db = 0
        self.scale_list = []
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

        # pad x et y pour les afficheurs
        self.padx = 20
        self.pady = 0

        # Polices 
        self.FONT_LABEL = "".join(["Helvetica ",str(int(13*self.win_width/self.max_width))])
        self.FONT_TEXT = "".join(["Helvetica ",str(int(26*self.win_width/self.max_width))])
        self.FONT_TEXT_MEDIUM = "".join(["Helvetica ",str(int(12*self.win_width/self.max_width))])
        self.FONT_TEXT_SMALL = "".join(["Helvetica ",str(int(10*self.win_width/self.max_width))])
        self.FONT_TEMP = "".join(["Helvetica ",str(int(70*self.win_width/self.max_width))])
        
        self.GRID_COLOR = "silver"
        self.RECTANGLE_COLOR = "purple"
        
        self.FG_COLOR_TEXT = "black"
        self.FG_COLOR_WAIT = "gray10"
        
        self.BG_COLOR = "grey90"#"gray80"
        self.BG_COLOR_DAYS = "grey95"
        self.BG_COLOR_PAC = "lavender"
        self.BG_COLOR_SELECTED = "red"
        self.BG_COLOR_UNUSED = "gray75"
        self.BG_COLOR_LABEL = "grey95"
        self.COLOR_BG_CANVAS = "gray90" # "azure"       
        self.CURSOR_X_COLOR = "red" # "gray25"
        self.CURSOR_Y_COLOR = "blue" # "gray50"
        # states
        self.COLOR_PUMP_BOILER = self.rgb_color((35, 221, 253))#191, 170, 138))
        self.COLOR_PUMP_HOME = self.rgb_color((158, 153, 182))#168, 186, 213))
        self.COLOR_PAC_ON_OFF = self.rgb_color((255, 0, 0))
        self.COLOR_BOILER_ON_OFF = self.rgb_color((3, 55, 246))


        # variables pour le grid de tkinter
        self.n_col = 64
        self.col_width = int(self.win_width / self.n_col)

        # 1ere ligne de la GRID : les etiquettes des afficheurs de température 
        # salon
        v_column_span = 16
        v_row = 0
        v_column = 0
        tk.Label(self.tk_root, text=self.menu_label[12], fg = self.FG_COLOR_TEXT, bg = self.BG_COLOR_LABEL, font = self.FONT_TEXT,
                 padx = self.padx, pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        # bureau
        tk.Label(self.tk_root, text=self.menu_label[13], fg = self.FG_COLOR_TEXT, bg = self.BG_COLOR_LABEL, font = self.FONT_TEXT,
                 padx = self.padx,pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        # extérieur
        tk.Label(self.tk_root, text=self.menu_label[14], fg = self.FG_COLOR_TEXT, bg = self.BG_COLOR_LABEL, font = self.FONT_TEXT,
                 padx = self.padx, pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        v_column += v_column_span
        # pac on-off
        tk.Label(self.tk_root, text=self.menu_label[17], fg = self.FG_COLOR_TEXT, bg = self.BG_COLOR_LABEL, font = self.FONT_TEXT,
                 padx = self.padx, pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        
        # 2eme ligne de la GRID : les afficheurs de température
        v_row = 1
        v_column = 0
        # Paramétrer les afficheurs de température en temps réel
        # Salon
        self.val_temp_salon = StringVar()
        tk.Label(self.tk_root,
                 textvariable=self.val_temp_salon, fg = self.menu_color[12], bg = self.BG_COLOR, font = self.FONT_TEMP,
                 padx = self.padx, pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        # Bureau
        v_column += v_column_span
        self.val_temp_bureau = StringVar()
        tk.Label(self.tk_root, textvariable=self.val_temp_bureau, fg = self.menu_color[13], bg = self.BG_COLOR, font = self.FONT_TEMP,
                 padx = self.padx, pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        # Extérieur
        v_column += v_column_span
        self.val_temp_ext = StringVar()
        tk.Label(self.tk_root, textvariable=self.val_temp_ext, fg = self.menu_color[14], bg = self.BG_COLOR, font = self.FONT_TEMP,
                 padx = self.padx, pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        # PAC
        v_column += v_column_span
        self.val_pac = StringVar()
        tk.Label(self.tk_root, textvariable=self.val_pac, fg = self.menu_color[17], bg = self.BG_COLOR, font = self.FONT_TEMP,
                 padx = self.padx, pady = self.pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
        
        # initialisations pour la 3ème ligne de la GRID : les étiquettes des courbes
        v_row = 2
        v_column_span = 3
        v_column = 3
        v_pady = 20

        # label en couleur pour identifier les courbes
        for i in range(22):
            if i < 15 or i > 18:
                tk.Label(self.tk_root, text = "--- " + self.menu_label[i], fg = self.menu_color[i], bg = self.BG_COLOR_LABEL, font = self.FONT_LABEL,
                         pady = v_pady).grid(row=v_row, column=v_column, columnspan=v_column_span)
                v_column += v_column_span
                if i in self.label_separator:
                    tk.Label(self.tk_root, text = " || ", pady = v_pady, fg = 'black', bg = self.BG_COLOR_LABEL, font = self.FONT_LABEL
                             ).grid(row=v_row, column=v_column)
                    v_column += 1
 
        # initialize le canvas pour le graphique des températures
        self.cnv = tk.Canvas(bg = self.COLOR_BG_CANVAS, height = 0.8 * self.win_height, width = self.win_width)

        # create the menus
        menubar = Menu(self.tk_root)
        filemenu = Menu(menubar, font = self.FONT_LABEL, tearoff=0)
        filemenu.add_command(label="Exit", font = self.FONT_LABEL, command=self.on_exit)
        menubar.add_cascade(label="File", font = self.FONT_LABEL, menu=filemenu)
        
        # menu time
        timemenu = Menu(menubar, tearoff=0)
        timemenu.add_radiobutton(label="6 hours", font = self.FONT_LABEL, value = 0, command = lambda: self.change_days_on_display(0.25))
        timemenu.add_radiobutton(label="12 hours", font = self.FONT_LABEL, value = 1, command = lambda: self.change_days_on_display(0.5))
        timemenu.add_separator()
        timemenu.add_radiobutton(label="1 day", font = self.FONT_LABEL, command = lambda: self.change_days_on_display(1))
        timemenu.add_radiobutton(label="2 days", font = self.FONT_LABEL, command = lambda: self.change_days_on_display(2))
        timemenu.add_radiobutton(label="4 days", font = self.FONT_LABEL, command = lambda: self.change_days_on_display(4))
        timemenu.add_radiobutton(label="7 days", font = self.FONT_LABEL, command = lambda: self.change_days_on_display(7))
        timemenu.add_radiobutton(label="10 days", font = self.FONT_LABEL, command = lambda: self.change_days_on_display(10))
        timemenu.add_radiobutton(label="30 days", font = self.FONT_LABEL, command = lambda: self.change_days_on_display(30))
        menubar.add_cascade(label="X-axis", font = self.FONT_LABEL, menu=timemenu)
        
        # menu courbes de température
        curvesmenu = Menu(menubar, tearoff=0)
        for i in range(22):
            curvesmenu.add_checkbutton(label=str(i)+"-"+self.menu_label[i], variable=self.menu_list[i], foreground=self.menu_color[i],
                                           command = self.change_curves_on_display)
            if i in self.menu_separator:
                curvesmenu.add_separator()
        curvesmenu.add_command(label="PAC toggle", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("pac"))
        curvesmenu.add_command(label="Home toggle", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("home"))
        curvesmenu.add_command(label="Boiler toggle", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("boiler"))
        curvesmenu.add_command(label="Afficheurs Toggle", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("display"))
        curvesmenu.add_command(label="States Toggle", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("states"))
        curvesmenu.add_separator()
        curvesmenu.add_command(label="All", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("all"))
        curvesmenu.add_command(label="Zero", font = self.FONT_LABEL, command = lambda: self.select_trace_on_display("zero"))
        menubar.add_cascade(label="Curves", font = self.FONT_LABEL, menu=curvesmenu)
        
        # menu mesures 
        self.mesuremenu = Menu(menubar, tearoff=0)
        self.mesuremenu.add_checkbutton(label="Temps", font = self.FONT_LABEL, variable = self.display_valeur_x)
        self.mesuremenu.add_checkbutton(label="Température", font = self.FONT_LABEL, variable = self.display_valeur_y)
        self.mesuremenu.add_separator()
        self.mesuremenu.add_command(label="Zoom x", font = self.FONT_LABEL, command=self.set_x_scale_change)
        self.mesuremenu.add_command(label="Zoom y", font = self.FONT_LABEL, command=self.set_y_scale_change)
        self.mesuremenu.add_separator()
        self.mesuremenu.add_command(label="No Zoom", font = self.FONT_LABEL, command=self.supress_all_zooms)
        self.mesuremenu.add_command(label="No cursors", font = self.FONT_LABEL, command=self.remove_cursors)
        menubar.add_cascade(label="Mesures", font = self.FONT_LABEL, menu=self.mesuremenu)
        
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
        self.refresh_data_and_display(self.NBRE_DAYS_ON_GRAPH)

    # read the new data's and reresh the display
    def refresh_data_and_display(self, nbre_days):

        # interrompre les répétitions        
        self.kill_repetition_job()

#         pdb.set_trace()
        
        # efface le graphique et affiche working pendant le travail
        self.cnv.delete("all")
        self.cnv.grid(row = 3, column = 0, columnspan = 64)
        self.cnv.create_text(int(self.win_width/2.25), int(self.win_height/3), font = self.FONT_TEXT, fill = self.FG_COLOR_WAIT, text = "... loading data ...")
#         self.cnv.update()
        self.cnv.update_idletasks()
        
        self.NBRE_DAYS_ON_GRAPH = nbre_days
        self.nbre_hours_on_graph = self.NBRE_DAYS_ON_GRAPH * 24
        
        # read the database for data's for graph
        t_start = datetime.now()
        t_start_mes = datetime.now()
        self.data_from_db = self.mysql_logger.get_temp_for_graph(self.nbre_hours_on_graph) # nbre_hours_on_graph
        if self.DEBUG:
            print("Loaded data", "{0:.3f}".format((datetime.now() - t_start_mes).total_seconds()),"s")
        t_start_mes = datetime.now()

        self.data_for_graph_new = []
        # sensors
        for sensor in range(len(self.data_from_db[0])-2):
            colonne = []
            for record in range(len(self.data_from_db)):
                colonne.append(self.data_from_db[record][sensor])
            colonne = list(colonne)
            self.data_for_graph_new.append(colonne)
            
        # PAC ft
        tmp = []
        for ix in range(len(self.data_for_graph_new[0])):
            if self.data_for_graph_new[0][ix] == -333 or self.data_for_graph_new[1][ix] == -333:
                tmp.append(-333)
            else:
                tmp.append(self.data_for_graph_new[0][ix] - self.data_for_graph_new[1][ix])
        tmp = list(tmp)
        self.data_for_graph_new.append(tmp)
        
        # Home ft
        tmp = []
        for ix in range(len(self.data_for_graph_new[0])):
            if self.data_for_graph_new[4][ix] == -333 or self.data_for_graph_new[7][ix] == -333:
                tmp.append(-333)
            else:
                tmp.append(self.data_for_graph_new[4][ix] - self.data_for_graph_new[7][ix])
        tmp = list(tmp)
        self.data_for_graph_new.append(tmp)
        
        # Boiler ft
        tmp = []
        for ix in range(len(self.data_for_graph_new[0])):
            if self.data_for_graph_new[11][ix] == -333 or self.data_for_graph_new[9][ix] == -333:
                tmp.append(-333)
            else:
                tmp.append(self.data_for_graph_new[11][ix] - self.data_for_graph_new[9][ix])
        tmp = list(tmp)
        self.data_for_graph_new.append(tmp)
        
        # time and id
        for sensor in range(len(self.data_from_db[0])-2, len(self.data_from_db[0])):
            colonne = []
            for record in range(len(self.data_from_db)):
                colonne.append(self.data_from_db[record][sensor])
            colonne = list(colonne)
            self.data_for_graph_new.append(colonne)
            
        self.data_for_graph_new = list(self.data_for_graph_new)

        # initialize the last id in the graph_data
        self.id_first_displayed_record = min(self.data_for_graph_new[23])
        self.id_last_displayed_record = max(self.data_for_graph_new[23])
        
        self.id_first_fromdb_record = min(self.data_for_graph_new[23])
        self.id_last_fromdb_record = max(self.data_for_graph_new[23])
        
        self.nbre_records_in_data_from_db = len(self.data_for_graph_new[23])
            
        if self.DEBUG:
            print("Data preparation", "{0:.3f}".format((datetime.now() - t_start_mes).total_seconds()),"s")
            print("Total for initialization", "{0:.3f}".format((datetime.now() - t_start).total_seconds()),"s for",
              str(self.NBRE_DAYS_ON_GRAPH), "days and", str(self.NBRE_DAYS_ON_GRAPH*24*60), "records")
        
        self.refresh_display()
        

    # Rafraichissement des valeurs toutes les minutes (l'intevalle peut être égal ou supérieur à celui entre deux acquisitions)
    def refresh_display(self):
        
        t_start = datetime.now() # par défault le graphique se termine à l'instant présent
        t_start_mes = datetime.now()
        
        # affichage des passes
        self.n_passe += 1
        self.tk_root.title("".join(["Monitor passe ", str(self.n_passe)])) #, " t=", "{0:.2f}".format(self.t_elapsed.total_seconds()), "[s])"]))
        
        # dictionnaire qui met en relation l'index du record avec son id
        # usage : record_index = record_dict[record_id]
        record_dict = {}
        record_id = 0
        record_index = 0
        for record_id, record_index in enumerate(self.data_for_graph_new[23]):
#             print(record_index, record_id)
            record_dict[record_index] = record_id
        
        
        # initialisation des variables internes
#         self.data_for_graph = []
        # créer la list data_for_graph -> parcourir tous les data's de data_from_db
        
        # Calcul % PAC ON
        count_on = 0
        count_tot = 0
        for index_pac, pac_onoff in enumerate(self.data_for_graph_new[17]):
            if self.data_for_graph_new[23][index_pac]  >= self.id_first_displayed_record \
               and self.data_for_graph_new[23][index_pac] <= self.id_last_displayed_record: 
                count_tot += 1
                if pac_onoff > 0:
                    count_on += 1
        if count_tot > 0:
            self.pac_on_off = count_on / count_tot * 100
        else:
            self.pac_on_off = 0
        # Affichage des températures actuelles
        # prendre les valeurs du dernier record
        # Les afficheur affichent toujours la dernière valeur mesurée quel que soit l'étendue des courbes affichées
        i_last = self.id_last_displayed_record
        self.t_salon = float(self.data_for_graph_new[12][record_dict[i_last]])
        self.t_bureau = float(self.data_for_graph_new[13][record_dict[i_last]])
        self.t_ext = float(self.data_for_graph_new[14][record_dict[i_last]])
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
            self.echelle_y_min , self.echelle_y_max, self.graduation_step = self.get_minmax_echelle_y(self.data_for_graph_new)
            
        if self.DEBUG:
            print("\nSacaling the graph", "{0:.3f}".format((datetime.now() - t_start_mes).total_seconds()),"s")
        t_start_mes = datetime.now()

        # initialize date and time
#         datetime_start_plot = min(self.data_for_graph_new[22])
        try:
            datetime_start_plot = self.data_for_graph_new[22][record_dict[self.id_first_displayed_record]]
        except:
            pdb.set_trace()
        datetime_start_plot_str = "".join([str(datetime_start_plot.year),"-",str(datetime_start_plot.month),"-", str(datetime_start_plot.day)," ",
                             str(datetime_start_plot.hour),":",str(datetime_start_plot.minute),":",str(datetime_start_plot.second)]) 
        datetime_obj_start_plot = datetime.strptime(datetime_start_plot_str, '%Y-%m-%d %H:%M:%S')

        # initialize canvas
        self.cnv.delete("all")
        self.cnv.grid(row = 3, column = 0, columnspan = 64)
        self.cnv.configure(cursor = "tcross black")
        # recreate cursors if exists
        for mouse_pos_cursor_x in self.mouse_pos_cursors_x:
            if mouse_pos_cursor_x > self.X_MIN:
                self.mouse_cursors_x.append(self.cnv.create_line(mouse_pos_cursor_x, self.Y_MIN, mouse_pos_cursor_x, self.Y_MAX, fill=self.CURSOR_X_COLOR, dash=(2, 4), width = 2))
        for mouse_pos_cursor_y in self.mouse_pos_cursors_y:
            self.mouse_cursors_y.append(self.cnv.create_line(self.X_MIN, mouse_pos_cursor_y, self.X_MAX, mouse_pos_cursor_y, fill=self.CURSOR_Y_COLOR, dash=(2, 4), width = 2))

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
        if self.menu_list[15].get() or self.menu_list[16].get() or self.menu_list[17].get() or self.menu_list[18].get() :
            
            y_sur_axe =  y_val_to_pix * self.graduation_step / 3 * 0.25  + self.Y_MIN 
            self.cnv.create_text(self.X_MIN - self.X_MIN * 0.25, y_sur_axe, font = self.FONT_LABEL, fill=self.COLOR_PAC_ON_OFF, text = "PAC")
            self.cnv.create_text(self.X_MIN - self.X_MIN * 0.75, y_sur_axe, font = self.FONT_LABEL, fill=self.COLOR_BOILER_ON_OFF, text = "Boiler")
            
            y_sur_axe =  y_val_to_pix * self.graduation_step / 3 * 1.75  + self.Y_MIN 
            self.cnv.create_text(self.X_MIN - self.X_MIN * 0.75, y_sur_axe, font = self.FONT_LABEL, fill=self.COLOR_PUMP_BOILER, text = "Boiler")
            self.cnv.create_text(self.X_MIN - self.X_MIN * 0.25, y_sur_axe, font = self.FONT_LABEL, fill=self.COLOR_PUMP_HOME, text = "Home")
            
            min_y_label = self.graduation_step
        else:
            min_y_label = 0
        
        # temperature labels on the y axe
        y_pos = self.echelle_y_min + min_y_label
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
#         n_mes = len(self.data_for_graph_new[0])
        n_mes = self.id_last_displayed_record - self.id_first_displayed_record + 1
        x_data_to_pix = (self.X_MAX - self.X_MIN) / n_mes

        # calculate the x scale min and max for the graph
        no_last_record = record_dict[self.id_last_displayed_record]
        no_first_record = record_dict[self.id_first_displayed_record]
        date_start = self.data_for_graph_new[22][record_dict[self.id_first_displayed_record]]
        date_end = self.data_for_graph_new[22][record_dict[self.id_last_displayed_record]]
        self.echelle_x_min = date_start.timestamp()
        self.echelle_x_max = date_end.timestamp()
        
        
        # initialize the old_values to 0
#         old_y_salon, old_y_bureau, old_y_ext, old_y_from_pac, old_y_to_pac, old_y_from_accu, old_y_to_home, old_y_to_boiler, old_y_home_ft, \
#                  old_y_from_bypass, old_y_boiler_ft, old_y_pac_ft, old_y_from_home, old_y_from_boiler = [0.0 for _ in range(14)]
#         old_x, old_x,  old_y_onoff = [0.0 for _ in range(3)]
            
        if self.DEBUG:
            print("Axes and grids placed", "{0:.3f}".format((datetime.now() - t_start_mes).total_seconds()),"s")
        t_start_mes = datetime.now()
        
        x_dat = []
        point_size = 3
        for i in range(len(self.data_for_graph_new[0]) + 1):
            x_dat.append(i * x_data_to_pix + self.V_PADX)
        
        print("x data ok")
        pump_line_width = 5#(self.X_MAX - self.X_MIN) / self.nbre_hours_on_graph / 60 * 1.2
        pixels_height_for_states = 25
        nbre_pixels_entre_dots = 1
        x_old = 0
        
        for rec_no in range(len(self.data_for_graph_new[0])-1): # pour toutes les mesures des traces
            x_new = x_dat[rec_no]
#             print("rec_no", rec_no)
#             print(int(x_old), int(x_new))
            if (rec_no >= record_dict[self.id_first_displayed_record] and rec_no  <= record_dict[self.id_last_displayed_record]) or rec_no == 0: 
                for trace_no in range(len(self.data_for_graph_new[0])-1): # pour toutes les traces
                    if trace_no < 15 and self.menu_list[trace_no].get():
#                         print("trace_no", trace_no)
                        if rec_no != 0:
                            val_old = self.data_for_graph_new[trace_no][rec_no-1]
                            val_new = self.data_for_graph_new[trace_no][rec_no]
                            if val_new != -333 and val_old != -333:
                                if (x_dat[rec_no] - x_dat[rec_no-1]) > nbre_pixels_entre_dots:
                                    y_old = y_val_to_pix * (val_old - self.echelle_y_min) + self.Y_MIN
                                    y_new = y_val_to_pix * (val_new - self.echelle_y_min) + self.Y_MIN
                                    self.cnv.create_line(x_old, y_old, x_new, y_new + self.TRACE_WIDTH, width = self.TRACE_WIDTH, fill = self.menu_color[trace_no])

#########################################################
#                             pdb.set_trace()
#########################################################
# 
#                         else:
#                             y_old = y_val_to_pix * (self.data_for_graph_new[trace_no][rec_no] - self.echelle_y_min) + self.Y_MIN
            x_old = x_new
                    
        
        
        # temperatures
#         for i_trace, trace in enumerate(self.data_for_graph_new):
#             if i_trace < 15:
#                 if self.menu_list[i_trace].get():
#                     for i_point in range(len(trace)):
#                         if trace[i_point] != -333 and trace[i_point-1] != -333 and i_point > 0 \
#                            and i_point  >= record_dict[self.id_first_displayed_record] \
#                            and i_point  <= record_dict[self.id_last_displayed_record]: 
#                                 
#                             if (x_dat[i_point] - x_old) > nbre_pixels_entre_dots:
#                                 x_new = x_dat[i_point]
#                                 y_new = y_val_to_pix * (trace[i_point] - self.echelle_y_min) + self.Y_MIN
#                                 self.cnv.create_line(x_old, y_old, x_new, y_new + self.TRACE_WIDTH,
#                                                          width = self.TRACE_WIDTH, fill = self.menu_color[i_trace])
# #                                 if (x_dat[i_point] - x_old) > 10:
# #                                     self.cnv.create_oval(x_new-point_size, y_new-point_size, x_new+point_size, y_new+point_size, outline = self.menu_color[i_trace])
#                                 x_old = x_dat[i_point]
#                                 y_old = y_val_to_pix * (trace[i_point] - self.echelle_y_min) + self.Y_MIN
#                         elif i_point == 0:
#                             x_old = x_dat[i_point]
#                             y_old = y_val_to_pix * (trace[i_point] - self.echelle_y_min) + self.Y_MIN
            
            # pumps boiler and pump home
#             elif i_trace >= 15 and i_trace <= 16:
#                 if self.menu_list[i_trace].get():
#                     for i_point in range(len(trace)):
#                         if trace[i_point] != -1 and trace[i_point-1] != -1 and i_point > 0 \
#                            and i_point  >= record_dict[self.id_first_displayed_record] \
#                            and i_point  <= record_dict[self.id_last_displayed_record]: 
#                             if (x_dat[i_point] - x_old) > nbre_pixels_entre_dots:
#                                 x_new = x_dat[i_point]
#                                 y_new = self.Y_MIN - pixels_height_for_states * trace[i_point]
#                                 self.cnv.create_line(x_new, self.Y_MIN, x_new, y_new, width =pump_line_width, fill = self.menu_color[i_trace])
#                         elif i_point == 0:
#                             x_old = x_dat[i_point]
#                             y_old = self.Y_MIN
                             
            # PAC on-off
#             elif i_trace == 17 :
#                 if self.menu_list[i_trace].get():
#                     for i_point in range(len(trace)):
#                         if trace[i_point] == 1 and i_point > 0 \
#                            and i_point  >= record_dict[self.id_first_displayed_record] \
#                            and i_point  <= record_dict[self.id_last_displayed_record]: 
#                             if (x_dat[i_point] - x_old) > nbre_pixels_entre_dots:
#                                 x_new = x_dat[i_point]
#                                 self.cnv.create_line(x_old, self.Y_MIN + 2.5, x_new, self.Y_MIN + 2.5 , width =pump_line_width, fill = self.menu_color[i_trace])
#                         else:
#                             x_old = x_dat[i_point]


            # Boiler on-off
#             elif i_trace == 18 :
#                 if self.menu_list[i_trace].get():
#                     for i_point in range(len(trace)):
#                         if (trace[i_point] == 1 and i_point > 0) \
#                            and i_point  >= record_dict[self.id_first_displayed_record] \
#                            and i_point  <= record_dict[self.id_last_displayed_record]: 
#                             if (x_dat[i_point] - x_old) > nbre_pixels_entre_dots:
#                                 x_new = x_dat[i_point]
#                                 self.cnv.create_line(x_old, self.Y_MIN + 8, x_new, self.Y_MIN + 8 , width =pump_line_width, fill = self.menu_color[i_trace])
#                         else:
#                             x_old = x_dat[i_point]
                            
#             elif i_trace > 18 and i_trace < 22:
#                 if self.menu_list[i_trace].get():
#                     for i_point in range(len(trace)):
#                         if trace[i_point] != -333 and trace[i_point-1] != -333 and i_point > 0 \
#                            and i_point  >= record_dict[self.id_first_displayed_record] \
#                            and i_point  <= record_dict[self.id_last_displayed_record]: 
#                             if (x_dat[i_point] - x_old) > nbre_pixels_entre_dots:
#                                 x_new = x_dat[i_point]
#                                 y_new = y_val_to_pix * (trace[i_point] - self.echelle_y_min) + self.Y_MIN
#                                 self.cnv.create_line(x_old, y_old, x_new, y_new + self.TRACE_WIDTH,
#                                                          width = self.TRACE_WIDTH, fill = self.menu_color[i_trace])
#                                 if (x_dat[i_point] - x_old) > 10:
#                                     self.cnv.create_oval(x_new-point_size, y_new-point_size, x_new+point_size, y_new+point_size, outline = self.menu_color[i_trace])
#                                 x_old = x_dat[i_point]
#                                 y_old = y_val_to_pix * (trace[i_point] - self.echelle_y_min) + self.Y_MIN
#                         elif i_point == 0:
#                             x_old = x_dat[i_point]
#                             y_old = y_val_to_pix * (trace[i_point] - self.echelle_y_min) + self.Y_MIN
                            
                
        
        if self.DEBUG:
            print("Plotted curves", "{0:.3f}".format((datetime.now() - t_start_mes).total_seconds()),"s")
        t_start_mes = datetime.now()
        
        # read the database for data's to append to the graph
        # but stop the changes in the daabase while zoom is active
        n_row = 0
        if not self.zoom_active:
            
            # read the new(s) record(s) in the database
            read_data = self.mysql_logger.get_temp_to_complete_graph(self.id_last_fromdb_record)
            read_data = list(read_data)
            # id's bigger than self.id_last_fromdb_record
            n_row = len(read_data)
            n_removed = 0
            
            if n_row > 0:

                # remove the old(s) record(s) in the data_from_db list
                while n_removed < n_row:
                    for i_sensor in range(len(self.data_for_graph_new)):
                        del self.data_for_graph_new[i_sensor][0]
                    n_removed += 1
                    
                # and add the now(s) record(s) in the data_from_db list
                for row in read_data:
                    for i_field, field in enumerate(row):
                        if i_field < 19:
                            self.data_for_graph_new[i_field].append(field)

                    # PAC ft
                    if row[0] == -333 or row[1] == -333:
                        tmp = -333
                    else:
                        tmp = row[0] - row[1]
                    self.data_for_graph_new[19].append(tmp)
                
                    # Home ft
                    if row[4] == -333 or row[7] == -333:
                        tmp = -333
                    else:
                        tmp = row[4] - row[7]
                    self.data_for_graph_new[20].append(tmp)
                
                    # Boiler ft
                    if row[11] == -333 or row[9] == -333:
                        tmp = -333
                    else:
                        tmp = row[11] - row[9]
                    self.data_for_graph_new[21].append(tmp)
            
                # time and id
                self.data_for_graph_new[22].append(row[19])
                self.data_for_graph_new[23].append(row[20])
                    
                # adapt the id of the last records
                self.id_last_fromdb_record = max(self.data_for_graph_new[23])
                self.id_last_displayed_record = self.id_last_fromdb_record
            
            # recreate cursors if exists
            pixels_pro_minute = (self.X_MAX - self.X_MIN) / self.nbre_hours_on_graph / 60
            pixels_shift_left = n_removed * pixels_pro_minute

            tmp_mouse_pos_cursors_x = list(self.mouse_pos_cursors_x)
            self.mouse_pos_cursors_x.clear()
            self.mouse_cursors_x.clear()

            for mouse_pos_cursor_x in tmp_mouse_pos_cursors_x:
                new_x = mouse_pos_cursor_x - pixels_shift_left
                self.mouse_pos_cursors_x.append(new_x)
                
            self.mouse_cursors_y.clear()
            for mouse_pos_cursor_y in self.mouse_pos_cursors_y:
                self.mouse_cursors_y.append(self.cnv.create_line(self.X_MIN, mouse_pos_cursor_y, self.X_MAX, mouse_pos_cursor_y,
                                                                 fill=self.CURSOR_Y_COLOR, dash=(2, 4), width = 2))
                            
        self.t_elapsed = datetime.now() - t_start
        secondes_decimales_str = str(self.t_elapsed).split(".")[1]
        secondes_decimales_float = float(secondes_decimales_str)/1E6
        t_elapsed = int((self.t_elapsed.seconds + secondes_decimales_float) * 1000)
        t_pause = self.t_pause - t_elapsed
        
        if self.DEBUG:
            print("".join(["Pass ", str(self.n_passe), " - new records ", str(n_row),
                       " - total pass time ", "{0:.3f}".format((datetime.now() - t_start).total_seconds()),"s"]))

        # pause the program for a while (t_pause) and after that restat it
        self._job = self.tk_root.after(t_pause, self.refresh_display)

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
        tk.Button(ask_window, text='cancel', command = lambda: self.apply_x_scale_change(" cancel ", ask_window, \
                                             get_x_min.get(), get_x_max.get())).grid(row = 3, sticky = tk.W)
        tk.Button(ask_window, text='Default', command = lambda: self.apply_x_scale_change("default", ask_window, \
                                             get_x_min.get(), get_x_max.get())).grid(row = 3, column = 1)
        tk.Button(ask_window, text='OK', default = "active",  command = lambda: self.apply_x_scale_change("ok", ask_window, \
                                             get_x_min.get(), get_x_max.get())).grid(row = 3, column = 0, columnspan = 2, sticky = tk.E)

        # show the window and start event trapper
        ask_window.focus_set()
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
        
        # ok button pressed
        if v_choice == "ok":
            self.remove_cursors()
            # do not accept x_min > x_max
            if get_x_min > get_x_max:
                msg = "la valeur de x min doit être plus petite que x max"
                tk.messagebox.showwarning("Erreur", msg)
            else:
                # values seems to be good so search indexes for min and max
                min_found = False
                max_found = False
                for i, row in enumerate(self.data_from_db):
                    
                    if row[22] >= time_begin_mesure and not min_found:
                        self.id_first_displayed_record = i
                        min_found = True
                        
                    if row[22] >= time_end_mesure and not max_found:
                        self.id_last_displayed_record  = i
                        max_found = True
                # set the zoom indicator
                self.zoom_active = True
                # to disable the zooms menus
                self.refresh_display()
                
        elif v_choice == "default":
            self.refresh_data_and_display(self.NBRE_DAYS_ON_GRAPH)
            self.remove_cursors()

    # define the y axis zoom
    def set_y_scale_change(self):
        
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
        
        self.ip_db_server = ip_adress
        self.mysql_logger = Mysql(self.ip_db_server)
        self.refresh_data_and_display(self.NBRE_DAYS_ON_GRAPH)        

    # fonction appelée par le menu 'curvesmenu' et par la fonction 'select_trace_on_display'
    def change_curves_on_display(self):

        # tuer la tache en cours
        self.kill_repetition_job()
        
        # efface le graphique et affiche working pendant le travail
        self.cnv.delete("all")
        self.cnv.create_text(int(self.win_width/2.25), int(self.win_height/3), font = self.FONT_TEXT, fill = self.FG_COLOR_WAIT, text = "... loading data ...")
        self.cnv.update()
        
        # mettre à jour l'affichage
        self.refresh_display()

    # fonction appelée par le menu 'timemenu'
    def change_days_on_display(self, nbre_days):
        
        # tuer la tache en cours
        self.kill_repetition_job()
        
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
        
        if who == "pac":
            self.menu_list[0].set(not self.menu_list[0].get())
            self.menu_list[1].set(not self.menu_list[1].get())
            self.menu_list[2].set(not self.menu_list[2].get())
            
        if who == "home": 
            self.menu_list[3].set(not self.menu_list[3].get())
            self.menu_list[4].set(not self.menu_list[4].get())
            self.menu_list[5].set(not self.menu_list[5].get())
            self.menu_list[6].set(not self.menu_list[6].get())
            self.menu_list[7].set(not self.menu_list[7].get())
            self.menu_list[8].set(not self.menu_list[8].get())
            
        if who == "boiler": 
            self.menu_list[9].set(not self.menu_list[9].get())
            self.menu_list[10].set(not self.menu_list[10].get())
            self.menu_list[11].set(not self.menu_list[11].get())
        
        if who == "display": 
            self.menu_list[12].set(not self.menu_list[12].get())
            self.menu_list[13].set(not self.menu_list[13].get())
            self.menu_list[14].set(not self.menu_list[14].get())

        if who == "states":
            self.menu_list[15].set(not self.menu_list[15].get())
            self.menu_list[16].set(not self.menu_list[16].get())
            self.menu_list[17].set(not self.menu_list[17].get())
            self.menu_list[18].set(not self.menu_list[18].get())
            
        if who == "zero":
            for ix in range(22):
                self.menu_list[ix].set(False)
           
        if who == "all": 
            for ix in range(22):
                self.menu_list[ix].set(True)
        
        self.change_curves_on_display()


    # apply the y zoom
    def apply_y_scale_change(self, v_choice, ask_window, get_y_min, get_y_max, get_graduation_step):
        
        # close the window
        ask_window.destroy()
        self.zoom_active = False
        
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
                self.refresh_display()
            
        elif v_choice == "default":
            # reset the graduation to default
            self.graduation_step = self.get_y_graduation_step(self.echelle_y_min, self.echelle_y_max)

    def supress_all_zooms(self):

        # reinitialize the params ans the datas and display graph
        self.remove_cursors()
        self.zoom_active = False
        self.graduation_step = self.get_y_graduation_step(self.echelle_y_min, self.echelle_y_max)
        self.refresh_data_and_display(self.NBRE_DAYS_ON_GRAPH)


    def on_mouse_manage(self, event):

        # LEFT MOUSE BUTTON
        # left mouse button in the graph area --> rectangle pour zoom
        if str(event.type) == "ButtonPress" and event.num == 1 and event.x >= self.X_MIN and event.x <= self.X_MAX:
            
            self.mouse_x = event.x
            self.mouse_y = event.y
            
            self.select_area_x1 = event.x
            self.select_area_y1 = event.y
            self.added_rectangle.append(self.cnv.create_rectangle(self.select_area_x1, self.select_area_y1, self.select_area_x1, self.select_area_y1, dash=(2, 4), outline=self.RECTANGLE_COLOR))

        # left mouse button on the left or right outside of the graph area --> scroll
        elif str(event.type) == "ButtonPress" and event.num == 1 and (event.x < self.X_MIN or event.x > self.X_MAX):
            
            if self.mouse_scroll_left and (self.id_first_displayed_record > self.id_first_fromdb_record ):
                self.id_first_displayed_record -= 1
                self.id_last_displayed_record -= 1
                self.refresh_display()
                self.cnv.configure(cursor = "sb_left_arrow")

            if self.mouse_scroll_right and (self.id_last_displayed_record < self.id_last_fromdb_record):
                self.id_first_displayed_record += 1
                self.id_last_displayed_record += 1
                self.refresh_display()
                self.cnv.configure(cursor = "sb_right_arrow")
            
        # mouse move while left button pressed in the graph --> cursor
        if str(event.type) == "Motion"  and event.state == 272 and event.x >= self.X_MIN and event.x <= self.X_MAX: # state 272 = left button
            if abs(event.x - self.mouse_x) > 2 or abs(event.y - self.mouse_y) > 2:
                for rectangle in self.added_rectangle:
                    self.cnv.delete(rectangle)
                self.select_area_x2 = event.x
                self.select_area_y2 = event.y
                self.added_rectangle.append(self.cnv.create_rectangle(self.select_area_x1, self.select_area_y1, self.select_area_x2, self.select_area_y2, dash=(2, 4), outline=self.RECTANGLE_COLOR))
            
        # mouse button release while left button pressed
        if str(event.type) == "ButtonRelease"  and event.num == 1 \
        and event.x >= self.X_MIN and event.x <= self.X_MAX \
        and abs(self.select_area_x1 - event.x) > 10 \
        and abs(self.select_area_y1 - event.y) > 10:
                
            self.kill_repetition_job()
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
            x_min_date = datetime.fromtimestamp(x_min_seconds).strftime('%Y-%m-%d %H:%M:%S')
            x_min_date = datetime.strptime(x_min_date, '%Y-%m-%d %H:%M:%S')
            
            x_max_seconds = (self.select_area_x2 - self.X_MIN) * (self.echelle_x_max - self.echelle_x_min) / (self.X_MAX - self.X_MIN) + self.echelle_x_min
            x_max_date = datetime.fromtimestamp(x_max_seconds).strftime('%Y-%m-%d %H:%M:%S')
            x_max_date = datetime.strptime(x_max_date, '%Y-%m-%d %H:%M:%S')

            self.nbre_hours_on_graph = abs(x_max_date - x_min_date).seconds / 3600
            
            min_found = False
            max_found = False
            for i_row in range(len(self.data_for_graph_new[23])):
                
                if self.data_for_graph_new[22][i_row] >= x_min_date and not min_found:
                    self.id_first_displayed_record = self.data_for_graph_new[23][i_row]
                    min_found = True
                    
                if self.data_for_graph_new[22][i_row] >= x_max_date and not max_found:
                    self.id_last_displayed_record = self.data_for_graph_new[23][i_row]
                    max_found = True
            
            y_min_celsius = (self.select_area_y1 - self.Y_MIN) * (self.echelle_y_max - self.echelle_y_min) / (self.Y_MAX - self.Y_MIN) + self.echelle_y_min
            y_max_celsius = (self.select_area_y2 - self.Y_MIN) * (self.echelle_y_max - self.echelle_y_min) / (self.Y_MAX - self.Y_MIN) + self.echelle_y_min
            self.echelle_y_min = y_max_celsius
            self.echelle_y_max = y_min_celsius
            
            self.graduation_step = self.get_y_graduation_step(self.echelle_y_min, self.echelle_y_max)

            self.cnv.configure(cursor = "tcross black")
            self.zoom_active = True
                
#################################
#             pdb.set_trace()
#################################
            
            self.refresh_display()

        # RIGHT MOUSE BUTTON
        # right mouse button
        if str(event.type) == "ButtonPress" and event.num == 3 and event.y >= self.Y_MIN and event.y <= self.Y_MAX:
            self.mouse_y = event.y
            self.mouse_events_x.append(self.cnv.create_line(event.x, self.X_MIN, event.x, self.X_MAX, fill=self.CURSOR_X_COLOR, dash=(2, 4), width = 2))

        # mouse move while right button pressed
        if str(event.type) == "Motion"  and event.state == 1040 and event.y <= self.Y_MIN and event.y >= self.Y_MAX: # state 1040 = right button
            
            if abs(event.y - self.mouse_y) > 2:
                
                for mouse_event in self.mouse_events_y:
                    self.cnv.delete(mouse_event)

                for mouse_event in self.mouse_events_x:
                    self.cnv.delete(mouse_event)
                self.mouse_events_x.append(self.cnv.create_line(event.x, self.Y_MIN, event.x, self.Y_MAX, fill=self.CURSOR_X_COLOR, dash=(2, 4), width = 2))
                self.get_mouse_cursor_label(event)
                self.mouse_x = event.x
                self.mouse_y = event.y

        # mouse button release while right button pressed
        if str(event.type) == "ButtonRelease"  and event.num == 3 and event.y <= self.Y_MIN and event.y >= self.Y_MAX:
            
            for mouse_event in self.mouse_events_y:
                self.cnv.delete(mouse_event)
            self.mouse_events_y.clear()

            for mouse_event in self.mouse_events_x:
                self.cnv.delete(mouse_event)
            self.mouse_events_x.clear()
                
            self.mouse_cursors_x.append(self.cnv.create_line(event.x, self.Y_MIN, event.x, self.Y_MAX, fill=self.CURSOR_X_COLOR, dash=(2, 4), width = 2))
            self.mouse_pos_cursors_x.append(event.x)

        #CENTER MOUSE BUTTOM
        # mouse center button pressed
        if str(event.type) == "ButtonPress" and event.num == 2:
            self.remove_cursors()
            self.supress_all_zooms()

    
    def on_mouse_move(self, event):
        
        if abs(event.x - self.mouse_x) > 2:
            self.get_mouse_cursor_label(event)
        if event.x < self.X_MIN and (self.id_first_displayed_record > self.id_first_fromdb_record):
            self.cnv.configure(cursor = "sb_left_arrow")
            self.mouse_scroll_left = True
        elif event.x > self.X_MAX and (self.id_last_displayed_record < self.id_last_fromdb_record):
            self.cnv.configure(cursor = "sb_right_arrow")
            self.mouse_scroll_right = True
        else:
            self.cnv.configure(cursor = "tcross black")#"crosshair")
            self.mouse_scroll_left = False
            self.mouse_scroll_right = False


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
        
        nbre_div = 9
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

#     def get_min_max(self, sensor_data):
#         
#         tmp = []
#         for i, l in enumerate(sensor_data):
#             if l != -333:
#                 tmp.append(l)
#                 
#         y_min = min(tmp)
#         y_max = max(tmp)
#         
#         return [y_min, y_max]
        

    # calcul arrondi pour echelle y
    def get_minmax_echelle_y(self, graph_data):

        
        for ix in range(len(graph_data)-2):
            tmp = []
            for ind, val in enumerate(graph_data[ix]):
                if graph_data[23][ind] >= self.id_first_fromdb_record and graph_data[23][ind] <= self.id_last_fromdb_record:
                    if val != -333:
                        tmp.append(val)
            y_min = min(tmp)
            y_max = max(tmp)
            self.scale_list.append([y_min, y_max])
        
        y_min = 9999999
        y_max = -9999999
        for ix, vx in enumerate(self.menu_list):
            if vx.get() and (ix < 15 or ix > 18):
                y_min = min(y_min, self.scale_list[ix][0])
                y_max = max(y_max, self.scale_list[ix][1])
        
        if y_max < y_min:
            y_max = 20
            y_min = 0
                
        graduation_step = self.get_y_graduation_step(y_min , y_max)        
                
        if self.menu_list[15].get() or self.menu_list[16].get() or self.menu_list[17].get() or self.menu_list[18].get() :
            y_min_ret = (y_min // graduation_step) * graduation_step  - 2 * graduation_step
            y_max_ret = (y_max // graduation_step) * graduation_step
        else:
            y_min_ret = (y_min // graduation_step) * graduation_step  
            y_max_ret = (y_max // graduation_step) * graduation_step
            
        if y_max > 0:
            y_max_ret += graduation_step

        return y_min_ret, y_max_ret, graduation_step

    def rgb_color(self, rgb):
        
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb   


    def about(self):
        
        tk.messagebox.showinfo \
            ("Monitor", "".join([ \
            "Temperature monitor", "\n\n" \
            "Version no : ", self.VERSION_NO, " du ", self.VERSION_DATE, "\n", \
            "Status : ", self.VERSION_STATUS, "\n", \
            "Author : ", self.VERSION_AUTEUR, "\n\n", \
            "Note : \n", self.VERSION_DESCRIPTION, "\n"])
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

################################################################################################################################################################################

if __name__ == '__main__':

    tk_root = tk.Tk()
    main = Main(tk_root)
        
    tk_root.mainloop()
    
    if main._job is not None:
        main.tk_root.after_cancel(main._job)
        main._job = None


