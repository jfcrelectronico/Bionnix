###################################################################################################
# Step 1 : Setup initial basic graphics
# Step 2: Update available COMs & Baude rate
# Step 3: Serial connection setup
# Step 4: Dynamic GUI update
# Step 5: Testing & Debugging


##NOTAS
# PARA GENERAR EL EJECUTABLE
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


from tkinter.ttk import *
from tkinter import *

import serial.tools.list_ports
import threading
from tkinter import messagebox

import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def inicio():
    global inicio,root, Master, BrodSla, Slave, Broadcast
    Master = False
    BrodSla = False
    Slave = False
    Broadcast = False
    root = False

    inicio = Tk()
    inicio.title("IOTHIX")
    inicio.geometry("300x400")
    inicio.config(bg="#f0f0f0", bd=5, relief="groove")
    inicio.resizable(0, 0)
    inicio.iconbitmap('icono.ico')

    #frameLogo = Frame(inicio, bd=3, relief="sunken", bg="#ff6b0f")
    #frameLogo.grid(column=0, row=0, pady=150, padx=40)

    #image = PhotoImage(file="icono2.png")

    frameBtnDirecciones = Frame(inicio, bd=3, relief="sunken", bg="#ff6b0f")
    frameBtnDirecciones.grid(column=0, row=0, pady=150, padx=40)

    BtnDirecciones = Button(frameBtnDirecciones, text="Configurar\ndispositivos de\nred", height=3, width=30, command=Programa, fg="#ffffff",
                       bg="#ff6b0f", state="active")
    BtnDirecciones.grid(column=0, row=0)

    #frameBtnFirmware = Frame(inicio, bd=3, relief="sunken", bg="#ff6b0f")
    #frameBtnFirmware.grid(column=2, row=0, pady=150, padx=40)

    BtnProgramar = Button(frameBtnDirecciones, text="Conf_Firmware", height=3, width=30, command=ventanaConfFirmware,
                          fg="#ffffff", bg="#ff6b0f", state="active")
    BtnProgramar.grid(column=0, row=1)

    BtnAmpy = Button(frameBtnDirecciones, text="InstalarAmpy", height=3, width=30, command=instalarampy,
                          fg="#ffffff", bg="#ff6b0f", state="active")
    BtnAmpy.grid(column=0, row=2)

    inicio.protocol("WM_DELETE_WINDOW", close_window)
    inicio.mainloop()



def Programa():
    global root, Master, BrodSla, Slave, Broadcast, BtnvolverM, frameLogo, BtnConectar, BtnMaster, BtnBroSla, BtnBuscar, BtnBorrarConf,BtnProgramar,BtnVolverI
    Master = False
    BrodSla = False
    Slave = False
    Broadcast = False
    #inicio= False
    root = Toplevel()
    #root = Tk()
    root.title("IOTHIX")
    root.geometry("860x480")
    root.config(bg="#f0f0f0", bd=5, relief="groove")
    root.resizable(0, 0)
    root.iconbitmap('icono.ico')

    frameBtnMaster = Frame(root, bd=3, relief="sunken", bg="#ff6b0f")
    frameBtnMaster.grid(column=0, row=0, pady=150, padx=40)

    BtnMaster = Button(frameBtnMaster, text="Maestro", height=3, width=30, command=ventanaMaster, fg="#ffffff",
                       bg="#ff6b0f", state="disable")
    BtnMaster.grid(column=0, row=0)

    frameBtnBroSla = Frame(root, bd=3, relief="sunken", bg="#ff6b0f")
    frameBtnBroSla.grid(column=2, row=0, pady=150, padx=40)

    #BtnProgramar = Button(frameBtnBroSla, text="Conf_Firmware", height=3, width=30, command=ventanaConfFirmware,fg="#ffffff", bg="#ff6b0f", state="disable")
    #BtnProgramar.grid(column=0, row=0)

    BtnBroSla = Button(frameBtnBroSla, text="Repetidor-Esclavo", height=3, width=30, command=ventanaBroSla,fg="#ffffff", bg="#ff6b0f", state="disable")
    BtnBroSla.grid(column=0, row=0)

    frameLogo = Frame(root, bd=3, relief="sunken", bg="#ff6b0f")
    frameLogo.grid(column=1, row=0, pady=150, padx=40)

    image = PhotoImage(file="icono2.png")

    LbImagen = Label(frameLogo, image=image)
    LbImagen.grid(column=0, row=0, pady=10, padx=10)

    BtnBuscar = Button(frameLogo, text="Buscar Puertos", height=1, width=10, command=actualizar_puertos,
                       fg="#ffffff", bg="#ff6b0f")
    BtnBuscar.grid(column=0, row=1)

    BtnConectar = Button(frameLogo, text="Conectar", height=1, width=10, state="disabled", command=Abrir_Puerto,
                         fg="#ffffff", bg="#ff6b0f")
    BtnConectar.grid(column=0, row=2)

    BtnBorrarConf = Button(frameLogo, text="Borrar_Conf", height=1, width=10, state="disabled", command=Borrar_Conf,
                           fg="#ffffff", bg="#ff6b0f")
    BtnBorrarConf.grid(column=0, row=4)

    BtnVolverI = Button(frameLogo, text='Volver', height=1, width=10, command=volverProgramaInicio, fg="#ffffff",
                        bg="#ff6b0f")
    BtnVolverI.grid(column=0, row=5)

    #root.protocol("WM_DELETE_WINDOW", close_window)
    #root.mainloop()

    if (root):  # si ventana abierta del master
        #os.system('cmd /k "pip3 install adafruit-ampy"')
        #print("ingreso a root")
        inicio.withdraw()  # oculta ventana principal
        root.deiconify()  # muestra ventana Master en primer plano

