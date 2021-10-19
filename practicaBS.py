import tkinter as tk
from tkinter import END
from tkinter import messagebox
import sqlite3
from bs4 import BeautifulSoup
import urllib
from urllib import request
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

DATABASE = 'libros.db'
URL_BASE = "https://www.uniliber.com"
URL_1="https://www.uniliber.com/buscar/libros_pagina_1?descripcion%5B0%5D=CL%C3%81SICOS"
URL_2="https://www.uniliber.com/buscar/libros_pagina_2?descripcion%5B0%5D=CL%C3%81SICOS"
urls=[URL_1, URL_2]

# Ejercicio 1

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
                    telefono = pagLibreria.find("div", class_="border-orange info-libreria").find("th", string="Teléfono:").find_next_sibling().string.strip().replace(' ', '')

            cursor.execute('INSERT INTO Libros (titulo, autor, editorial, estado, precio, libreria, telefono) VALUES (?,?,?,?,?,?,?)', (titulo, autor, editorial, estado, precio, libreria, telefono))

    
    num = cursor.execute('SELECT COUNT(*) FROM Libros').fetchone()[0]

    connection.commit()
    connection.close()
    messagebox.showinfo('Guardado correctamente.', 'Se han guardado correctamente {} libros'.format(num))

# Ejercicio 2 y 3

def find_books():
    '''Muestra una lista de tuplas cuyos datos son
    el título, el autor, la editorial y el precio'''
    con = sqlite3.connect(DATABASE)
    data = [(titulo, autor, editorial, '{}€'.format(precio)) for titulo, autor, editorial, precio in con.execute('SELECT titulo, autor, editorial, precio FROM Libros').fetchall()]
    con.close()
    crear_listbox_con_scrollbar(data)

def find_distinct_library():
    '''Muestra todas las librerias y números en la base de datos'''
    con = sqlite3.connect(DATABASE)
    data = con.execute('SELECT DISTINCT libreria, telefono FROM Libros').fetchall()
    con.close()
    crear_listbox_con_scrollbar(data)    

def find_books_by_editorial(editorial: str) -> list[tuple[str, str, str, str, float]]:
    '''Devuelve una lisat de tuplas con el título, el autor, estado de conservación
    librería y precio filtrados por editorial'''
    con = sqlite3.connect(DATABASE)
    res = [(titulo, autor, estado, libreria, '{}€'.format(precio)) for titulo, autor, estado, libreria, precio in 
                        con.execute('SELECT titulo, autor, estado, libreria, precio FROM Libros WHERE editorial LIKE ?'
                        , ('%{}%'.format(editorial),)).fetchall()]
    con.close()
    return res

def find_books_by_titulo_or_autor(titulo_autor: str) -> list[tuple[str, str, str, str, float]]:
    '''Devuelve una lisat de tuplas con el título, el autor, estado de conservación
        librería y precio filtrados por título o autor'''
    
    if ' ' in titulo_autor.strip():
        raise ValueError('Solo se permite introducir una palabra')

    con = sqlite3.connect(DATABASE)
    res = [(titulo, autor, estado, libreria, '{}€'.format(precio)) for titulo, autor, estado, libreria, precio in 
                        con.execute('SELECT titulo, autor, estado, libreria, precio FROM Libros WHERE titulo LIKE ? OR autor LIKE ?'
                        , ('%{}%'.format(titulo_autor),'%{}%'.format(titulo_autor))).fetchall()]
    con.close()
    return res

def find_by_editorial_aux():
    con = sqlite3.connect(DATABASE)
    options = [option[0] for option in con.execute('SELECT DISTINCT editorial FROM Libros').fetchall()]
    con.close()
    create_spinbox('Escoge una editorial', options, find_books_by_editorial)

# Tkinter functions

def start():
    main_window = tk.Tk()
    
    menu = tk.Menu(main_window, tearoff=0)

    datos = tk.Menu(menu, tearoff=0)
    datos.add_command(label='Cargar', command=cargar)
    datos.add_command(label='Salir', command=main_window.destroy)

    menu.add_cascade(label='Datos', menu=datos)

    listar = tk.Menu(menu, tearoff=0)
    listar.add_command(label='Libros', command=find_books)
    listar.add_command(label='Librerías', command=find_distinct_library)

    menu.add_cascade(label='Listar', menu=listar)

    buscar = tk.Menu(menu, tearoff=0)
    buscar.add_command(label='Libros por editorial'
                        , command=find_by_editorial_aux)
    buscar.add_command(label='Libros por título o autor'
                        , command=lambda: create_search_window_one_entry('Título o autor (Sólo una palabra): ', find_books_by_titulo_or_autor))

    menu.add_cascade(label='Buscar', menu=buscar)
    
    main_window.config(menu=menu)
    main_window.mainloop()

def crear_listbox_con_scrollbar(data: list[tuple]) -> None:
    main_window = tk.Tk()
    scrollbar = tk.Scrollbar(main_window)
    scrollbar.pack(side='right', fill='both')
    listbox = tk.Listbox(main_window, yscrollcommand=scrollbar.set, width=200)
    for d in data:
        listbox.insert(END, str(d))
    
    listbox.pack(side='left', fill='both')
    scrollbar.config(command=listbox.yview)
    main_window.mainloop()

def create_search_window_one_entry(label, command) -> None:
    def listar(event):
        try:
            data = command(entry.get())
            window.destroy()
            crear_listbox_con_scrollbar(data)
        except ValueError as e:
            window.destroy()
            messagebox.showwarning('Warning', str(e))
            create_search_window_one_entry(label, command)
    window = tk.Tk()

    entry = create_entry(window, label, listar)
    window.mainloop()

def create_entry(window: tk.Tk, label: str, command) -> None:
    label_widget = tk.Label(window)
    label_widget['text'] = label
    label_widget.pack(side='left')
    entry = tk.Entry(window)
    entry.bind("<Return>", command)
    entry.pack(side='left')
    return entry

def create_label(window: tk.Tk, text: str, side='left') -> None:
    label = tk.Label(window)
    label['text'] = text
    label.pack(side=side)

def create_spinbox(label, options: list[str], command):
    def listar(event):
        data = command(spinbox.get())
        window.destroy()
        crear_listbox_con_scrollbar(data)
            
    window = tk.Tk()
    create_label(window, label, side='top')
    spinbox = tk.Spinbox(window, width=200, values=options)
    spinbox.pack(side='top')
    spinbox.bind('<Return>', listar)

start()