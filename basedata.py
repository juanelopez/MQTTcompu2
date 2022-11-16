#!/usr/bin/python3
from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
#from concurrent import futures
import os
#hilos = futures.ThreadPoolExecutor()
from datetime import datetime

DB_NAME = 'Logger'

TABLES = {}
TABLES['mensajes'] = (
    "CREATE TABLE `mensajesmqtt` ("
    "  `idMsj` int(11) NOT NULL AUTO_INCREMENT,"
    "  `tiempo` datetime NOT NULL,"
    "  `mensaje` varchar(600) NOT NULL,"
    "  `topic` varchar(100) NOT NULL,"    
    "  PRIMARY KEY (`idMsj`)"
    ") ENGINE=InnoDB")

"""fecha = str(datetime.now().date())
TABLES['mensajes'] = (
    "CREATE TABLE `"+fecha+"` ("
    "  `idMsj` int(11) NOT NULL AUTO_INCREMENT,"
    "  `tiempo` datetime NOT NULL,"
    "  `mensaje` varchar(600) NOT NULL,"
    "  `topic` varchar(100) NOT NULL,"    
    "  PRIMARY KEY (`idMsj`)"
    ") ENGINE=InnoDB")
"""

add_msj = ("INSERT INTO mensajesmqtt "
            "(tiempo, mensaje, topic) "
            "VALUES (%(tiempo)s, %(mensaje)s, %(topic)s)")
def databaseStart(q):
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    try:
        cnx = mysql.connector.connect(user="python",passwd="123456",host="localhost",port="5000")
    except:
        estado = q.put( "No hay base de datos")
        print(estado)
        return
    cursor = cnx.cursor()
    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
        print("Usando la base de datos->",DB_NAME)
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()
    estado = q.put( "Configurado")
    print(estado)
    return

def databasePUT(q):
    try:
        cnx = mysql.connector.connect(user="python",passwd="123456",host="localhost",port="5000",database = "Logger")
    except:
        estado = q.put( "No hay base de datos")
        print(estado)
        return
    cursor = cnx.cursor()
    print('parent process:', os.getppid())
    print('I AM process id:', os.getpid())
    estadisticas = '{"estadisticas":true}'
    topic = "prod/test"
    data_salary = {
                'tiempo': datetime.now(),
                'mensaje': estadisticas,
                'topic': topic,        
            }
    #cursor.execute(add_msj, data_salary)
    print("Hoy es",datetime.now().date())
    # Make sure data is committed to the database    
    print("COMENZANDO LOGUEO")
    while True:
        lectura = q.get()
        if(lectura != None):
            #print("Hay algo: ",lectura)
            mqttCompleto = lectura.split("DELIMITA",1)
            #print(len(mqttCompleto))
            if(len(mqttCompleto) == 2 and len(mqttCompleto[1]) < 600 and len(mqttCompleto[0]) < 200):                
                data_salary = {
                    'tiempo': datetime.now(),
                    'mensaje': mqttCompleto[1],
                    'topic': mqttCompleto[0],        
                }                
                cursor.execute(add_msj, data_salary)
                cnx.commit()
    cnx.close()
    cursor.close()