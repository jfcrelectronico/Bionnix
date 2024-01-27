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
    root.geometry("860x450")
    root.config(bg="#f0f0f0",bd=5,relief="groove")
    #root.resizable(0, 0)
    root.iconbitmap('icono.ico')

    frameImagen = Frame(root, bd=3, relief="sunken",bg="#ff6b0f")
    frameImagen.grid(column=0, row=0, pady=10, padx=10)

    image = PhotoImage(file="icono2.png")

    LbImagen = Label(frameImagen,image=image)
    LbImagen.grid(column=0, row=0, pady=10, padx=10)

    #image2 = PhotoImage(file="barraN.png")

    #Lblinea = Label(frameImagen, image=image2)
    # Lblinea.grid(column=0, row=1)
    #Lblinea.grid(column=0, row=1)


    frameBotones=Frame(frameImagen,bd=5,relief="groove",bg="#ff6b0f")
    frameBotones.grid(column=0, row=1, pady=10, padx=10)

    #ETIQUETAS PARA IDENTIFICAR A QUE CAMPO CORRESPONDE CADA ITEM
    #LbPuerto = Label(frameBotones, text="Puertos Detectados: ", bg="#f0f0f0")
    #LbPuerto.grid(column=1, row=1, pady=10, padx=10)

    # BOTONES PARA A GENERARA CONEXION SERIAL
    BtnBuscar = Button(frameBotones, text="Buscar Puertos", height=1, width=10, command=actualizar_puertos,fg="#ffffff",bg="#ff6b0f")
    BtnBuscar.grid(column=0, row=0)

    BtnConectar = Button(frameBotones, text="Conectar", height=1, width=10, state="disabled", command=Abrir_Puerto,fg="#ffffff",bg="#ff6b0f")
    BtnConectar.grid(column=0, row=1)

    BtnLeerDatos = Button(frameBotones, text='LeerConf', height=1, width=10, command=callleerArc,fg="#ffffff",bg="#ff6b0f")
    BtnLeerDatos.grid(column=0, row=3)

    BtnEnvDatos = Button(frameBotones, text='ConfAcceso', height=1, width=10, command=callenviardatos,fg="#ffffff",bg="#ff6b0f")
    BtnEnvDatos.grid(column=0, row=4)

    BtnEnvDet = Button(frameBotones, text='callFunConf', height=1, width=10, command=callfuncionconf,fg="#ffffff",bg="#ff6b0f")
    BtnEnvDet.grid(column=0, row=5)

    BtnDetener = Button(frameBotones, text='DetEjec', height=1, width=10, command=detener_programa,fg="#ffffff",bg="#ff6b0f")
    BtnDetener.grid(column=0, row=6)

    BtnEnviarCom = Button(frameBotones, text='EnviarC', height=1, width=10, command=EnviarComando,fg="#ffffff",bg="#ff6b0f")
    BtnEnviarCom.grid(column=0, row=7)

    actualizar_puertos()
    ScrollDatoRecibido = Scrollbar(root, bg="#f0f0f0", orient='vertical')
    ScrollDatoRecibido.grid(column=2, row=0,sticky=NS)
    DatoRecibido = Text(root, bg="#ffffff",yscrollcommand=ScrollDatoRecibido.set,borderwidth = 4)
    DatoRecibido.grid(column=1, row=0, pady=20, padx=10)
    ScrollDatoRecibido.config(command=DatoRecibido.yview)
    root.protocol("WM_DELETE_WINDOW", close_window)
    root.mainloop()

# verifica si se selecciono una opcion valida en el menu desplgable puertos
def verificar_conexion(args):
    if "-" in pulso_actualizar.get() :#or "-" in pulso_baudios.get() or "-" in pulso_dbits.get() :
        BtnConectar["state"] = "disable"
    else:
        BtnConectar["state"] = "active"
