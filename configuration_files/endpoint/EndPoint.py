#region identification
# Perimetral EndPoint module
# Authors: 
#    Jony Carmona
#    Jhojan Poveda
#    Alejandro Beltrán 
#endregion

#region imports
from BasePerimetral import BasePerimetralClass, rxPollDelay, slaveSendDelay, esp32AlarmPin, esp32DetectionPin, esp32CCDetectionPin
from machine import Pin, Timer
import utime
#endregion 

#region EndPoint Class
class EndPoint(BasePerimetralClass):
    def __init__(self, address = "zn000", master_address = "mastr", on_High_alarm=60, enable_timer_alarm = False) -> None:
        super().__init__(address, master_address = master_address)
        self.detection=False
        self.alarm=False
        self.batteryLevel=0
        self.onHighAlarm=on_High_alarm
        self.enableTimerAlarm = enable_timer_alarm
        self.timer0 = Timer(0)
        self.source=True
        self.monitoring=False
        #Gpio's
        self.alarmPin = Pin(esp32AlarmPin, mode = Pin.OUT, value = 0)
        self.detectionPin = Pin(esp32DetectionPin, mode = Pin.IN, pull = None)
        self.CCDetectionPin = Pin(esp32CCDetectionPin, mode = Pin.IN, pull = None)
        
    def StartMonitoring(self):
        self.detectionPin.irq(trigger=Pin.IRQ_FALLING, handler=self.MonitoringDetection)
        self.CCDetectionPin.irq(trigger=Pin.IRQ_FALLING, handler=self.MonitoringCloseCircuit)
        self.monitoring=True
        print("The system is monitoring")
        return "ok"

    def StopMonitoring(self):
        self.detectionPin.irq(trigger=Pin.IRQ_FALLING, handler=None)
        self.CCDetectionPin.irq(trigger=Pin.IRQ_FALLING, handler=None)
        self.monitoring=False
        print("The monitoring was stopped")
        return "ok"

    def MonitoringDetection(self, p):
        self.SetDetection()
        self.StartAlarm()
        if self.enableTimerAlarm:
            self.timer0.init(mode=Timer.ONE_SHOT, period=self.onHighAlarm*1000, callback=self.ClearAlarm)
        print ("Detection on " + self.address)
        return "ok"

    def MonitoringCloseCircuit(self, p):
        self.SetDetection()
        self.StartAlarm()
        if self.enableTimerAlarm:
            self.timer0.init(mode=Timer.ONE_SHOT, period=self.onHighAlarm*1000, callback=self.ClearAlarm)
        print ("Close circuit on " + self.address)
        return "ok"
    
    def ClearAlarm(self, t=0):
        self.alarmPin.off()
        self.alarm = False
        print("The alarm was cleared")
        return "ok"

    def StartAlarm(self):
        self.alarmPin.on()
        self.alarm = True
        print("The alarm was set")
        return "ok"
    
    def ClearDetection(self):
        self.detection = False
        print("The detection was cleared")
        return "ok"
    
    def SetDetection(self):
        self.detection = True
        print("The detection was set")
        return "ok"
    
    def Listen(self):
        self.radio.open_tx_pipe(self.address.encode())
        self.radio.open_rx_pipe(1, self.masterAddress.encode())
        self.radio.start_listening()
        print("Waiting for incoming package from master on " + self.masterAddress)

        while True:
            if self.radio.any():
                while self.radio.any():
                    rxBuff = self.radio.recv()
                    
                # Give master time to get into receive mode.
                utime.sleep_ms(slaveSendDelay)
                self.radio.stop_listening()
                
                if self.ReadFrame(rxBuff) == "ok":
                    try:
                        txBuff = self.BuildFrame()
                        self.radio.send(txBuff)
                    except OSError:
                        pass
                    
                    print("The response was sent")
                
                utime.sleep_ms(rxPollDelay)
                self.radio.start_listening()

    def EnableTimerAlarm (self):
        self.enableTimerAlarm = True
        return "ok"

    def DisableTimerAlarm (self):
        self.enableTimerAlarm = False
        return "ok"

    def SetOnHighAlarm(self, value_time):
        self.onHighAlarm = value_time
        print("The time on high alarm was set in " + str(value_time) + " seconds")
        return "ok"

    def BuildFrame(self):
        frame = self.address + "^A:" + str(int(self.detection)) + "^B:" + str(int(self.alarm)) + "^C:0" + "^D:" + str(int(self.source)) + "^E:" + (str(int(self.monitoring))) + "^"
        print(frame)
        return frame.encode()

    def ReadFrame(self, masterFrame):
        masterFrame = masterFrame.decode()
        masterFrame = masterFrame.split("^")
        print("Read Frame:" )
        print(masterFrame)
        if masterFrame[0] == self.address:
            if masterFrame[1] == "A:1":
                self.StartMonitoring()
            else:
                self.StopMonitoring()
            if masterFrame[2] == "B:0":
                self.ClearDetection()
                self.ClearAlarm()
            if masterFrame[3] == "C:1":
                self.StartAlarm()
            return "ok"
        else:
            return "error"

    def __str__(self):
        return """      EndPoint in '{}' address
        Master address: {}
        Detection: {}
        Alarm: {}
        Battery level: {}
        Source: {}
        Status: {}
        """.format(self.address, self.masterAddress, self.detection, self.alarm, self.batteryLevel, 
        self.source, self.status)
#endregion