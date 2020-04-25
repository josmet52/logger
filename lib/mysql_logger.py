#!/usr/bin/env python3
# -*-
"""
    class Mysql to manage de db access for the programm temp_db
"""
import socket
import sys
from tkinter import messagebox
import mysql.connector

# import tkinter as tk
# from datetime import datetime, timedelta
# import time


class Mysql:
    
    """ cette classe sert à accéder à la base de données des températures
        les valeurs sont retournées selon la liste ci-après.
        
        La base de données est sur le RPI 192.168.1.109 et est accessible en local ou par le réseau.
        L'accès à la base de données est vérifiée lors de l'_init et les défauts d'accès sont enregistrés.
        
        [0] -> timeStamp
        [1] -> id
        [2] -> from PAC
        [3] -> to PAC
        [4] -> from accu
        [5] -> to bypass
        [6] -> to home
        [7] -> from home
        [8] -> from bypass
        [9] -> to boiler
        [10] -> from boiler
        [11] -> salon
        [12] -> bureau
        [13] -> ext
        [14] -> from floor
        [15] -> from first
        
        Procédures :
        _init ()
        get_last_mesured_temperature() -> retourne les dernières temperatures acquises
        get_temp_for_graph() -> retourne les températures sur la plage de temps choisie
        get_temp_to_complete_graph() -> retourne les températures acquises après la dernière mise à jour de l'affichage
    """

    def __init__(self, ip_db_server):
        
        # version infos
        VERSION_NO = "0.01.01" 
        VERSION_DATE = "23.04.2020"
        VERSION_DESCRIPTION = "tout au début"
        VERSION_STATUS = "en développement "
        VERSION_AUTEUR = "josmet"
        
        self.database_username = "pi"  # YOUR MYSQL USERNAME, USUALLY ROOT
        self.database_password = "mablonde"  # YOUR MYSQL PASSWORD
        self.database_name = "logger"  # YOUR DATABASE NAME
        self.host_name = "localhost"
        self.server_ip = ip_db_server
        self.record = ""
        # get the local IP adress
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.local_ip = s.getsockname()[0]
        s.close()
        
        con, e = self.get_db_connection(True)
        if not con:
            print("_init_ -> DB UNEXPECTED ERROR\n" + str(e[0]), "/", str(e[1]), "/", str(e[2]) + "\nLe programme va s'arrêter")
            msg = "".join(["ERROR " + str(e[0]), "/ ", str(e[1]), "/ ", str(e[2]) + "Le programme va s'arrêter"])
            tk.messagebox.showerror("DB UNEXPECTED ERROR", msg)
            print("DB UNEXPECTED ERROR", msg)
            exit()
            
    def get_db_connection(self, verbose):
        
        # verify if the mysql server is ok and the db avaliable
        try:
            if self.local_ip == self.server_ip: #.split('.')[3]: # if we are on the RPI with mysql server (RPI making temp acquis)
                # test the local database connection
#                 con = mdb.connect(self.host_name, self.database_username, self.database_password, self.database_name)
                con = mysql.connector.connect(user=self.database_username, password=self.database_password, host=self.host_name, database=self.database_name)
                if verbose: print("".join(['Connected on local DB "', self.database_name, '"']))
            else:
                # test the distant database connection
                con = mysql.connector.connect(user=self.database_username, password=self.database_password, host=self.server_ip, database=self.database_name)
                if verbose: print("".join(['Connected on distant DB "', self.database_name, '" on "', self.server_ip, '"']))
            return con, sys.exc_info()
        
        except:
            # return error
            return False, sys.exc_info()


if __name__ == '__main__':

    # ERROR : direct acces to this class is not ok, reason = ????? (21.04.2020 jm)
    mysql = Mysql('192.168.1.139')
    ip  = mysql.local_ip
    mysql.get_db_connection(True)
