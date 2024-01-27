#region identification
# Perimetral Master module
# Authors: 
#    Jony Carmona
#    Jhojan Poveda
#    Alejandro Beltrán 
#endregion

#region imports
from BasePerimetral import BasePerimetralClass, timeoutLimit, commands2Broadcast
from machine import Pin
from micropython import const
import utime
from pico_i2c_lcd import Screen
#endregion

#region constants
masterAlarmPin = const(2)
upButtonPin = const(36)
rightButtonPin = const(39)
downButtonPin = const(34)
leftButtonPin = const(35)
masterSCL = const(22)
masterSDA = const(21)
#endregion

#region Master Class
class Master(BasePerimetralClass):
    def __init__(self, address="mastr", master_address = None) -> None:
        super().__init__(address, master_address = master_address)
        #self.alarmPin = Pin(masterAlarmPin, mode = Pin.OUT, value = 0)
        #self.clearAlarmPin = Pin(masterClearAlarmPin, mode = Pin.IN)
        #self.clearAlarmPin.irq(trigger=Pin.IRQ_FALLING, handler=self.ClearAlarm)
        self.upButton = Pin(upButtonPin, mode = Pin.IN)
        self.upButton.irq(trigger = Pin.IRQ_FALLING, handler = self.ReadButtons)
        self.rigthButton = Pin(rightButtonPin, mode = Pin.IN)
        self.rigthButton.irq(trigger = Pin.IRQ_FALLING, handler = self.ReadButtons)
        self.downButton = Pin(downButtonPin, mode = Pin.IN)
        self.downButton.irq(trigger = Pin.IRQ_FALLING, handler = self.ReadButtons)
        self.leftButton = Pin(leftButtonPin, mode = Pin.IN)
        self.leftButton.irq(trigger = Pin.IRQ_FALLING, handler = self.ReadButtons)
        self.lcd = Screen(masterSCL, masterSDA)
        self.lcd.DefaultMessage()
        self.rowOnLCD = 0
        self.commands2Broadcast = commands2Broadcast

    def StartAlarm(self):
        self.alarmPin.on()
        print("\nThe alarm was set")
        return "ok"
    
    def ClearAlarm(self, p):
        self.alarmPin.off()
        print("\nThe alarm was cleared")
        return "ok"
    
    def ReadButtons(self, p) -> str:
        if self.upButton.value() == 0:
            self.UserInterface("up")
            utime.sleep_ms(25)
            return
        if self.rigthButton.value() == 0:
            self.UserInterface("rigth")
            utime.sleep_ms(25)
            return
        if self.downButton.value() == 0:
            self.UserInterface("down")
            utime.sleep_ms(25)
            return
        if self.leftButton.value() == 0:
            self.UserInterface("left")
            utime.sleep_ms(25)
            return

    def ChargeBroadcast(self):
        if len(self.routingTableBroadcast):
            for broadcast in self.routingTableBroadcast:
                print("===========================")
                print(broadcast)
                print("---------------------------")
                
                self.radio.stop_listening()
                self.radio.open_tx_pipe(self.address.encode())
                self.radio.open_rx_pipe(1, broadcast.address.encode())
                self.radio.start_listening()
                utime.sleep_ms(1)
                self.radio.stop_listening()

                if len(broadcast.routingTableEndPoint):
                    for endpoint in broadcast.routingTableEndPoint:
                        self.radio.stop_listening()
                        frame = broadcast.address + "^" + endpoint.address + "^" + endpoint.name + "^"

                        try:
                            print("Sending " + frame)
                            self.radio.send(frame.encode())
                        except OSError:
                            pass
                        
                        self.radio.start_listening()
                        start_time = utime.ticks_ms()
                        timeout = False
                        while not self.radio.any() and not timeout:
                            if utime.ticks_diff(utime.ticks_ms(), start_time) > timeoutLimit:
                                timeout = True
                        if timeout:
                            print("\nCan not connect with Broadcast {} please check the device".format(broadcast))
                            broadcast.SetStatus(False)
                            break # revisar si este break es necesario
                        else:
                            while self.radio.any():
                                rxBuff = self.radio.recv()
                            #rxBuff = self.radio.recv()
                            rxBuff = rxBuff.decode().split("^")
                            print("The Broadcast answered: {}".format(rxBuff[0]))
                            broadcast.SetStatus(True)
                                       
                    self.radio.stop_listening()
                    frame = broadcast.address + "^" + "A^"
                    try:
                        print("Sending " + frame)
                        self.radio.send(frame.encode())
                    except OSError:
                        pass

                    self.radio.start_listening()
                    start_time = utime.ticks_ms()
                    timeout = False
                    while not self.radio.any() and not timeout:
                        if utime.ticks_diff(utime.ticks_ms(), start_time) > timeoutLimit:
                            timeout = True
                    if timeout:
                        print("\nCan not connect with Broadcast {} please check and restart device".format(broadcast.address))
                        broadcast.SetStatus(False)
                    else:
                        while self.radio.any():
                            rxBuff = self.radio.recv()
                        rxBuff = rxBuff.decode().split()
                        print("The Broadcast answered: {}".format(rxBuff[0]))
                        broadcast.SetStatus(True)                    
                else:
                    self.radio.stop_listening()
                    print("There are no EndPoints in Broadcast with address {}".format(broadcast.address))
            return "ok"
        else:
            print("\nThere are no Broadcast")
            return "error"

    def SendCommandBroadcast(self, command) -> str:
        if not command in self.commands2Broadcast.values():
            print("\nIncorrect command")
            return "error"
            
        if len(self.routingTableBroadcast):
            for broadcast in self.routingTableBroadcast:
                print("===========================")
                print(broadcast)
                print("---------------------------")
                
                self.radio.stop_listening()
                self.radio.open_tx_pipe(self.address.encode())
                self.radio.open_rx_pipe(1, broadcast.address.encode())
                self.radio.start_listening()
                utime.sleep_ms(1)
                self.radio.stop_listening()
                
                if len(broadcast.routingTableEndPoint):
                    self.radio.stop_listening()
                    frame = broadcast.address +"^"+ str(command) + "^"
                    
                    try:
                        print("Sending " + frame)
                        self.radio.send(frame.encode())
                    except OSError:
                        pass

                    self.radio.start_listening()
                    start_time = utime.ticks_ms()
                    timeout = False
                    while not self.radio.any() and not timeout:
                        if utime.ticks_diff(utime.ticks_ms(), start_time) > timeoutLimit:
                            timeout = True
                    if timeout:
                        print("\nCan not connect with Broadcast {} please check the device".format(broadcast.address))
                        broadcast.SetStatus(False)
                    else:
                        while self.radio.any():
                            rxBuff = self.radio.recv()
                        rxBuff = rxBuff.decode().split("^")
                        print("The Broadcast {} answered: {}".format(broadcast.address ,rxBuff[0]))
                        broadcast.SetStatus(True)

                    if command == self.commands2Broadcast["read EndPoints"]:
                        for endPoint in broadcast.routingTableEndPoint:
                            frame = endPoint.address + "^"
                            self.radio.stop_listening()
                            
                            try:
                                print("Sending " + frame)
                                self.radio.send(frame.encode())
                            except OSError:
                                pass
                            
                            self.radio.start_listening()
                            start_time = utime.ticks_ms()
                            timeout = False
                            while not self.radio.any() and not timeout:
                                if utime.ticks_diff(utime.ticks_ms(), start_time) > timeoutLimit:
                                    timeout = True
                            if timeout:
                                print("\nCan not connect with Broadcast {} please check the device".format(broadcast.address))
                                broadcast.SetStatus(False)
                            else:
                                while self.radio.any():
                                    rxBuff = self.radio.recv()
                                rxBuff2 = rxBuff.decode().split("^")
                                if rxBuff2[0] == "m":
                                    if rxBuff2[1] == "NotFound":
                                        print("The Endpoint {} is not registered in the Broadcast".format(endPoint.address))
                                    else:
                                        endPoint.ReadFrame(rxBuff[2:])
                        
                        frame = "end^"
                        self.radio.stop_listening()
                        
                        try:
                            print("Sending " + frame)
                            self.radio.send(frame.encode())
                        except OSError:
                            pass

                else:
                    self.radio.stop_listening()
                    print("There are no EndPoints in Broadcast with address {}".format(broadcast.address))

            return "ok"

        else:
            print("\nThere are no Broadcast")
            return "error"

    def CheckDevices2Print(self) -> list:

        toPrint = []

        if len(self.routingTableEndPoint) : 
            for endPoint in self.routingTableEndPoint:
                if endPoint.alarm : 
                    toPrint.append(dict(name = endPoint.name, status = "Alarma"))
                if endPoint.status == False:
                    toPrint.append(dict(name = endPoint.name, status = "No com"))

        if len(self.routingTableBroadcast):
            for broadcast in self.routingTableBroadcast:
                if broadcast.status == False:
                    toPrint.append(dict(name = broadcast.address, status = "No com")) 
                else: 
                    if len(broadcast.routingTableEndPoint):
                        for endPoint in broadcast.routingTableEndPoint:
                            if endPoint.alarm : 
                                toPrint.append(dict(name = endPoint.name, status = "Alarma"))
                            if endPoint.status == False:
                                toPrint.append(dict(name = endPoint.name, status = "No com"))

        return toPrint

    def UserInterface(self, button = ""):
        toPrint = self.CheckDevices2Print()

        if len(toPrint) > 0:
            pages = int(len(toPrint)/3)+1
        else:
            pages = 0
        
        if toPrint:
            if button == "up":
                self.rowOnLCD += 1
            elif button == "down":
                self.rowOnLCD -= 1
            
            if self.rowOnLCD <= 0:
                self.rowOnLCD = 0 
            if self.rowOnLCD >= pages:
                self.rowOnLCD = pages - 1

            row = 0
            toLCD = []
            for event in toPrint:
                text = str(row + 1) + " " + event["name"] + ": " + event["status"]
                text = text + " "*(20 - len(text))
                toLCD.append(text)
                row += 1

            row = 0
            for i in range(self.rowOnLCD*3, (self.rowOnLCD*3) + 3, 1):
                if i < len(toLCD):
                    self.lcd.Print(toLCD[i], 0, row)
                else:
                    self.lcd.Print(" "*20, 0, row)
                row += 1
        
            self.lcd.Print("Bajar off Subir alrm", 0, 3)
        else: 
            self.lcd.DefaultMessage()
            self.rowOnLCD = 0

        if button == "left":
            self.lcd.Clear()
            self.lcd.Print("Encendiendo alarmas", 0, 0)
            self.StartAlarmsEndPoints()
            #self.StartAlarm()
            self.SendCommandBroadcast(commands2Broadcast["start alarms EndPoints"])
            self.lcd.Clear()
            self.lcd.Print("Todas las", 0, 0)
            self.lcd.Print("alarmas", 0, 1)
            self.lcd.Print("encendidas", 0, 2)
            utime.sleep(2)
            self.lcd.Clear()

        if button == "rigth":
            self.rowOnLCD = 0
            self.lcd.Clear()
            self.lcd.Print("apagando alarmas", 0, 0)
            #self.ClearAlarm()
            self.ClearDetectionsEndPoints()
            self.SendCommandBroadcast(self.commands2Broadcast["clear EndPoints"])
            self.lcd.Clear()
            self.lcd.Print("Todas las", 0, 0)
            self.lcd.Print("alarmas", 0, 1)
            self.lcd.Print("apagadas", 0, 2)
            utime.sleep(2)
            self.lcd.Clear()
            self.lcd.DefaultMessage()

    def __str__(self):
        return "Master in '{}' addres".format(self.address)
#endregion