def volverProgramaInicio():
    global root
    try:

        root.destroy()
        inicio.deiconify()  # dar foco a una ventana
        root = False
    except Exception as e:
        print(e)


def ventanaConfFirmware():
    global ConfFirmware,port,frameLogo
    ConfFirmware = Toplevel()
    ConfFirmware.title("IOTHIX")
    ConfFirmware.geometry("370x400")
    ConfFirmware.config(bg="#f0f0f0", bd=5, relief="groove")
    ConfFirmware.resizable(0, 0)
    ConfFirmware.iconbitmap('icono.ico')
    ConfFirmware.overrideredirect(True)  # quitar la barra de nombre junto con los botones de minimizar, maximizar y cerrar

    frameImagen = Frame(ConfFirmware, bd=3, relief="sunken", bg="#ff6b0f")
    frameImagen.grid(column=0, row=0, pady=30, padx=30)
    image = PhotoImage(file="icono2.png")
    LbImagen = Label(frameImagen, image=image)
    LbImagen.grid(column=0, row=0, pady=10, padx=10)

    framefunciones = Frame(frameImagen, bd=5, relief="groove", bg="#ff6b0f")
    framefunciones.grid(column=0, row=1, pady=10, padx=10)

    BtnConfFirmendpoint = Button(framefunciones, text='UpdateFirmwareSlave', height=1, width=20, command=programarendpoint, fg="#ffffff",
                      bg="#ff6b0f")
    BtnConfFirmendpoint.grid(column=0, row=0, pady=10, padx=10)

    BtnConfFirmBroadcast = Button(framefunciones, text='UpdateFirmwareBroadcast', height=1, width=20,command=programarBroadcast, fg="#ffffff",
                                bg="#ff6b0f")
    BtnConfFirmBroadcast.grid(column=0, row=1 , pady=10, padx=10)

    BtnConfFirmMaster = Button(framefunciones, text='UpdateFirmwareMaster', height=1, width=20,command=programarMaster, fg="#ffffff",
                                  bg="#ff6b0f")
    BtnConfFirmMaster.grid(column=0, row=2 , pady=10, padx=10)

    frameLogo = Frame(frameImagen, bd=5, relief="groove", bg="#ff6b0f")
    frameLogo.grid(column=1, row=0, pady=10, padx=10)

    BtnBuscar = Button(frameLogo, text="Buscar Puertos", height=1, width=10, command=actualizar_puertos2,
                       fg="#ffffff", bg="#ff6b0f")
    BtnBuscar.grid(column=0, row=2)

    BtnVolverM = Button(frameLogo, text='Volver', height=1, width=10, command=volverConfFirmwareInicio, fg="#ffffff",
                        bg="#ff6b0f")
    BtnVolverM.grid(column=0, row=4, pady=10, padx=10)

    if (ConfFirmware):  # si ventana abierta del master
        #os.system('cmd /k "pip3 install adafruit-ampy"')
        inicio.withdraw()  # oculta ventana principal
        ConfFirmware.deiconify()  # muestra ventana Master en primer plano
def instalarampy():
    os.system('cmd /k "pip install adafruit-ampy"')
def programarendpoint():
    global port
    port = pulso_actualizar.get()
    os.system(f'cmd /k "cd C:\Program Files (x86)\SmartGrid\endpoint && ampy --port "{port}" put EndPoint.py "')
    os.system(f'cmd /k "cd C:\Program Files (x86)\SmartGrid\endpoint && ampy --port "{port}" put main.py"')

def programarBroadcast():
    global port
    port = pulso_actualizar.get()
    os.system(f'cmd /k "cd C:\Program Files (x86)\SmartGrid\\broadcast && ampy --port "{port}" put Broadcast.py "')
    os.system(f'cmd /k "cd C:\Program Files (x86)\SmartGrid\\broadcast && ampy --port "{port}" put main.py"')

def programarMaster():
    global port
    port = pulso_actualizar.get()
    os.system(f'cmd /k "cd C:\Program Files (x86)\SmartGrid\master && ampy --port "{port}" put Master.py "')
    os.system(f'cmd /k "cd C:\Program Files (x86)\SmartGrid\master && ampy --port "{port}" put main.py"')

def volverConfFirmwareInicio():
    global ConfFirmware
    try:
        ConfFirmware.destroy()
        inicio.deiconify()  # dar foco a una ventana
        ConfFirmware = False
        #callleerArc()
    except Exception as e:
        print(e)

