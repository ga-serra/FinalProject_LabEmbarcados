import time
import board
import pwmio

class Buzzer:
    def __init__(self, pin=board.D5):
        self.buzzer = pwmio.PWMOut(pin, duty_cycle=0, frequency=440, variable_frequency=True)

    def play_tone(self, freq, duration):
        if freq == 0:  # Pausa
            self.buzzer.duty_cycle = 0
        else:
            self.buzzer.frequency = freq
            self.buzzer.duty_cycle = 65535 // 2  # 50% duty
        time.sleep(duration)
        self.buzzer.duty_cycle = 0  # Silencia ao final da nota

    def play_song(self, song):
        """
        song: lista de tuplas (nota, duração), ex:
        [('C4', 0.3), ('D4', 0.3), ('E4', 0.3)]
        """
        for note, dur in song:
            freq = self.NOTES.get(note.upper(), 0)
            self.play_tone(freq, dur)
            time.sleep(0.05)  # Pequena pausa entre notas
