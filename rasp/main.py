from machine import Pin, UART
from utime import sleep
from servo import Servo
import time
from dht import DHT11, InvalidCheckSum
from PicoDHT22 import PicoDHT22

led_pin = Pin(13, Pin.OUT)
led_pin.on()
dht_pin = Pin(4, Pin.OUT, Pin.PULL_DOWN)

serial = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))
servo = Servo(8)
dht_sensor = DHT11(dht_pin)
#dht_sensor=PicoDHT22(Pin(4,Pin.IN,Pin.PULL_UP),dht11=True)
servo.step_to_angle(90)

while True:
    if serial.any():
        request = serial.read().decode('utf-8')
        command = request.splitlines()[1]
        print(command)

    # if serial.any():
    #     msg = serial.read().decode('utf-8')
    #     print(msg)
    #
    #     if msg == "report\r\n":
    #         try:
    #             temp, hum = dht_sensor.measure()
    #             serial.write("Temperature: ")
    #             serial.write(str(temp))
    #             serial.write(" C\r\n")
    #             serial.write("Humidity: ")
    #             serial.write(str(hum))
    #             serial.write(" %\r\n")
    #         except Exception as e:
    #             serial.write(f"Error reading ambient data: {e}\r\n")


    # time.sleep(1)
    # servo.step_to_angle(90)
    # time.sleep(1)
    # servo.step_to_angle(0)
    # time.sleep(1)

# The program should never reach here
led_pin.off()
print("Finished.")