def ventanaMaster():
    global Master, BtnConectarM, BtnBuscar, DatoRecibido, frameBotones, BtnLeerArchivo, DatoRecibido, BtnVolverM, BtnBrod, BtnSlave, Slave, Broadcast, BrodSla, NombreMaster, DatoMaster
    Slave = False
    Broadcast = False
    BrodSla = False
    Master = Toplevel()
    Master.title("IOTHIX")
    Master.geometry("370x400")
    Master.config(bg="#f0f0f0", bd=5, relief="groove")
    Master.resizable(0, 0)
    Master.iconbitmap('icono.ico')
    Master.overrideredirect(True)  # quitar la barra de nombre junto con los botones de minimizar, maximizar y cerrar
    # callleerArc()
    frameImagen = Frame(Master, bd=3, relief="sunken", bg="#ff6b0f")
    frameImagen.grid(column=0, row=0, pady=10, padx=10)
    image = PhotoImage(file="icono2.png")
    LbImagen = Label(frameImagen, image=image)
    LbImagen.grid(column=0, row=0, pady=10, padx=10)

    framefunciones = Frame(frameImagen, bd=5, relief="groove", bg="#ff6b0f")
    framefunciones.grid(column=0, row=1, pady=10, padx=10)

    BtnBrod = Button(framefunciones, text='Broadcast', height=1, width=10, command=ventanaAgregarBroadcast,
                     fg="#ffffff", bg="#ff6b0f")
    BtnBrod.grid(column=0, row=0, pady=10, padx=10)

    BtnSlave = Button(framefunciones, text='Slave', height=1, width=10, command=ventanaAgregarSlave, fg="#ffffff",
                      bg="#ff6b0f")
    BtnSlave.grid(column=0, row=1, pady=10, padx=10)

    BtnVolverM = Button(framefunciones, text='Volver', height=1, width=10, command=volverMasterRoot, fg="#ffffff",
                        bg="#ff6b0f")
    BtnVolverM.grid(column=0, row=2)

    frameconfiguracion = Frame(Master, bd=3, relief="sunken", bg="#ff6b0f")
    frameconfiguracion.grid(column=1, row=0, pady=10, padx=10)

    LbNomMaster = Label(frameconfiguracion, text="Direccion dispositivo", bg="#ff6b0f")
    LbNomMaster.grid(column=0, row=0, pady=10, padx=10)

    NombreMaster = StringVar()
    DatoMaster = Entry(frameconfiguracion, bg="#ffffff", borderwidth=4, width=5, textvariable=NombreMaster,
                       font=('Georgia 20'))
    DatoMaster.grid(column=0, row=1, pady=10, padx=10)

    LbNomMaster2 = Label(frameconfiguracion, text="Max 5 caracteres", bg="#ff6b0f")
    LbNomMaster2.grid(column=0, row=2, pady=10, padx=10)

    BtnEnvDatos = Button(frameconfiguracion, text='Configurar', height=1, width=10, command=callenviardatosMaster,
                         fg="#ffffff",
                         bg="#ff6b0f")
    BtnEnvDatos.grid(column=0, row=3)

    callleerArc()

    if conf_readymaster:

        DatoMaster.insert(END, direcciones[1])
        DatoMaster["state"] = "disabled"
        BtnEnvDatos["state"] = "disable"
        BtnBrod['state'] = 'active'
        BtnSlave['state'] = 'active'
    else:
        DatoMaster["state"] = "normal"
        BtnEnvDatos["state"] = "active"
        BtnBrod['state'] = 'disable'
        BtnSlave['state'] = 'disable'

    if (Master):  # si ventana abierta del master
        root.withdraw()  # oculta ventana principal
        Master.deiconify()  # muestra ventana Master en primer plano


def volverMasterRoot():
    global Master
    try:

        Master.destroy()
        root.deiconify()  # dar foco a una ventana
        Master = False
        callleerArc()
    except Exception as e:
        print(e)


def ventanaBroSla():
    global BrodSla, BtnConectarBS, BtnBuscar, DatoRecibido, frameBotones, BtnLeerArchivo, DatoRecibido, BtnVolverBS, Master, NombreEsclavoBroadcast,NombreMaestroescbroad
    # instanciar el objeto Tk para creacion de GUI

    BrodSla = Toplevel()
    BrodSla.title("IOTHIX")
    BrodSla.geometry("370x400")
    BrodSla.config(bg="#f0f0f0", bd=5, relief="groove")
    BrodSla.resizable(0, 0)
    BrodSla.iconbitmap('icono.ico')
    BrodSla.overrideredirect(True)  # quitar la barra de nombre junto con los botones de minimizar, maximizar y cerrar

    frameImagen = Frame(BrodSla, bd=3, relief="sunken", bg="#ff6b0f")
    frameImagen.grid(column=0, row=0, pady=10, padx=10)
    image = PhotoImage(file="icono2.png")
    LbImagen = Label(frameImagen, image=image)
    LbImagen.grid(column=0, row=0, pady=10, padx=10)

    framefunciones = Frame(frameImagen, bd=5, relief="groove", bg="#ff6b0f")
    framefunciones.grid(column=0, row=1, pady=10, padx=10)

    BtnVolverBS = Button(framefunciones, text='Volver', height=1, width=10, command=volverBroSlaRoot, fg="#ffffff",
                         bg="#ff6b0f")
    BtnVolverBS.grid(column=0, row=0)

    frameconfiguracion = Frame(BrodSla, bd=3, relief="sunken", bg="#ff6b0f")
    frameconfiguracion.grid(column=1, row=0, pady=10, padx=10)

    LbAgregarEsclavo = Label(frameconfiguracion, text="Agregar Esclavo/Broadcast", bg="#ff6b0f")
    LbAgregarEsclavo.grid(column=0, row=0)

    NombreEsclavoBroadcast = StringVar()
    DatoEsclavoBroadcast = Entry(frameconfiguracion, bg="#ffffff", borderwidth=4, width=5,
                                 textvariable=NombreEsclavoBroadcast,
                                 font=('Georgia 20'))
    DatoEsclavoBroadcast.grid(column=0, row=1, pady=10, padx=10)

    Lb1 = Label(frameconfiguracion, text="Direccion dispositivo", bg="#ff6b0f")
    Lb1.grid(column=0, row=2)
    Lb2 = Label(frameconfiguracion, text="5 caracteres", bg="#ff6b0f")
    Lb2.grid(column=0, row=3)

    NombreMaestroescbroad = StringVar()
    DatoMaestroescbroadt = Entry(frameconfiguracion, bg="#ffffff", borderwidth=4, width=5,
                                 textvariable=NombreMaestroescbroad,
                                 font=('Georgia 20'))
    DatoMaestroescbroadt .grid(column=0, row=4, pady=10, padx=10)

    Lb3 = Label(frameconfiguracion, text="Direccion dispositivo maestro", bg="#ff6b0f")
    Lb3.grid(column=0, row=5)
    Lb4 = Label(frameconfiguracion, text="5 caracteres", bg="#ff6b0f")
    Lb4.grid(column=0, row=6)





    BtnConfigurar = Button(frameconfiguracion, text='Configurar', height=1, width=10, command=agregarEsclavoBroadcast,
                           fg="#ffffff", bg="#ff6b0f")
    BtnConfigurar.grid(column=0, row=7)

    if (BrodSla):
        root.withdraw()
        BrodSla.deiconify()

    '''
    BrodSla = Toplevel()
    BrodSla .title("IOTHIX")
    BrodSla .geometry("310x400")
    BrodSla .config(bg="#f0f0f0", bd=5, relief="groove")
    BrodSla .resizable(0, 0)
    BrodSla .iconbitmap('icono.ico')
    BrodSla.overrideredirect(True)# quitar la barra de nombre junto con los botones de minimizar, maximizar y cerrar
    frameImagen = Frame(BrodSla , bd=3, relief="sunken", bg="#ff6b0f")
    frameImagen.grid(column=0, row=0, pady=10, padx=10)

    image = PhotoImage(file="icono2.png")

    LbImagen = Label(frameImagen, image=image)
    LbImagen.grid(column=0, row=0, pady=10, padx=10)

    frameBotones = Frame(frameImagen, bd=5, relief="groove", bg="#ff6b0f")
    frameBotones.grid(column=0, row=1, pady=10, padx=10)


   # BtnLeerDatos = Button(frameBotones, text='LeerConf', height=1, width=10, command=callleerArc, fg="#ffffff",
   #                       bg="#ff6b0f")
    #BtnLeerDatos.grid(column=0, row=3)

    #BtnEnvDatos = Button(frameBotones, text='ConfAcceso', height=1, width=10, command=callenviardatos, fg="#ffffff",
     #                    bg="#ff6b0f")
    #BtnEnvDatos.grid(column=0, row=4)


    BtnEnviarCom = Button(frameBotones, text='EnviarC', height=1, width=10, command=EnviarComando, fg="#ffffff",
                          bg="#ff6b0f")
    BtnEnviarCom.grid(column=0, row=7)

    NombreBrodSla = StringVar()
    DatoBrodSla = Entry(BrodSla, bg="#ffffff", borderwidth=4, width=2, textvariable=NombreBrodSla, font=('Georgia 20'))
    DatoBrodSla.place(x=180, y=10, width=90, height=50)

    LbNomBrodSla = Label(BrodSla, text="Direccion dispositivo")
    LbNomBrodSla.place(x=170, y=60, width=110, height=30)

    LbNomBrodSla2 = Label(BrodSla, text="5 caracteres")
    LbNomBrodSla2.place(x=180, y=80, width=90, height=30)



    BtnVolverBS= Button(BrodSla, text='Volver', height=1, width=10, command=volverBroSlaRoot, fg="#ffffff",bg="#ff6b0f")
    BtnVolverBS.place(x=180, y=350, width=90, height=30)
    '''


