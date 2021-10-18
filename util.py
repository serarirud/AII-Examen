import tkinter as tk
from tkinter import END

def menu_example(*example):
    main_window = tk.Tk()
    
    menu = tk.Menu(main_window, tearoff=0)

    datos = tk.Menu(menu, tearoff=0)
    datos.add_command(label='Cargar', command=menu_example)
    datos.add_command(label='Listar', command=menu_example)
    datos.add_command(label='Salir', command=lambda: menu_example(main_window))

    menu.add_cascade(label='Datos', menu=datos)

    busc = tk.Menu(menu, tearoff=0)
    busc.add_command(label='Titulo', command=lambda: menu_example('Título: ', menu_example.search_by_title))
    busc.add_command(label='Fecha', command=lambda: menu_example('Fecha: ', menu_example.search_by_date))
    busc.add_command(label='Genero', command=menu_example)

    menu.add_cascade(label='Buscar', menu=busc)
    
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
            create_search_window(label, command)
    window = tk.Tk()

    entry = create_entry(window, label, listar)
    window.mainloop()

def create_search_window(labels, command) -> None:
    def listar(event):
        kwargs = {'entry{}'.format(i+1): entry.get() for i, entry in enumerate(entries)}
        try:
            window.destroy()
            data = command(**kwargs)
            crear_listbox_con_scrollbar(data)
        except:
            create_search_window(labels, command)
    window = tk.Tk()
    if not isinstance(labels, list):
        labels = [labels]

    entries = []
    for label in labels:
        entries.append(create_entry(window, label, listar))
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