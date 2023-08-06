from machine import Pin, I2C, SPI
from display import Write, GFX, SSD1306_I2C
from display import ST7735R as ST7735R_
from display.fonts import ubuntu_mono_15, ubuntu_mono_20


########################################################################
class GFX_:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, pixel):
        """Constructor"""

        self.gfx = GFX(size[0], size[1], pixel)
        self.fonts = {}

    # ----------------------------------------------------------------------
    def write(self, text, pos, font=ubuntu_mono_15):
        """"""

        if font.__name__ in self.fonts:
            self.fonts[font.__name__].text(text, *pos)
        else:
            self.fonts[font.__name__] = Write(self.oled, font)
            self.fonts[font.__name__].text(text, *pos)

    # ----------------------------------------------------------------------
    def __getattr__(self, attr):
        """"""

        if hasattr(self.oled, attr):
            return getattr(self.oled, attr)

        elif hasattr(self.gfx, attr):
            return getattr(self.gfx, attr)


########################################################################
class SSD1306(GFX_):

    # ----------------------------------------------------------------------
    def __init__(self, scl, sda, rst=16, size=(128, 64)):
        """"""

        i2c = I2C(scl=Pin(scl), sda=Pin(sda))
        Pin(rst, Pin.OUT, value=1)
        self.oled = SSD1306_I2C(size[0], size[1], i2c)

        super().__init__(self.oled.pixel)


########################################################################
class ST7735R(GFX_):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, dc, cs, rst, sclk, mosi, miso, size=(128, 128), offset=(0, 3)):
        """"""

        self.spi = SPI(2)
        self.spi.init(mosi=Pin(mosi), sck=Pin(sclk), miso=Pin(miso), baudrate=32000000)
        self.display = ST7735R(self.spi, dc=Pin(dc), cs=Pin(cs), rst=Pin(rst), width=size[0], height=size[1], ofx=offset[0], ofy=offset[1])

        super().__init__(self.display.pixel)

    # ----------------------------------------------------------------------
    def close(self):
        """"""

        self.spi.deinit()