def volverBroSlaRoot():
    try:
        BrodSla.destroy()
        root.deiconify()
    except Exception as e:
        print(e)


def ventanaAgregarSlave():
    global Slave, BtnConectarS, BtnBuscar, DatoRecibido, frameBotones, BtnLeerArchivo, DatoRecibido, BtnVolverS, Master, NombreEsclavoMaster,DireccionSlaveBroadcast
    # instanciar el objeto Tk para creacion de GUI

    Slave = Toplevel()
    Slave.title("IOTHIX")
    Slave.geometry("310x400")
    Slave.config(bg="#f0f0f0", bd=5, relief="groove")
    Slave.resizable(0, 0)
    Slave.iconbitmap('icono.ico')
    Slave.overrideredirect(True)  # quitar la barra de nombre junto con los botones de minimizar, maximizar y cerrar

    frameImagen = Frame(Slave, bd=3, relief="sunken", bg="#ff6b0f")
    frameImagen.grid(column=0, row=0, pady=10, padx=10)
    image = PhotoImage(file="icono2.png")
    LbImagen = Label(frameImagen, image=image)
    LbImagen.grid(column=0, row=0, pady=10, padx=10)

    framefunciones = Frame(frameImagen, bd=5, relief="groove", bg="#ff6b0f")
    framefunciones.grid(column=0, row=1, pady=10, padx=10)

    BtnVolverS = Button(framefunciones, text='Volver', height=1, width=10, command=volverSlaveMaster, fg="#ffffff",
                        bg="#ff6b0f")
    BtnVolverS.grid(column=0, row=0)

    frameconfiguracion = Frame(Slave, bd=3, relief="sunken", bg="#ff6b0f")
    frameconfiguracion.grid(column=1, row=0, pady=10, padx=10)

    LbAgregarEsclavo = Label(frameconfiguracion, text="Agregar Esclavo", bg="#ff6b0f")
    LbAgregarEsclavo.grid(column=0, row=0)

    NombreEsclavoMaster = StringVar()
    DatoEsclavo = Entry(frameconfiguracion, bg="#ffffff", borderwidth=4, width=5, textvariable=NombreEsclavoMaster,
                        font=('Georgia 20'))
    DatoEsclavo.grid(column=0, row=1, pady=10, padx=10)

    Lb1 = Label(frameconfiguracion, text="Direccion dispositivo", bg="#ff6b0f")
    Lb1.grid(column=0, row=2)
    Lb2 = Label(frameconfiguracion, text="5 caracteres", bg="#ff6b0f")
    Lb2.grid(column=0, row=3)

    BtnConfigurar = Button(frameconfiguracion, text='Configurar', height=1, width=10, command=agregarEsclavoMaster,
                           fg="#ffffff", bg="#ff6b0f")
    BtnConfigurar.grid(column=0, row=3)

    if Slave:
        Master.withdraw()
        Slave.deiconify()


def volverSlaveMaster():
    try:
        Slave.destroy()
        Master.deiconify()
    except Exception as e:
        print(e)


