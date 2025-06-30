import datetime
import time
from machine import Pin, UART
from OLED import Display
from buzzer import Buzzer
from servo import Servo

def movie_mode(image_path, white_port, red_port, green_port, blue_port):
    ## Criar parte das luzes
    led_white = Pin(white_port, Pin.OUT)
    led_white.value(0)  
    led_red = Pin(red_port, Pin.OUT)
    led_red.value(0)      
    led_green = Pin(green_port, Pin.OUT)
    led_green.value(0)      
    blue_red = Pin(blue_port, Pin.OUT)
    blue_red.value(0)      
    display = Display()
    display.show_message(text='Welcome')
    display.display_image(image_path)

def disco_mode(music_notes, red_port, green_port, blue_port):
    ## Criar LEDs 
    buzzer = Buzzer()
    buzzer.play_song(music_notes)

def wake_up_mode(hour,minute,music_notes,white_port):
    buzzer = Buzzer()
    now = datetime.datetime.now()
    if now.hour == hour and now.minute == minute:
        buzzer.play_song(music_notes)
        led_white = Pin(white_port, Pin.OUT)
        led_white.value(1)  

def house_close(password, servo_room_port, servo_bath_port, flag_house_close, white_port, red_port, green_port, blue_port):
    key = 1234
    servo_room = Servo(servo_room_port)
    servo_bath = Servo(servo_bath_port)
    if password != key:
        led_white = Pin(white_port, Pin.OUT)
        led_white.value(0)  
        led_red = Pin(red_port, Pin.OUT)
        led_red.value(0)      
        led_green = Pin(green_port, Pin.OUT)
        led_green.value(0)      
        blue_red = Pin(blue_port, Pin.OUT)
        blue_red.value(0) 
        servo_room.step_to_angle(0)
        servo_bath.step_to_angle(0)
        flag_house_close = 1
    elif password == key:
        led_white = Pin(white_port, Pin.OUT)
        led_white.value(1)  
        led_red = Pin(red_port, Pin.OUT)
        led_red.value(0)      
        led_green = Pin(green_port, Pin.OUT)
        led_green.value(0)      
        blue_red = Pin(blue_port, Pin.OUT)
        blue_red.value(0) 
        servo_room.step_to_angle(180)
        servo_bath.step_to_angle(180)
        flag_house_close = 0
    return flag_house_close

