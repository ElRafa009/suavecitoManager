    
import os
from tkinter import Button
import tkinter
from file_operations import nuevo, abrir, guardar, guardar_como

# Lista para mantener referencias globales a las imágenes
images = []

def resize_image(image_path, width, height):
    original_image = tkinter.PhotoImage(file=image_path)
    resized_image = original_image.subsample(width, height)
    images.append(resized_image)  # Mantener referencia global
    return resized_image

def create_buttons(button_frame, root, mensaje, texto, pantalla_salida):

    # Rutas de las imagenes
    img_new_path = os.path.abspath("img/new.png")
    img_open_path = os.path.abspath("img/open.png")
    img_save_path = os.path.abspath("img/save.png")
    img_save_as_path = os.path.abspath("img/save_as.png")
    img_run_path = os.path.abspath("img/run.png")
    
    img_new = resize_image(img_new_path, 2, 2)
    img_open = resize_image(img_open_path, 2, 2)
    img_save = resize_image(img_save_path, 2, 2)
    img_save_as = resize_image(img_save_as_path, 2, 2)
    img_run = resize_image(img_run_path, 2, 2)

    button_new = Button(button_frame, image=img_new, command=lambda: nuevo(root, mensaje, texto))
    button_new.pack(side='left', padx=5)
    button_open = Button(button_frame, image=img_open, command=lambda: abrir(root, mensaje, texto))
    button_open.pack(side='left', padx=5)
    button_save = Button(button_frame, image=img_save, command=lambda: guardar(root, mensaje, texto))
    button_save.pack(side='left', padx=5)
    button_save_as = Button(button_frame, image=img_save_as, command=lambda: guardar_como(root, mensaje, texto))
    button_save_as.pack(side='left', padx=5)

    def mostrar_mensaje_en_rojo(mensaje):
        pantalla_salida.config(state='normal', fg='red')  # Habilitar la edición para agregar texto en rojo
        pantalla_salida.insert('end', mensaje + '\n')  # Insertar el mensaje y un salto de línea
        pantalla_salida.config(state='disabled')  # Deshabilitar la edición para que sea solo de lectura
        pantalla_salida.see('end')  # Desplazar la pantalla hacia abajo para mostrar el mensaje más reciente

    def run_command():
        guardar(root, mensaje, texto)
        mensaje.set("Corriendo")
        mostrar_mensaje_en_rojo("¡Corriendo el programa!")

    button_run = Button(button_frame, image=img_run, command= run_command)
    button_run.pack(side='left', padx=5)

    
 