def ventanaAgregarBroadcast():
    global Broadcast, BtnConectarB, BtnBuscar, DatoRecibido, frameBotones, BtnLeerArchivo, DatoRecibido, BtnVolverB, NombreBroadcast, ComboBroadcastActuales, BtnAgregarSlaveBroadcast, SlaveBroadcastDireccion, SlaveBroadcastNombre,NombreSlaveBroadcast,DireccionSlaveBroadcast
    Broadcast = Toplevel()
    Broadcast.title("IOTHIX")
    Broadcast.geometry("700x300")
    Broadcast.config(bg="#f0f0f0", bd=5, relief="groove")
    Broadcast.resizable(0, 0)
    Broadcast.iconbitmap('icono.ico')
    Broadcast.overrideredirect(True)  # quitar la barra de nombre junto con los botones de minimizar, maximizar y cerrar

    frameImagen = Frame(Broadcast, bd=3, relief="sunken", bg="#ff6b0f")
    frameImagen.grid(column=0, row=0, pady=10, padx=10)
    image = PhotoImage(file="icono2.png")
    LbImagen = Label(frameImagen, image=image)
    LbImagen.grid(column=0, row=0, pady=10, padx=10)

    framefunciones = Frame(frameImagen, bd=5, relief="groove", bg="#ff6b0f")
    framefunciones.grid(column=0, row=1, pady=10, padx=10)

    BtnVolverB = Button(framefunciones, text='Volver', height=1, width=10, command=volverBrodMaster, fg="#ffffff",
                        bg="#ff6b0f")
    BtnVolverB.grid(column=0, row=0)

    frameconfiguracion = Frame(Broadcast, bd=3, relief="sunken", bg="#ff6b0f")
    frameconfiguracion.grid(column=1, row=0, pady=10, padx=10)

    LbAgregarBroadcast = Label(frameconfiguracion, text="Agregar Broadcast", bg="#ff6b0f")
    LbAgregarBroadcast.grid(column=0, row=0)

    NombreBroadcast = StringVar()
    DatoBroadcast = Entry(frameconfiguracion, bg="#ffffff", borderwidth=4, width=5, textvariable=NombreBroadcast,
                          font=('Georgia 20'))
    DatoBroadcast.grid(column=0, row=1, pady=10, padx=10)

    LbNomBroadcast = Label(frameconfiguracion, text="Direccion dispositivo", bg="#ff6b0f")
    LbNomBroadcast.grid(column=0, row=2)
    LbNomBroadcast2 = Label(frameconfiguracion, text="5 caracteres", bg="#ff6b0f")
    LbNomBroadcast2.grid(column=0, row=3)

    BtnConfigurar = Button(frameconfiguracion, text='Configurar', height=1, width=10, command=agregarBroadcastMaster,
                           fg="#ffffff", bg="#ff6b0f")
    BtnConfigurar.grid(column=0, row=3)

    frameAgregarBroadcastSlave = Frame(Broadcast, bd=3, relief="sunken", bg="#ff6b0f")
    frameAgregarBroadcastSlave.grid(column=2, row=0, pady=10, padx=10)

    LbBroadActuales = Label(frameAgregarBroadcastSlave, text="Seleccionar Broadcast", bg="#ff6b0f")
    LbBroadActuales.grid(column=0, row=0)

    BroadcastActuales = StringVar()
    ComboBroadcastActuales = Combobox(frameAgregarBroadcastSlave, width=27, textvariable=BroadcastActuales)
    ComboBroadcastActuales.grid(column=0, row=1, pady=10, padx=10)

    frameAgregarSlave = Frame(frameAgregarBroadcastSlave, bd=3, relief="sunken", bg="#ff6b0f")
    frameAgregarSlave.grid(column=0, row=2, pady=10, padx=10)

    LbBroadActuales = Label(frameAgregarSlave, text="Agregar esclavo a broadcast ", bg="#ff6b0f")
    LbBroadActuales.grid(column=0, row=0)

    LbNombreSlaveBroadcast = Label(frameAgregarSlave, text="Nombre Esclavo", bg="#ff6b0f")
    LbNombreSlaveBroadcast.grid(column=0, row=1)

    SlaveBroadcastNombre = StringVar()
    NombreSlaveBroadcast = Entry(frameAgregarSlave, bg="#ffffff", borderwidth=4, width=10,
                                 textvariable=SlaveBroadcastNombre,
                                 font=('Georgia 20'))
    NombreSlaveBroadcast.grid(column=1, row=1, pady=10)

    LbDireccionSlaveBroadcast = Label(frameAgregarSlave, text="Direccion Esclavo", bg="#ff6b0f")
    LbDireccionSlaveBroadcast.grid(column=0, row=2)

    SlaveBroadcastDireccion = StringVar()
    DireccionSlaveBroadcast = Entry(frameAgregarSlave, bg="#ffffff", borderwidth=4, width=5,
                                    textvariable=SlaveBroadcastDireccion,
                                    font=('Georgia 20'))
    DireccionSlaveBroadcast.grid(column=1, row=2, pady=10)



    BtnAgregarSlaveBroadcast = Button(frameAgregarSlave, text='Agregar', height=1, width=10,
                                      command=agregarSlaveBroadcast,
                                      fg="#ffffff", bg="#ff6b0f")
    BtnAgregarSlaveBroadcast.grid(column=1, row=3)

    BtnAgregarSlaveBroadcast['state'] = 'disable'

    ActualizarComboBroadcast()

    if (Broadcast):
        Master.withdraw()
        Broadcast.deiconify()


def volverBrodMaster():
    try:
        Broadcast.destroy()
        Master.deiconify()
    except Exception as e:
        print(e)


