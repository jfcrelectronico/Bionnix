#region identification
# Perimetral BasePerimetralBroadcast module 
# Authors: 
#    Jony Carmona
#    Jhojan Poveda
#    Alejandro Beltrán 
#endregion 

#region imports
from BasePerimetral import BasePerimetralClass, rxPollDelay, slaveSendDelay, timeoutLimit, commands2Broadcast
import utime
#endregion 

#region Broadcast Class
class Broadcast(BasePerimetralClass):
    def __init__(self, address = "br000", master_address = "mastr") -> None:
        super().__init__(address, master_address = master_address)

    def GetEndPoints(self):
        self.radio.open_tx_pipe(self.address.encode())
        self.radio.open_rx_pipe(1, self.masterAddress.encode())
        self.radio.start_listening()
        
        print("Waiting for incoming package from master on " + self.masterAddress)

        while True:
            if self.radio.any():
                while self.radio.any():
                    rxBuff = self.radio.recv()
                
                rxBuff = rxBuff.decode().split("^")
                
                # Give master time to get into receive mode.
                utime.sleep_ms(slaveSendDelay)
                utime.sleep_ms(2)
                self.radio.stop_listening()
                
                if rxBuff[0] == self.address:
                    try:
                        txBuff = "ok".encode()
                        self.radio.send(txBuff)
                    except OSError:
                        pass

                    print("The EndPoint was received and the answer was sent")

                    if rxBuff[1] != "A":
                        self.AddEndPoint(rxBuff[1], rxBuff[2])
                    else:
                        print("\n\n")
                        self.ShowEndPoints()
                        print("The EndPoints were added succesfully")
                        #self.Listen()
                        return "ok"
                    
                utime.sleep_ms(rxPollDelay)
                self.radio.start_listening()
    
    def Listen(self):
        self.radio.open_tx_pipe(self.address.encode())
        self.radio.open_rx_pipe(1, self.masterAddress.encode())
        self.radio.start_listening()
        print("Waiting for incoming package from master on " + self.masterAddress)

        while True:
            if self.radio.any():
                while self.radio.any():
                    rxBuff = self.radio.recv()

                rxBuff = rxBuff.decode().split("^")
                # Give master time to get into receive mode.
                utime.sleep_ms(slaveSendDelay)
                self.radio.stop_listening()

                try:
                    if rxBuff[0] == self.address:
                        self.radio.send("ok^".encode())
                except OSError:
                    pass
                    
                print("The response was sent")
                utime.sleep_ms(rxPollDelay)

                if rxBuff[0] == self.address:
                    if int(rxBuff[1]) == commands2Broadcast["check EndPoints"]:
                        print("Verifying the EndPoints status")
                        utime.sleep_ms(5)
                        self.CheckEndPoints()
                        self.ShowEndPoints()
                    elif int(rxBuff[1]) == commands2Broadcast["read EndPoints"]:
                        self.radio.start_listening()
                        print("Reading the EndPoints status")
                        while True:
                            if self.radio.any():
                                while self.radio.any():
                                    rxBuff = self.radio.recv()

                                rxBuff = rxBuff.decode().split("^")

                                if rxBuff[0] == "end":
                                    break
                                else:
                                    deviceFound = 0
                                    for endpoint in self.routingTableEndPoint:
                                        if rxBuff[0] == endpoint.address:
                                            frame = "m^" + endpoint.BuildFrame2Master()
                                            print(frame)
                                            deviceFound = deviceFound + 1
                                            break

                                    if deviceFound == 0:
                                        print("The endpoint {} was not found in the broadcast".format(rxBuff[0]))
                                        frame = "m^" + "NotFound^"

                                    # Give master time to get into receive mode.
                                    utime.sleep_ms(slaveSendDelay)
                                    self.radio.stop_listening()

                                    try:
                                        self.radio.send(frame.encode())
                                        pass
                                    except OSError:
                                        pass
                                utime.sleep_ms(rxPollDelay)
                                self.radio.start_listening()

                    elif int(rxBuff[1]) == commands2Broadcast["clear EndPoints"]:
                        print("Clearing the EndPoints detections and alarms")
                        utime.sleep_ms(5)
                        self.ClearDetectionsEndPoints()
                    
                    elif int(rxBuff[1]) == commands2Broadcast["start alarms EndPoints"]:
                        print("starting alarms of the EndPoints")
                        utime.sleep_ms(5)
                        self.StartAlarmsEndPoints()

                    self.radio.stop_listening()
                    self.radio.open_tx_pipe(self.address.encode())
                    self.radio.open_rx_pipe(1, self.masterAddress.encode())

                else:
                    print("The address is incorrect. The one that arrived was {}".format(rxBuff[0]))
                
                utime.sleep_ms(rxPollDelay)
                self.radio.start_listening()
    
    def __str__(self):
        return "Broadcast in '{}' address \nMaster address: {}".format(self.address, self.masterAddress)
#endregion 