def actualizar_puertos():
    global pulso_actualizar, desplegar_puertos
    #retorna en una lista los puertos detectados
    ports = serial.tools.list_ports.comports()
    #recorre la lista y asigna de forma dinamica los puertos encontrados
    coms = [com[0] for com in ports]
    coms.insert(0, "-")
    try:
        pulso_actualizar = StringVar()
        pulso_actualizar.set(coms[0])
        desplegar_puertos = OptionMenu(frameBotones, pulso_actualizar, *coms, command=verificar_conexion)
        desplegar_puertos.config(width=6,fg="#ffffff",bg="#ff6b0f")
        desplegar_puertos.grid(column=0, row=2)
        verificar_conexion(0)
    except:
        desplegar_puertos.destroy()
        print("Error funcion update_coms")
#lee los datos encontrados en el puerto serial, la funcion esta corriendo en un hilo paralelo a la GUI
def readSerial(puerto_open):
    global serialData
    while serialData:
        data = puerto_open.readline()
        print(f'dato recibido: {data} ')
        if len(data) > 0:
            try:
                trama_util = str(data)
                #quitar de a trama los caracteres que no son utiles, las letras mayusculas NO pueden ser eliminadas usando este metodo
                trama_filtrada = trama_util.strip("'b'\\r\\n")
                imprimir_valor(trama_filtrada)
            except:
                print("Error lectura del puerto serial")
#los datos capturados a traves del puerto serial son enviados a los label correspondientes
def imprimir_valor(trama):
    DatoRecibido.insert(END,f'{trama}\n')
    puerto_serial.flush()
def callfuncionconf():
    try:
        if BtnConectar["text"] in "Desconectar":
            puerto_serial.write('Enviar()\n\r'.encode())
            DatoRecibido.delete("1.0","end")
            print('Ingreso a configuracion'.encode())
    except:
        print("Problemas envio")
def callenviardatos():
    try:
        if BtnConectar["text"] in "Desconectar":
            direcciones = DatoRecibido.get("1.0", END)
            puerto_serial.write(f'Configurar_Acceso({direcciones})\n\r'.encode())
            DatoRecibido.delete("1.0", "end")
            print('Envio paquete de datos'.encode())
    except:
        print("Problemas envio")

def callleerArc():
    try:
        if BtnConectar["text"] in "Desconectar":
            puerto_serial.write('Leer_Archivo()\n\r'.encode())
            DatoRecibido.delete("1.0", "end")
            print('Lectura de configuracion actual'.encode())
    except:
        print("Problemas envio")

def Abrir_Puerto():
    global serialData, puerto_serial,BtnLeerArchivo
    if BtnConectar["text"] in "Desconectar":
        serialData = False
        BtnConectar["text"] = "Conectar"
        BtnBuscar["state"] = "active"
        desplegar_puertos["state"] = "active"
        DatoRecibido.delete("1.0", "end")
        puerto_serial.close()
    else:
        serialData = True
        BtnConectar["text"] = "Desconectar"
        BtnBuscar["state"] = "disable"
        desplegar_puertos["state"] = "disable"
        port = pulso_actualizar.get()
        baud = 115200
        dbits =8
        try:
            puerto_serial = serial.Serial(port=port, baudrate=baud, bytesize=dbits, timeout=None)
        except:
            print("Error funcion connexion")
        #se crea hilo de apertura de puertos seriales
        t1 = threading.Thread(target=readSerial, args=(puerto_serial,))
        t1.deamon = True
        t1.start()

def close_window():
    global root, serialData
    if messagebox.askokcancel("Cerrar", "Quiere finalizar la apliacion de configuracion?"):
        serialData = False
        root.destroy()

def detener_programa():
    puerto_serial.write('\x03'.encode())
    DatoRecibido.delete("1.0", "end")

def EnviarComando():
    comando=DatoRecibido.get("1.0",END)
    puerto_serial.write(f'{comando}\n\r'.encode())
    DatoRecibido.delete("1.0", "end")
    print(comando)

Programa()
#root.protocol("WM_DELETE_WINDOW", close_window)
#root.mainloop()