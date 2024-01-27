#region identification
# Perimetral main Broadcast
# Authors: 
#    Jony Carmona
#    Jhojan Poveda
#    Alejandro Beltrán 
#endregion

from Broadcast import Broadcast 

print("Creating Broadcats\n")
Broadcast = Broadcast()
print(Broadcast)

def main():
    Broadcast.GetEndPoints()
    Broadcast.Listen()