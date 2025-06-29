import datetime
import time
from OLED import Display
from buzzer import Buzzer
from servo import Servo

def movie_mode(image_path):
    ## Criar parte das luzes
    display = Display()
    display.show_message(text='Welcome')
    display.display_image(image_path)

def disco_mode(music_notes):
    ## Criar LEDs 
    buzzer = Buzzer()
    buzzer.play_song(music_notes)

def wake_up_mode(hour,minute,music_notes):
    buzzer = Buzzer()
    now = datetime.datetime.now()
    if now.hour == hour and now.minute == minute:
        buzzer.play_song(music_notes)
        ## LEDs acendem

def house_close(password, servo_room_port, servo_bath_port, flag_house_close):
    key = 1234
    servo_room = Servo(servo_room_port)
    servo_bath = Servo(servo_bath_port)
    if password != key:
        ## apagar luzes
        servo_room.step_to_angle(0)
        servo_bath.step_to_angle(0)
        flag_house_close = 1
    elif password == key:
        ## acender luzes
        servo_room.step_to_angle(180)
        servo_bath.step_to_angle(180)
        flag_house_close = 0
    return flag_house_close

