import tkinter as tk
from tkinter import END
from tkinter import messagebox
import sqlite3

DATABASE = 'libros.db'

def find_books():
    '''Muestra una lista de tuplas cuyos datos son
    el título, el autor, la editorial y el precio'''
    con = sqlite3.connect(DATABASE)
    data = con.execute('SELECT titulo, autor, editorial, precio FROM Libros').fetchall()
    con.close()
    crear_listbox_con_scrollbar(data)
    

def find_distinct_library():
    '''Muestra todas las librerias y números en la base de datos'''
    con = sqlite3.connect(DATABASE)
    data = con.execute('SELECT DISTINCT libreria, numero FROM Libros').fetchall()
    con.close()
    crear_listbox_con_scrollbar(data)    

def find_books_by_editorial(editorial: str) -> list[tuple[str, str, str, str, float]]:
    '''Devuelve una lisat de tuplas con el título, el autor, estado de conservación
    librería y precio filtrados por editorial'''
    con = sqlite3.connect(DATABASE)
    res = con.execute('SELECT titulo, autor, estado, librería, precio FROM Libros WHERE editorial LIKE ?'
                        , ('%{}%'.format(editorial),)).fetchall()
    con.close()
    return res

def find_books_by_titulo_or_autor(titulo_autor: str) -> list[tuple[str, str, str, str, float]]:
    '''Devuelve una lisat de tuplas con el título, el autor, estado de conservación
        librería y precio filtrados por título o autor'''
    con = sqlite3.connect(DATABASE)
    res = con.execute('SELECT titulo, autor, estado, librería, precio FROM Libros WHERE titulo LIKE ? OR autor LIKE ?'
                        , ('%{}%'.format(titulo_autor),'%{}%'.format(titulo_autor))).fetchall()

def cargar():
    pass

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
                        , command=lambda: create_search_window_one_entry('Editorial: ', find_books_by_editorial))
    buscar.add_command(label='Libros por título o autor'
                        , command=lambda: create_search_window_one_entry('Título o autor: ', find_books_by_titulo_or_autor))

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
        except:
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

def create_option_button(window: tk.Tk, text: str, command, side='left') -> None:
    option = tk.Button(window)
    option['text'] = text
    option['command'] = command
    option.pack(side=side)

def create_radiobutton(window: tk.Tk, option_name: str, command) -> None:
    radiobutton = tk.Radiobutton(window)
    radiobutton['text'] = option_name
    radiobutton['command'] = command
    radiobutton.pack(side='top')

def create_label(window: tk.Tk, text: str, side='left') -> None:
    label = tk.Label(window)
    label['text'] = text
    label.pack(side=side)

def create_spinbox(options: list[str], command):
    def listar(event):
        window.destroy()
        data = command(spinbox.get())
        crear_listbox_con_scrollbar(data)
            
    window = tk.Tk()
    create_label(window, 'Escoge una uva', side='top')
    spinbox = tk.Spinbox(window, width=200, values=options)
    spinbox.pack(side='top')
    spinbox.bind('<Return>', listar)

start()