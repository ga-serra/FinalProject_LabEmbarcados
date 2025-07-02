from machine import Pin, UART
from utime import sleep
from servo import Servo
import time
from dht import DHT11, InvalidCheckSum
from PicoDHT22 import PicoDHT22
from OLED import Display
from buzzer import Buzzer
from photoresistor import photoresistor

flag_automatic_mode = 0

buzzer_port = 5
buzzer = Buzzer(buzzer_port)

dht_pin = Pin(4, Pin.OUT, Pin.PULL_DOWN)
dht_sensor = DHT11(dht_pin)

oled_SDA = 7
oled_SCL = 22
oled = Display(oled_SCL,oled_SDA)

lum_pin = 66
lum = photoresistor(lum_pin)

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
        if flag_automatic_mode == 1:
            temp, hum = dht_sensor.measure()
            lum.read_sensor()
            if lum <= 0.5:
                for led, _ in leds_state:
                    leds_state[led] = True
            else:
                for led, _ in leds_state:
                    leds_state[led] = False
            if temp >= 30:
                fan.value(1)
            else:
                fan.value(0)

        if serial.any():
            request = serial.read().decode('utf-8')
            command = request.splitlines()[1]
            print(command)
            if(command == "/env"):
                temp, hum = dht_sensor.measure()
                lum.read_sensor()

                serial.write(str(temp))
                serial.write(",")
                serial.write(str(hum))
                serial.write(",")
                serial.write(str(lum))
                serial.write("\r\n")
            
            if(command == "/front-door/0"):
                doors_state[0] = 'close'
                control_house(leds_state, doors_state)
            
            if(command == "/front-door/1"):
                doors_state[0] = 'open'
                control_house(leds_state, doors_state)
            
            if(command == "/bath-door/0"):
                doors_state[1] == 'close'
                control_house(leds_state, doors_state)

            if(command == "/bath-door/1"):
                doors_state[1] == 'open'
                control_house(leds_state, doors_state)

            if(command == '/fan/0'):
                fan.value(0)
            
            if(command == '/fan/1'):
                fan.value(1)
            
            if(command == '/bedroom-light/0'):
                leds_state['house_white'] = False
                leds_state['house_green'] = False
                leds_state['house_red'] = False
                leds_state['house_blue'] = False
                control_house(leds_state, doors_state)
            
            if(command == '/bedroom-light/1'):
                leds_state['house_white'] = True
                leds_state['house_green'] = True
                leds_state['house_red'] = True
                leds_state['house_blue'] = True
                control_house(leds_state, doors_state)

            if(command == '/red-light/0'):
                leds_state['house_red'] = False
                leds_state['house_green'] = False
                leds_state['house_blue'] = False 

            if(command == '/red-light/1'):
                leds_state['house_green'] = False
                leds_state['house_red'] = True
                leds_state['house_blue'] = False 

            if(command == '/green-light/0'):
                leds_state['house_red'] = False
                leds_state['house_green'] = False
                leds_state['house_blue'] = False 

            if(command == '/green-light/1'):
                leds_state['house_green'] = True
                leds_state['house_red'] = False
                leds_state['house_blue'] = False   

            if(command == '/blue-light/0'):
                leds_state['house_red'] = False
                leds_state['house_green'] = False
                leds_state['house_blue'] = False 

            if(command == '/blue-light/1'):
                leds_state['house_green'] = False
                leds_state['house_red'] = False
                leds_state['house_blue'] = True

            if(command == '/bath-light/0'):
                leds_state['bath'] = False
                control_house(leds_state, doors_state)
            
            if(command == '/bath-light/1'):
                leds_state['bath'] = True
                control_house(leds_state, doors_state)
            
            if(command == '/tv/0'):
                oled.power_off()
            
            if(command == '/tv/1'):
                oled.show_message('Welcome')
                time.sleep(3)
                oled.display_image("palmeiras.bmp")
            
            if(command == '/mode/movie'):
                for led, state in leds_state:
                    leds_state[led] = False
                doors_state = ('close', 'close')
                control_house(leds_state, doors_state)
                oled.display_image("palmeiras.bmp")

            if(command == '/mode/wakeup'):
                leds_state['house_white'] = True
                leds_state['house_green'] = True
                leds_state['house_red'] = True
                leds_state['house_blue'] = True
                control_house(leds_state, doors_state)
                song = [('C4', 0.3), ('C4', 0.3), ('D4', 0.3), ('C4', 0.3), ('F4', 0.3), ('E4', 0.6),
                        ('C4', 0.3), ('C4', 0.3), ('D4', 0.3), ('C4', 0.3), ('G4', 0.3), ('F4', 0.6),
                        ('C4', 0.3), ('C4', 0.3), ('C5', 0.3), ('A4', 0.3), ('F4', 0.3), ('E4', 0.3), ('D4', 0.3),
                        ('A#4', 0.3), ('A#4', 0.3), ('A4', 0.3), ('F4', 0.3), ('G4', 0.3), ('F4', 0.6)]
                buzzer.play_song(song)

            if(command == '/mode/empty'):
                for led, state in leds_state:
                    leds_state[led] = False
                oled.power_off()
                doors_state = ('close', 'close')
                fan.value(0)

            if(command == '/mode/automatic'):
                flag_automatic_mode = 1
            
            if(command == '/mode/manual'):
                flag_automatic_mode = 0

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