def verificar_conexion(args):
    if "-" in pulso_actualizar.get():  # or "-" in pulso_baudios.get() or "-" in pulso_dbits.get() :
        BtnConectar["state"] = "disable"
    else:
        BtnConectar["state"] = "active"


def actualizar_puertos():
    global pulso_actualizar, desplegar_puertos
    # retorna en una lista los puertos detectados
    ports = serial.tools.list_ports.comports()
    # recorre la lista y asigna de forma dinamica los puertos encontrados
    coms = [com[0] for com in ports]
    coms.insert(0, "-")
    try:
        pulso_actualizar = StringVar()
        pulso_actualizar.set(coms[0])
        desplegar_puertos = OptionMenu(frameLogo, pulso_actualizar, *coms, command=verificar_conexion)
        desplegar_puertos.config(width=6, fg="#ffffff", bg="#ff6b0f")
        desplegar_puertos.grid(column=0, row=3)
        verificar_conexion(0)
    except Exception as e:
        desplegar_puertos.destroy()
        print("Error funcion update_coms")
        print(e)


def actualizar_puertos2():
    global pulso_actualizar, desplegar_puertos
    # retorna en una lista los puertos detectados
    ports = serial.tools.list_ports.comports()
    # recorre la lista y asigna de forma dinamica los puertos encontrados
    coms = [com[0] for com in ports]
    coms.insert(0, "-")
    try:
        pulso_actualizar = StringVar()
        pulso_actualizar.set(coms[0])
        desplegar_puertos = OptionMenu(frameLogo, pulso_actualizar, *coms)
        desplegar_puertos.config(width=6, fg="#ffffff", bg="#ff6b0f")
        desplegar_puertos.grid(column=0, row=3)
        #verificar_conexion(0)
    except Exception as e:
        desplegar_puertos.destroy()
        print("Error funcion update_coms")
        print(e)


def readSerial(puerto_open):
    global serialData
    while serialData:
        if puerto_open.is_open:
            data = puerto_open.readline()
            datoutil = str(data)

            if len(data) > 0 and (datoutil[0] == 'b' and '[' in datoutil and not ('(' in datoutil)):
                try:
                    trama_util = str(data)
                    trama_util = trama_util.replace('b"', '')
                    trama_util = trama_util.replace('\\r\\n"', '')
                    trama_util = trama_util.replace('[', '')
                    trama_util = trama_util.replace(']', '')
                    trama_util = trama_util.replace(',', '')
                    trama_util = trama_util.replace("'", '')
                    trama_util = (trama_util.split(" "))

                    #print(f"trama util {trama_util[0]}")
                    if trama_util[0] != '':
                        imprimir_valor(trama_util)
                except Exception as e:
                    print("Error lectura del puerto serial")
                    print(e)


def Abrir_Puerto():
    global serialData, puerto_serial, BtnLeerArchivo, BtnVolver, BtnVolverM, port, baud, dbits, BtnBuscar,BtnVolverI
    if root:
        if BtnConectar["text"] in "Desconectar":
            serialData = False
            BtnConectar["text"] = "Conectar"
            BtnBuscar["state"] = "active"
            desplegar_puertos["state"] = "active"
            BtnBroSla["state"] = "disable"
            BtnMaster["state"] = "disable"
            BtnBorrarConf["state"] = "disable"
            BtnVolverI["state"]="active"
           # BtnProgramar["state"]="disable"
            puerto_serial.close()
        else:
            serialData = True
            BtnConectar["text"] = "Desconectar"
            BtnBuscar["state"] = "disable"
            desplegar_puertos["state"] = "disable"
            BtnBroSla["state"] = "active"
            BtnMaster["state"] = "active"
            BtnBorrarConf["state"] = "active"
            BtnVolverI["state"] = "disable"
            #BtnProgramar["state"] = "active"
            port = pulso_actualizar.get()
            baud = 115200
            dbits = 8
            try:
                puerto_serial = serial.Serial(port=port, baudrate=baud, bytesize=dbits, timeout=None)
            except Exception as e:
                print("No se puede abrir el puerto")
                print(e)
            # se crea hilo de apertura de puertos seriales
            t1 = threading.Thread(target=readSerial, args=(puerto_serial,))
            t1.deamon = True
            t1.start()
            try:
                if BtnConectar["text"] in "Desconectar":
                    puerto_serial.write('\x03'.encode())
                    puerto_serial.write('Leer_Archivo()\n\r'.encode())
            except Exception as e:
                print("Problemas envio")
                print(e)


def close_window():
    global inicio,root, serialData
    if messagebox.askokcancel("Cerrar", "Quiere finalizar la apliacion de configuracion?"):
        serialData = False
        inicio.destroy()


def detener_programa():
    puerto_serial.write('\x03'.encode())
    DatoRecibido.delete("1.0", "end")


def EnviarComando():
    puerto_serial.write(f'Leer_Archivo()\n\r'.encode())

    # DatoRecibido.delete("1.0", "end")
    print(f'Leer_Archivo()\n\r'.encode())


def callleerArc():
    try:
        if BtnConectar["text"] in "Desconectar":
            puerto_serial.write('Leer_Archivo()\n\r'.encode())
    except Exception as e:
        print("Problemas envio")
        print(e)


def callfuncionconf():
    try:
        if BtnConectar["text"] in "Desconectar":
            # puerto_serial.write("Configurar_Acceso(['[MASTER]', 'MAS01', '[ENDPOINT]', 'ENDPOINT01-END01', 'ENDPOINT02-END02', '[BROADCAST]','BRO001'])\n\r".encode())
            puerto_serial.write(
                "Configurar_Acceso(['[ENDPOINT]', 'ENDPOINT01-END01', 'ENDPOINT02-END02', '[BROADCAST]','BRO001'])\n\r".encode())
            # puerto_serial.write("Configurar_Acceso(['[MASTER]', 'MAS01'])\\n\\r".encode())
            # puerto_serial.write("Configurar_Acceso(['[MASTER]', 'MAS01'])\n\r".encode())
            # DatoRecibido.delete("1.0","end")
            # print('Ingreso a configuracion'.encode())
    except Exception as e:
        print("Problemas envio")
        print(e)


