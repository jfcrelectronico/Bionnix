###################################################################################################
# Step 1 : Setup initial basic graphics
# Step 2: Update available COMs & Baude rate
# Step 3: Serial connection setup
# Step 4: Dynamic GUI update
# Step 5: Testing & Debugging


##NOTAS
#PARA GENERAR EL EJECUTABLE
# INSTALE SERIAL Y PYSERIAL
# pip install serial
# pip install pyserial
# ACTUALIZAR LA VERSION DE PYSERIAL
## pip install pyserial==2.7
# EN EL CMD UBIQUESE EN LA CARPETA QUE CONTIENE EL ARCHIVO .PY A VOLVER EJECUTABLE
# si desea un icono personalizado para su aplicacion cree la imagen con extension .ico y guardela en la carpeta del proyecto
# instale pyinstaller
# pip install pyinstaller
# para crear el ejecutable use la siguiente linea de comandos
# pyinstaller --windowed --onefile --icon=./nombre_imagen.ico nombre_archivo_a_volver_ejecutable.py

# Nota si ya genero el .exe debe eliminar las carpetas, dist,build: _pycache_ antes de generar un nuevo .exe
###################################################################################################
'''

from tkinter import *
import serial.tools.list_ports
import threading
from tkinter import messagebox

def Programa():
    #variables globales para permitir captura de datos en las diferentes funciones
    global root, BtnConectar, BtnBuscar,DatoRecibido,frameBotones,BtnLeerArchivo,DatoRecibido
    # instanciar el objeto Tk para creacion de GUI
    root = Tk()
    root.title("IOTHIX")
    root.geometry("920x450")
    root.config(bg="#f0f0f0",bd=5,relief="groove")
    root.resizable(0, 0)
    root.iconbitmap('icono.ico')

    frameImagen = Frame(root, bd=3, relief="sunken",bg="#ffffff")
    frameImagen.grid(column=0, row=0, pady=10, padx=10)

    image = PhotoImage(file="icono2.png")

    LbImagen = Label(frameImagen,image=image)
    LbImagen.pack()

    Lblinea = Label(frameImagen,bg="orange")
    #Lblinea.grid(column=0, row=1)
    Lblinea.pack()

    frameBotones=Frame(frameImagen,bd=5,relief="groove",bg="#ffffff")
    frameBotones.grid(column=1, row=0)

    root.protocol("WM_DELETE_WINDOW", close_window)
    root.mainloop()

def close_window():
    global root, serialData
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        serialData = False
        root.destroy()

Programa()
#root.protocol("WM_DELETE_WINDOW", close_window)
#root.mainloop()
'''


from tkinter import *

win= Tk()

for i in range (1):
    for j in range(1):
        frameImagen = Frame(win, bd=3, relief="sunken", bg="#ffffff")
        frameImagen.grid(column=0, row=0, pady=10, padx=10)

        image = PhotoImage(file="icono2.png")

        LbImagen = Label(frameImagen,image=image)
        LbImagen.grid(column=0, row=0)

        image2 = PhotoImage(file="barraN.png")

        Lblinea = Label(frameImagen, image=image2)
        # Lblinea.grid(column=0, row=1)
        Lblinea.grid(column=0, row=1,columnspan=2)

        #frame=Frame(win,relief=RAISED,borderwidth=1)
        #frame.grid(row=i,column=j, padx=5, pady=5)
        #label=Label(frame,text=f'Row {i}\nColumn{j}')
        #label.pack()

win.mainloop()
