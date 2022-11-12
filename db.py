#!/usr/bin/python3
from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
from concurrent import futures

hilos = futures.ThreadPoolExecutor()

DB_NAME = 'Logger'

TABLES = {}
TABLES['mensajes'] = (
    "CREATE TABLE `mensajesmqtt` ("
    "  `idMsj` int(11) NOT NULL AUTO_INCREMENT,"
    "  `tiempo` datetime NOT NULL,"
    "  `mensaje` varchar(200) NOT NULL,"
    "  `topic` varchar(100) NOT NULL,"    
    "  PRIMARY KEY (`idMsj`)"
    ") ENGINE=InnoDB")
def databaseStart():
    try:
        cnx = mysql.connector.connect(user="python",passwd="123456",host="localhost",port="5000")
    except:
        return "No hay base de datos"
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
    return "Configurado"

if __name__ == '__main__':
    hilo = hilos.submit(databaseStart) #hilo de monitor mqtt
    resultHilo = hilo.result()
    if(resultHilo == "No hay base de datos"):
        print("No hay DB, verificar")
    elif(resultHilo == "Configurado"):
        print("Base de datos lista")

    