def callenviardatos():
    try:
        if BtnConectar["text"] in "Desconectar":
            # direcciones = DatoRecibido.get("1.0", END)
            direcciones = ["abcd", ]
            puerto_serial.write(f'Configurar_Acceso({direcciones})\n\r'.encode())
            # DatoRecibido.delete("1.0", "end")
            print('Envio paquete de datos'.encode())
    except Exception as e:
        print("Problemas envio")
        print(e)


def Borrar_Conf():
    try:
        if BtnConectar["text"] in "Desconectar":
            if messagebox.askokcancel("Eliminar Configuración",
                                      "Se eliminaran los registros de direcciones del dispositivo conectado actualmente, una vez se ejecute el proceso la informacion no podra ser recuperada,Desea continuar?"):
                puerto_serial.write(f'Borrar_Configuracion()\n\r'.encode())
                messagebox.showinfo("Eliminación", "Se elimino el archivo de configuracion del dispositivo")
                callleerArc()
    except Exception as e:
        print("Problemas envio")
        print(e)


def ActualizarComboBroadcast():
    global BtnAgregarSlaveBroadcast
    callleerArc()
    if len(direcciones) > 2:
        if direcciones[2] == 'BROADCAST':
            posicion_broadcast = direcciones.index('BROADCAST')
            posicion_endpoint = direcciones.index('ENDPOINT')
            itemsCombo = []
            for items in range(posicion_broadcast + 1, posicion_endpoint):
                itemsCombo.append(direcciones[items])
            ComboBroadcastActuales['values'] = itemsCombo
            if len(direcciones) > 4:
                BtnAgregarSlaveBroadcast['state'] = 'active'
        else:
            BtnAgregarSlaveBroadcast['state'] = 'disable'


def agregarBroadcastMaster():
    try:
        if BtnConectar["text"] in "Desconectar":
            """crear nuevo arreglo con datos del broadcast a agregar"""

            if len(direcciones) == 2:
                direcciones.append("BROADCAST")
                direcciones.append("ENDPOINT")
                if len(NombreBroadcast.get()) > 0 and len(NombreBroadcast.get()) < 6:
                    verifica = f"{NombreBroadcast.get().upper()}" in direcciones
                    if not verifica:
                        direcciones.insert(3, f'{NombreBroadcast.get().replace(" ","").upper()}')
                        puerto_serial.write(f'Configurar_Acceso({direcciones})\n\r'.encode())
                        messagebox.showinfo("Configuracion ejecutada",
                                            f'Se añadio el broadcast con direccion {NombreBroadcast.get().replace(" ","").upper()} al dispositivo conectado maestro')
                        posicion_broadcast = direcciones.index('BROADCAST')
                        posicion_endpoint = direcciones.index('ENDPOINT')
                        itemsCombo = []
                        for items in range(posicion_broadcast + 1, posicion_endpoint):
                            itemsCombo.append(items)
                        ComboBroadcastActuales['values'] = itemsCombo
                        volverBrodMaster()
                    else:
                        messagebox.showerror("Error en direccion", "La direccion digitada ya existe")
                else:
                    messagebox.showerror("Error en direccion",
                                         "La direccion a asignar al broadcast no puede estar vacia o ser mayor a 5 caracteres")
            else:
                if len(NombreBroadcast.get()) > 0 and len(NombreBroadcast.get()) < 6:
                    verifica = f"{NombreBroadcast.get().upper()}" in direcciones
                    if not verifica:
                        direcciones.insert(3, f'{NombreBroadcast.get().replace(" ","").upper()}')
                        puerto_serial.write(f'Configurar_Acceso({direcciones})\n\r'.encode())
                        messagebox.showinfo("Configuracion ejecutada",
                                            f"Se añadio el broadcast con direccion {NombreBroadcast.get().upper()} al dispositivo conectado maestro")
                        posicion_broadcast = direcciones.index('BROADCAST')
                        posicion_endpoint = direcciones.index('ENDPOINT')
                        itemsCombo = []
                        for items in range(posicion_broadcast + 1, posicion_endpoint):
                            itemsCombo.append(direcciones[items])
                        ComboBroadcastActuales['values'] = itemsCombo
                        volverBrodMaster()
                    else:
                        messagebox.showerror("Error en direccion", "La direccion digitada ya existe")
                else:
                    messagebox.showerror("Error en direccion",
                                         "La direccion a asignar al broadcast no puede estar vacia o ser mayor a 5 caracteres")
    except Exception as e:
        print("Problemas envio")
        print(e)


def agregarEsclavoBroadcast():
    if(len(NombreEsclavoBroadcast.get()) > 0 and len(NombreEsclavoBroadcast.get()) < 6) and (len(NombreMaestroescbroad.get())>0 and len(NombreMaestroescbroad.get()) < 6):
    #if len(NombreEsclavoBroadcast.get()) > 0 and len(NombreEsclavoBroadcast.get()) < 6:

        #print(NombreEsclavoBroadcast.get().replace(" ","").upper())
        #print(NombreMaestroescbroad.get().replace(" ", "").upper())

        #paquete = [NombreEsclavoBroadcast.get().upper()]
        paquete = ["other",NombreEsclavoBroadcast.get().replace(" ","").upper(),NombreMaestroescbroad.get().replace(" ", "").upper()]
        puerto_serial.write(f'Configurar_Acceso({paquete})\n\r'.encode())
        messagebox.showinfo("Actualizacion de configuracion",
                            f"Se configuro el dispositivo con la direccion {NombreEsclavoBroadcast.get().upper()}")
    else:
        messagebox.showinfo("Error en nombre de dispositivo",
                            "El nombre asignado NO puede estar vacio y debe tener una extension maxima de 5 caracteres")


