from machine import Pin, UART
from utime import sleep
from servo import Servo
import time
from dht import DHT11, InvalidCheckSum
from PicoDHT22 import PicoDHT22

dht_pin = Pin(4, Pin.OUT, Pin.PULL_DOWN)
dht_sensor = DHT11(dht_pin)

serial = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))

led_pins = {
    'house_red': Pin(0, Pin.OUT),
    'house_green': Pin(1, Pin.OUT),
    'house_blue': Pin(2, Pin.OUT),
    'house_white': Pin(3, Pin.OUT),
    'bath': Pin(18, Pin.OUT),
}

door_front = Servo(8)
door_bath = Servo(9)

fan = Pin(19, Pin.OUT)

def control_house(leds_state, door_state):
    for led, pin in led_pins.items():
        pin.value(leds_state[led])

    if (door_state[0] == 'open'):
        door_front.step_to_angle(175)
    else:
        door_front.step_to_angle(5)

    if (door_state[1] == 'open'):
        door_bath.step_to_angle(0)
    else:
        door_bath.step_to_angle(155)

def main():
    leds_state = {
        'house_blue': False,
        'house_red': False,
        'house_green': False,
        'house_white': False,
        'bath': False,
    }

    doors_state = ('closed', 'closed')

    while True:
        if serial.any():
            request = serial.read().decode('utf-8')
            command = request.splitlines()[1]
            print(command)

            if(command == "/env"):
                temp = 21
                hum = 60
                lum = 0.32

                serial.write(str(temp))
                serial.write(",")
                serial.write(str(hum))
                serial.write(",")
                serial.write(str(lum))
                serial.write("\r\n")

        control_house(leds_state, doors_state)


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

main()

# The program should never reach here
print("Finished.")
