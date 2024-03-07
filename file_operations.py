from tkinter import END, filedialog as FileDialog
from io import open

ruta = "" # La utilizaremos para almacenar la ruta del archivo

# Crear un archivo nuevo
def nuevo(root, mensaje, texto):
    global ruta
    mensaje.set("Nuevo Archivo")
    ruta = ""
    texto.delete(1.0, END)
    root.title("Suavecito Compiler")

# Abrir un archivo
def abrir(root, mensaje, texto):
    global ruta
    mensaje.set("Abrir Archivo")
    ruta = FileDialog.askopenfilename(
        initialdir=".",
        filetype=(("Archivos de texto", "*.txt"),),
        title="Abrir un archivo de texto")
    
    if ruta != "":
        archivo = open(ruta, 'r')
        contenido = archivo.read()
        texto.delete(1.0, END)
        texto.insert('insert', contenido)
        archivo.close()
        root.title(ruta + "- Suavecito Compiler")

# Guardar archivo
def guardar(root, mensaje, texto):
    mensaje.set("Guardar Archivo")
    if ruta != "":
        contenido = texto.get(1.0, 'end-1c')
        archivo = open(ruta, 'w+')
        archivo.write(contenido)
        archivo.close()
        mensaje.set("Archivo guardado correctamente")
    else:
        guardar_como(root, mensaje, texto)

# Guardar como
def guardar_como(root, mensaje, texto):
    global ruta
    mensaje.set("Guardar Archivo como")
    archivo = FileDialog.asksaveasfile(title="Guardar archivo", mode="w", defaultextension=".txt")
    if archivo is not None:
        ruta = archivo.name
        root.title(ruta + "- Suavecito Compiler")
        contenido = texto.get(1.0, 'end-1c')
        archivo = open(ruta, 'w+')
        archivo.write(contenido)
        archivo.close()
        mensaje.set("Archivo guardado correctamente")
    else:
        mensaje.set("Guardado cancelado")
        ruta = ""