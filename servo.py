from machine import Pin, PWM
import time

class Servo:
    def __init__(self, pin_num:int, freq:int = 50):
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(freq)
        self.current_angle = 0

    def step_to_angle(self, angle,delay=0.01, step_size=1):
        # Angle has to be between 0º and 180º
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180

        step = step_size if angle > self.current_angle else -step_size

        for ang in range(self.current_angle, angle, step):
            self.write_angle(ang)
            time.sleep(delay)
        
        self.write_angle(angle)
        # self.current_angle = angle

    def write_angle(self, angle):
        # angle for time (pulse)
        min_time = 500                  # minimum pulse time
        max_time = 2500                 # maximum pulse time
        time_us = min_time + (angle/180) * (max_time - min_time)

        
        # Set duty cycle
        duty_cycle = int(time_us * 65535 / 20000)
        self.pwm.duty_u16(duty_cycle)        
