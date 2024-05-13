from tkinter import Frame, Scrollbar, StringVar, Tk, Text, Label, ttk
from menu import create_menu
from buttons import create_buttons

def highlight_syntax(texto):
    
    keywords = ['int', 'float', 'if', 'else', 'for', 'while', 'do']

    # Borrar estilos anteriores
    texto.tag_remove('keyword', '1.0', 'end')
    texto.tag_remove('string', '1.0', 'end')
    texto.tag_remove('comment_line', '1.0', 'end')
    texto.tag_remove('comment_block', '1.0', 'end')

    # Resaltado de palabras clave
    for kw in keywords:
        start = '1.0'
        while True:
            start = texto.search(kw, start, stopindex='end', regexp=True, count='1')
            if not start:
                break
            end = f"{start}+{len(kw)}c"
            texto.tag_add('keyword', start, end)
            start = end

    # Resaltado de texto entre comillas
    start = '1.0'
    while True:
        start = texto.search('"', start, stopindex='end', count='1')
        if not start:
            break
        end = texto.search('"', f"{start}+1c", stopindex='end', count='1')
        if not end:
            break
        texto.tag_add('string', start, f"{end}+1c")
        start = f"{end}+1c"

    # Resaltado de comentarios de línea (//)
    start = '1.0'
    while True:
        start = texto.search('//', start, stopindex='end', count='1')
        if not start:
            break
        end = texto.search('\n', f"{start} lineend", stopindex='end', count='1')
        if not end:
            end = 'end'
        texto.tag_add('comment_line', start, end)
        start = end

    # Resaltado de comentarios de bloque (/* ... */)
    start = '1.0'
    while True:
        start = texto.search('/*', start, stopindex='end', count='1')
        if not start:
            break
        end = texto.search('*/', f"{start}+2c", stopindex='end', count='1')
        if not end:
            end = 'end'
        texto.tag_add('comment_block', start, end+'+2c')
        start = end+'+2c'

    # Estilos para tags
    texto.tag_configure('keyword', foreground='blue')
    texto.tag_configure('string', foreground='#ba6b2b')
    texto.tag_configure('comment_line', foreground='green')
    texto.tag_configure('comment_block', foreground='green')

def create_editor():
    root = Tk()
    root.title("Suavecito Compiler")

    # Configuracion de la ventana
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    ventana_ancho = int(width * 0.9)
    ventana_alto = int(height * 0.9)
    pos_x = int((width - ventana_ancho) / 2)
    pos_y = int((height - ventana_alto) / 2)
    root.geometry(f"{int(ventana_ancho)}x{int(ventana_alto)}+{int(pos_x)}+{int(pos_y)}")

    # Frame para los botones
    button_frame = Frame(root)
    button_frame.pack(side='top', fill='x', padx=20, pady=(10, 0))

    # Frame principal el cual sera dividido
    frame_principal = Frame(root)
    frame_principal.pack(fill='both', expand=True)

    margen_x = 20
    margen_y = 20

    # Parte izquierda: editor de texto
    frame_izquierda = Frame(frame_principal)
    frame_izquierda.pack(side='left', fill='both', expand=True)
    texto = Text(frame_izquierda, wrap='word', bd=0, padx=6, font=("Consolas", 12))
    texto.pack(fill="both", expand=True, padx=margen_x, pady=margen_y)
    
    # Vincular evento de cambio de texto a la función de resaltado de sintaxis
    texto.bind('<KeyRelease>', lambda event: highlight_syntax(texto))
    
    # Parte derecha: Analisis lexico y sintactico
    frame_derecha = Frame(frame_principal)
    frame_derecha.pack(side='right', fill='both', expand=True)
    tab_control_analisis = ttk.Notebook(frame_derecha)
    # Pestaña para Análisis Léxico
    frame_lexico = ttk.Frame(tab_control_analisis)
    tab_control_analisis.add(frame_lexico, text='Análisis Léxico')
    # Aquí se debe agregar el análisis léxico

    # Pestaña para Análisis Sintáctico
    frame_sintactico = ttk.Frame(tab_control_analisis)
    tab_control_analisis.add(frame_sintactico, text='Análisis Sintáctico')
    # Aquí se debe agregar el análisis sintáctico
    
    tab_control_analisis.pack(fill='both', expand=True, padx=margen_x, pady=margen_y)

    # Monitor inferior
    mensaje = StringVar()
    mensaje.set("Bienvenido a Suavecito Compiler")
    monitor = Label(root, textvar=mensaje, justify='left')
    monitor.pack(side='bottom', anchor='se', padx=20)

    # Crear Notebook para errores y resultados
    tab_control = ttk.Notebook(root)
    frame_errors = ttk.Frame(tab_control)
    tab_control.add(frame_errors, text='Errores')
    frame_results = ttk.Frame(tab_control)
    tab_control.add(frame_results, text='Resultados')
    tab_control.pack(side='right', fill='both', expand=True, padx=margen_x, pady=margen_y)

    # Pantalla de salida para errores
    pantalla_errores = Text(frame_errors, height=10, state='disabled', wrap='word')
    pantalla_errores.pack(fill='both', expand=True, padx=6, pady=6)
    scrollbar_errores = Scrollbar(frame_errors, command=pantalla_errores.yview)
    scrollbar_errores.pack(side='right', fill='y')
    pantalla_errores['yscrollcommand'] = scrollbar_errores.set

    # Pantalla de salida para resultados
    pantalla_resultados = Text(frame_results, height=10, state='disabled', wrap='word')
    pantalla_resultados.pack(fill='both', expand=True, padx=6, pady=6)
    scrollbar_resultados = Scrollbar(frame_results, command=pantalla_resultados.yview)
    scrollbar_resultados.pack(side='right', fill='y')
    pantalla_resultados['yscrollcommand'] = scrollbar_resultados.set

    # Menu superior y botones
    create_menu(root, mensaje, texto)
    create_buttons(button_frame, root, mensaje, texto, pantalla_resultados)

    # Bucle de la aplicacion
    root.mainloop()

if __name__ == "__main__":
    create_editor()