#region identification
# Perimetral main EndPoint
# Authors: 
#    Jony Carmona
#    Jhojan Poveda
#    Alejandro Beltrán 
#endregion

from EndPoint import EndPoint

print("\n\nPrograma de prueba\n\n")

print("Creating the EndPoint Device\n")
EndPoint = EndPoint(on_High_alarm=5)
EndPoint.SetMasterAddress("mastr")
print(EndPoint)

def main():
    EndPoint.Listen()