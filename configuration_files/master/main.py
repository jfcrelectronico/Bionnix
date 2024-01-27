#region identification
# Perimetral main Master
# Authors: 
#    Jony Carmona
#    Jhojan Poveda
#    Alejandro Beltrán 
#endregion

from Master import Master
import time

print("\n\nPrograma de prueba\n\n")

print("Creating the Master Device\n")

Master = Master()
print(Master)

Master.AddEndPoint("zn000", "Zona 0")
# Master.AddEndPoint("zn001", "Zona 1")
# Master.AddEndPoint("zn002", "Zona 2")
# Master.AddEndPoint("zn003", "Zona 3")
# Master.AddEndPoint("zn004", "Zona 4")
# Master.AddEndPoint("zn005", "Zona 5")
# Master.AddEndPoint("zn006", "Zona 6")
# Master.AddEndPoint("zn007", "Zona 7")
# Master.AddEndPoint("zn008", "Zona 8")
# Master.AddEndPoint("zn009", "Zona 9")

Master.ShowEndPoints()

Master.AddBroadcast("br000")
Master.ShowBroadcast()

Master.AddEndPointBroadcast("br000","zn001", "Zona 1")
Master.ShowEndPointsBroadcast("br000")


# Master.AddBroadcast("br000")
# Master.AddBroadcast("br001")
# Master.AddBroadcast("br002")

# Master.ShowBroadcast()

# Master.AddEndPointBroadcast("br000","zn000", "Zona 0")
# Master.AddEndPointBroadcast("br000","zn001", "Zona 1")
# Master.AddEndPointBroadcast("br000","zn002", "Zona 2")
# Master.AddEndPointBroadcast("br000","zn003", "Zona 3")
# Master.AddEndPointBroadcast("br000","zn004", "Zona 4")
# Master.AddEndPointBroadcast("br000","zn005", "Zona 5")
# Master.AddEndPointBroadcast("br000","zn006", "Zona 6")
# Master.AddEndPointBroadcast("br000","zn007", "Zona 7")
# Master.AddEndPointBroadcast("br000","zn008", "Zona 8")
# Master.AddEndPointBroadcast("br000","zn009", "Zona 9")

# Master.AddEndPointBroadcast("br001","zn010", "Zona 10")
# Master.AddEndPointBroadcast("br001","zn011", "Zona 11")
# Master.AddEndPointBroadcast("br001","zn012", "Zona 12")
# Master.AddEndPointBroadcast("br001","zn013", "Zona 13")
# Master.AddEndPointBroadcast("br001","zn014", "Zona 14")
# Master.AddEndPointBroadcast("br001","zn015", "Zona 15")
# Master.AddEndPointBroadcast("br001","zn016", "Zona 16")
# Master.AddEndPointBroadcast("br001","zn017", "Zona 17")
# Master.AddEndPointBroadcast("br001","zn018", "Zona 18")
# Master.AddEndPointBroadcast("br001","zn019", "Zona 19")

# Master.AddEndPointBroadcast("br002","zn020", "Zona 20")
# Master.AddEndPointBroadcast("br002","zn021", "Zona 21")
# Master.AddEndPointBroadcast("br002","zn022", "Zona 22")
# Master.AddEndPointBroadcast("br002","zn023", "Zona 23")
# Master.AddEndPointBroadcast("br002","zn024", "Zona 24")
# Master.AddEndPointBroadcast("br002","zn025", "Zona 25")
# Master.AddEndPointBroadcast("br002","zn026", "Zona 26")
# Master.AddEndPointBroadcast("br002","zn027", "Zona 27")
# Master.AddEndPointBroadcast("br002","zn028", "Zona 28")
# Master.AddEndPointBroadcast("br002","zn029", "Zona 29")

# Master.ShowEndPointsBroadcast("br000")
# Master.ShowEndPointsBroadcast("br001")
# Master.ShowEndPointsBroadcast("br002")

def main():
    Master.ChargeBroadcast()
    while True:
        Master.CheckEndPoints()
        Master.SendCommandBroadcast(Master.commands2Broadcast["check EndPoints"])
        time.sleep_ms(250)
        Master.SendCommandBroadcast(Master.commands2Broadcast["read EndPoints"])
        Master.UserInterface()
        
        

