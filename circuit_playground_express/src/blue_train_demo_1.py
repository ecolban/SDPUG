import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=True)
BLUE = (0, 0, 100)
BLACK = (0, 0, 0)
direction = -1
head, tail = 0, direction * (-4) % 10

while True:
    pixels[head] = BLUE
    pixels[tail] = BLACK
    head = (head + direction) % 10
    tail = (tail + direction) % 10
    time.sleep(1.0)
