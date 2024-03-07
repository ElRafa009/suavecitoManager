from tkinter import Button, Frame, Scrollbar, StringVar, Tk, Text, Label
from menu import create_menu
from buttons import create_buttons

def create_editor():

    # Configuracion de la raiz
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    # root.attributes('-fullscreen',True) -- Esta funcion sirve para poner la pantalla en modo pantalla completa
    root.title("Suavecito Compiler")

    button_frame = Frame(root)
    button_frame.pack(side='top', fill='x', padx=20, pady=10)

    # Caja de texto central
    texto = Text(root)
    # texto.pack(fill="both", expand=1) -- Con esto la caja de texto adopta el tamaño de la pantalla
    texto.pack()
    texto.config(bd=0, padx=6, font=("Consolas", 12))
    margen_x = 20
    margen_y = 50
    texto.place(x=margen_x, y=margen_y, width=(width-(2*margen_x)), height=300)
    # texto.grid(row=0, column=0, padx=10, pady=10) -- Uso de Grid

    # Monitor inferior
    mensaje = StringVar()
    mensaje.set("Bienvenido a Suavecito Compiler")
    monitor = Label(root, textvar=mensaje, justify='left')
    monitor.pack(side='bottom', anchor='se', padx=20)

    # Pantalla de salida
    pantalla_salida = Text(root, height=300, state='disabled', wrap='word')
    pantalla_salida.pack()
    pantalla_salida.config(bd=0, padx=6, font=("Consolas", 12))
    pantalla_salida.place(x=margen_x, y=2*margen_y+300, width=(width-(2*margen_x)), height=300)
    scrollbar = Scrollbar(pantalla_salida, command=pantalla_salida.yview)
    scrollbar.pack(side='right', fill='y')
    pantalla_salida['yscrollcommand'] = scrollbar.set

    # Menu superior
    create_menu(root, mensaje, texto)

    # Menu botones
    create_buttons(button_frame, root, mensaje, texto, pantalla_salida)

    # Finalmente bucle de la aplicacion
    root.mainloop()

if __name__ == "__main__":
    create_editor()