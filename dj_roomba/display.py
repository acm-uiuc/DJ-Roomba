#!/usr/bin/python
"""
Based on http://www.raspberrypi-spy.co.uk

 The wiring for the LCD is as follows:
 1 : GND
 2 : 5V
 3 : Contrast (0-5V)*
 4 : RS (Register Select)
 5 : R/W (Read Write)       - GROUND THIS PIN
 6 : Enable or Strobe
 7 : Data Bit 0             - NOT USED
 8 : Data Bit 1             - NOT USED
 9 : Data Bit 2             - NOT USED
 10: Data Bit 3             - NOT USED
 11: Data Bit 4
 12: Data Bit 5
 13: Data Bit 6
 14: Data Bit 7
 15: LCD Backlight +5V**
 16: LCD Backlight GND
"""

import time
# pylint: disable=E0611, F0401
import RPi.GPIO as GPIO

# Define GPIO to LCD mapping
LCD_PINS = {'RS': 7, 'E': 8, 'D4': 25, 'D5': 24, 'D6': 23, 'D7': 18}
LCD_DATA_PINS = [LCD_PINS['D4'], LCD_PINS['D5'], LCD_PINS['D6'], LCD_PINS['D7']]

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

HIGH_MASKS = [0x10, 0x20, 0x40, 0x80]
LOW_MASKS = [0x01, 0x02, 0x04, 0x08]

def set_bits(bits, masks):
    """Sets bits for display matrix, sends as 2 nibbles"""
    for lcd_pin in LCD_DATA_PINS:
        GPIO.output(lcd_pin, False)
    for mask, lcd_pin in zip(masks, LCD_DATA_PINS):
        if bits & mask == mask:
            GPIO.output(lcd_pin, True)

def lcd_byte(bits, mode):
    """Send byte to data pins
    bits = data
    mode = True  for character
            False for command"""
    GPIO.output(LCD_PINS['RS'], mode) # RS
    for masks in [HIGH_MASKS, LOW_MASKS]:
        set_bits(bits, masks=masks)
        toggle_enable_pin()

def display_line(msg, lcd_line):
    """Displays the msg on the specified lcd line"""
    lcd_byte(lcd_line, LCD_CMD)
    lcd_string(msg)
    time.sleep(3) # 3 second delay

def lcd_string(message):
    """Send string to display"""
    for char in message.ljust(LCD_WIDTH," ")[:LCD_WIDTH]:
        lcd_byte(ord(char), LCD_CHR)

def toggle_enable_pin(lcd_e=LCD_PINS['E'], e_delay=E_DELAY, e_pulse=E_PULSE):
    """Toggles enable pin"""
    time.sleep(e_delay)
    GPIO.output(lcd_e, True)
    time.sleep(e_pulse)
    GPIO.output(lcd_e, False)
    time.sleep(e_delay)

def display(msg) -> None:
    """displays msg on the lcd"""
    lines = msg.splitlines()
    for _lines in zip(lines[::2], lines[1::2]):
        for lcd_line, line in zip([LCD_LINE_1, LCD_LINE_2], _lines):
            display_line(line, lcd_line)

def init_display():
    """inits lcd display"""
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    for pin in LCD_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
    for byte in [0x33, 0x32, 0x28, 0x0C, 0x06, 0x01]:
        lcd_byte(byte, LCD_CMD)

if __name__ == '__main__':
    init_display()
    display("Marcell V.C\nFTW!!!!!!\nOMG\nOMG")