def agregarSlaveBroadcast():
    global DireccionSlaveBroadcast,NombreSlaveBroadcast
    try:
        if BtnConectar["text"] in "Desconectar":
            if (len(SlaveBroadcastNombre.get()) > 0 and len(SlaveBroadcastNombre.get()) < 11) and (
                    len(SlaveBroadcastDireccion.get()) > 0 and len(SlaveBroadcastDireccion.get()) < 6):
                direccioncompletaSlaveBroadcast = f'{ComboBroadcastActuales.get().replace(" ","").upper()}-{SlaveBroadcastNombre.get().replace(" ","").upper()}-{SlaveBroadcastDireccion.get().replace(" ","").upper()}'
                callleerArc()
                for x in direcciones:
                    print(x)

                print(direccioncompletaSlaveBroadcast)
                verifica = direccioncompletaSlaveBroadcast in direcciones
                if not verifica:
                    direcciones.append(f"{direccioncompletaSlaveBroadcast}")
                    puerto_serial.write(f'Configurar_Acceso({direcciones})\n\r'.encode())
                    messagebox.showinfo("Configuracion ejecutada",
                                        f'Se añadio el esclavo con nombre y direccion {SlaveBroadcastNombre.get().replace(" ","").upper()}-{SlaveBroadcastDireccion.get().replace(" ","").upper()} al broadcast con direccion {ComboBroadcastActuales.get().replace(" ","").upper()} al dispositivo conectado maestro')
                    # posicion_broadcast = direcciones.index('BROADCAST')
                    # posicion_endpoint = direcciones.index('ENDPOINT')
                    # itemsCombo = []
                    # for items in range(posicion_broadcast + 1, posicion_endpoint):
                    #   itemsCombo.append(direcciones[items])
                    # ComboBroadcastActuales['values'] = itemsCombo
                    # volverBrodMaster()
                    #DireccionSlaveBroadcast["text"]=''
                    DireccionSlaveBroadcast.delete(0,END)
                    NombreSlaveBroadcast.delete(0,END)

                else:
                    messagebox.showerror("Error en direccion", "La direccion digitada ya existe")
            else:
                messagebox.showerror("Error en direccion",
                                     "La direccion del esclavo puede tener maximo 5 caracteres y el nombre del esclavo no puede exceder los 10 caracteres")
    except Exception as e:
        print("Problemas envio")
        print(e)


def agregarEsclavoMaster():
    if len(direcciones) == 2:
        direcciones.append("BROADCAST")
        direcciones.append("ENDPOINT")
        if len(NombreEsclavoMaster.get()) > 0 and len(NombreEsclavoMaster.get()) < 6:
            verifica = NombreEsclavoMaster.get().upper() in direcciones
            if not verifica:
                direcciones.append(f'{NombreEsclavoMaster.get().replace(" ","").upper()}')
                puerto_serial.write(f'Configurar_Acceso({direcciones})\n\r'.encode())
                messagebox.showinfo("Configuracion ejecutada",
                                    f"Se añadio el esclavo con nombre {NombreEsclavoMaster.get().upper()} al dispositivo maestro con direccion {NombreMaster.get().upper()}")
                callleerArc()
                # volverSlaveMaster()
            else:
                messagebox.showerror("Error en direccion", "La direccion digitada ya existe")
        else:
            messagebox.showerror("Error en direccion",
                                 "La direccion del esclavo NO puede estar vacia y debe tener maximo 5 caracteres ")
    else:
        if len(NombreEsclavoMaster.get()) > 0 and len(NombreEsclavoMaster.get()) < 6:
            verifica = NombreEsclavoMaster.get().upper() in direcciones
            if not verifica:
                direcciones.append(f'{NombreEsclavoMaster.get().replace(" ","").upper()}')
                puerto_serial.write(f'Configurar_Acceso({direcciones})\n\r'.encode())
                messagebox.showinfo("Configuracion ejecutada",
                                    f"Se añadio el esclavo con nombre {NombreEsclavoMaster.get().upper()} al dispositivo maestro con direccion {NombreMaster.get().upper()}")
                callleerArc()
                # volverSlaveMaster()
            else:
                messagebox.showerror("Error en direccion", "La direccion digitada ya existe")
        else:
            messagebox.showerror("Error en direccion",
                                 "La direccion del esclavo NO puede estar vacia y debe tener maximo 5 caracteres ")


def callenviardatosMaster():
    try:
        if BtnConectar["text"] in "Desconectar":
            if len(NombreMaster.get()) < 6:
                puerto_serial.write(f"Configurar_Acceso(['MASTER','{NombreMaster.get().replace(' ','').upper()}'])\n\r".encode())
                messagebox.showinfo("Configuracion ejecutada",
                                    f"Se asigno la direccion {NombreMaster.get().upper()} al dispositivo conectado")
                volverMasterRoot()
            else:
                messagebox.showerror("Error en direccion",
                                     "El tamaño maximo del nombre para la direccion del maestro es de 5 caracteres")
    except Exception as e:
        print("Problemas envio")
        print(e)


def imprimir_valor(trama):
    global DatoMaster, direcciones, conf_readymaster, dirBroadcast
    direcciones = trama

    if trama[0] == "MASTER":
        #print("preconfigurado master")
        conf_readymaster = 1
        BtnBroSla['state'] = 'disable'
        # for x in direcciones:
        #   print(x)
    else:
        #print("sin configurar")
        conf_readymaster = 0
        BtnBroSla['state'] = 'active'
    puerto_serial.flush()


#Programa()
inicio()