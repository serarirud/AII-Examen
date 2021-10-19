#encoding: utf-8
from bs4 import BeautifulSoup
import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
import urllib
from urllib import request
import re
from datetime import datetime
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


DATABASE="libros.db"


def abrirUrl(url):
    try:
        f = urllib.request.urlopen(url)
        return f
    except:
        print("Error al conectarse a la página")
        return None

def soup(url):
    f = abrirUrl(url)
    return BeautifulSoup(f, "html.parser")


URL_BASE = "https://www.uniliber.com"
URL_1="https://www.uniliber.com/buscar/libros_pagina_1?descripcion%5B0%5D=CL%C3%81SICOS"
URL_2="https://www.uniliber.com/buscar/libros_pagina_2?descripcion%5B0%5D=CL%C3%81SICOS"
urls=[URL_1, URL_2]


def cargar():
    connection = sqlite3.connect(DATABASE) #crea la base de datos
    connection.text_factory = str 
    cursor = connection.cursor()    
    cursor.execute('DROP TABLE IF EXISTS Libros')
    cursor.execute('CREATE TABLE IF NOT EXISTS Libros (ID INTEGER PRIMARY KEY AUTOINCREMENT, titulo varchar(256), autor varchar(256), editorial varchar(256), estado varchar(256), precio float, libreria varchar(256), telefono varchar(256))')

    for url in urls:
        s = soup(url)
        libros = s.find("div", class_="listado_detallado").find_all("div", class_="description")
        for libro in libros:

            titulo, autor, editorial, estado, libreria, telefono = "Desconocido","Desconocido","Desconocido","Desconocido","Desconocido","Desconocido"
            precio = -1.0


            if (libro.find("a", class_="title")):
                titulo = libro.find("a", class_="title").string.strip()

            if (libro.find("div", class_="subtitle").string):
                autor = libro.find("div", class_="subtitle").string.strip()

            if (libro.find("strong", string="Editorial:")):
                editorial = libro.find("strong", string="Editorial:").parent.contents[2].string.strip()

            if (libro.find("strong", string="Estado de conservación:")):
                estado = libro.find("strong", string="Estado de conservación:").parent.contents[2].string.strip()

            if (libro.find("span", class_="precio")):
                precio = float(libro.find("span", class_="precio").string.strip().replace("€", ""))


            if (libro.find("a", class_="libreria")):
                libreria = libro.find("a", class_="libreria").string.strip()

                link = libro.find("a", class_="libreria")["href"]

                pagLibreria = soup(URL_BASE + link)

                if (pagLibreria.find("div", class_="border-orange info-libreria").find("th", string="Teléfono:")):
                    telefono = pagLibreria.find("div", class_="border-orange info-libreria").find("th", string="Teléfono:").find_next_sibling().string.strip()

            cursor.execute('INSERT INTO Libros (titulo, autor, editorial, estado, precio, libreria, telefono) VALUES (?,?,?,?,?,?,?)', (titulo, autor, editorial, estado, precio, libreria, telefono))

    
    num = cursor.execute('SELECT COUNT(*) FROM Libros')

    connection.commit()
    connection.close()




if __name__ == "__main__":
    cargar()





