import os

#os.system('cmd /k "pip3 install adafruit-ampy"')
#os.system('cmd /k "ampy --help"')

#os.system('cmd /k "cd C:\documentos\perimetral\serialesp8266 & ampy --port "COM4" put main.py"')#cd C:\documentos\perimetral\serialesp8266

#os.system('cmd /k "cd C:\Program Files (x86)\smartgrid\endpoint & ampy --port "COM4" put main.py"')#cd C:\documentos\perimetral\serialesp8266
#os.system('cmd /k "cd C:\Program Files (x86)\smartgrid\broadcast & ampy --port "COM4" put main.py"')#cd C:\documentos\perimetral\serialesp8266
#os.system('cmd /k "cd C:\Program Files (x86)\smartgrid\master & ampy --port "COM4" put main.py"')#cd C:\documentos\perimetral\serialesp8266

os.system('cmd /k "cd C:\Program Files (x86)\SmartGrid\master "')

os.system('cmd /k " ampy --port "COM4" put Master.py "')

os.system('cmd /k "ampy --port "COM4" put BasePerimetral.py"')
   # print("espere")
    #os.listdir()
#os.system(f'cmd /k "cd C:\Program Files (x86)\SmartGrid\master & ampy --port "COM4" put BasePerimetral.py"')


#os.system('cmd /k "ampy --port "COM4" put main.py"')