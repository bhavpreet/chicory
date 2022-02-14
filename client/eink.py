#!/usr/bin/env python3
from machine import SPI
from machine import Pin
import epaper2in13b

class eink:
    def __init__(self):
        # SPI3 on Black STM32F407VET6
        # spi = SPI(2, baudrate=2000000, polarity=0, phase=0)
        hspi = SPI(1, 10000000, sck=Pin(13), mosi=Pin(14), miso=Pin(12))

        cs = Pin(15)
        dc = Pin(27)
        rst = Pin(26)
        busy = Pin(25)

        self.e = epaper2in13b.EPD(hspi, cs, dc, rst, busy)
        self.e.init()

    def display(self, b_image, r_image):
        self.e.display_frame(b_image, r_image)
   
