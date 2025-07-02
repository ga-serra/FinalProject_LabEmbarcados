import board
import busio
from PIL import Image
import adafruit_ssd1306

class Display:
    def __init__(self, SCL_pin, SDA_pin, width=128, height=64):
        # Inicializa a interface I2C
        self.i2c = busio.I2C(SCL_pin, SDA_pin)
        self.width = width
        self.height = height

        # Inicializa o display OLED
        self.oled = adafruit_ssd1306.SSD1306_I2C(width, height, self.i2c)

        self.clear()

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

    def display_image(self, image_path):
        from PIL import Image
        image = Image.open(image_path).convert("L")
        image = image.resize((self.width, self.height))
        image = image.point(lambda x: 0 if x < 128 else 255, '1')  # Binarização
        self.oled.image(image)
        self.oled.show()

    def show_message(self, text, font=None, x=0, y=0):
        from PIL import ImageDraw, ImageFont, Image
        image = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        if font is None:
            font = ImageFont.load_default()
        draw.text((x, y), text, font=font, fill=255)
        self.oled.image(image)
        self.oled.show()
    
    def power_off(self):
        """Desliga o display (manda apagar e não mostrar mais nada)."""
        self.oled.poweroff()
