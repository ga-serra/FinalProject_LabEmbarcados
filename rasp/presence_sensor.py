from machine import Pin
import time

class Presence_Sensor:
    def __init__(self, pin_num):
        self.sensor = Pin(pin_num, Pin.IN)

    def detected(self):
        # returns True if detected presence
        return self.sensor.value == 1
    
    def scan_presence(self, activate, _time=1):
        while activate == True:
            if self.detected():
                print("Someone is in place")
            else:
                print("Nobody")
            time.sleep(_time)