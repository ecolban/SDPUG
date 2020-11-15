import time
import board
import digitalio
import neopixel
import uheapq

# Constants
BLUE = (0, 0, 100)
BLACK = (0, 0, 0)
DIRECTION = 1
MICROSECOND = 1000 # nano seconds
MILLISECOND = 1000 * MICROSECOND
SECOND = 1000 * MILLISECOND
EVENT_QUEUE = []

# Outputs
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=True)
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Global state
head, tail = 0, 5


def move_train(t):
    global head, tail
    if head == 0:
        print(f'move = {time.monotonic():.2f}')
    pixels[head] = BLUE
    pixels[tail] = BLACK
    head = (head + DIRECTION) % 10
    tail = (tail + DIRECTION) % 10
    uheapq.heappush(EVENT_QUEUE, (t + 100 * MILLISECOND, move_train))


def blink_on(t):
    print(f'blink_on: {time.monotonic():.2f}')
    led.value = True
    uheapq.heappush(EVENT_QUEUE, (t + 100 * MILLISECOND, blink_off))


def blink_off(t):
    led.value = False
    uheapq.heappush(EVENT_QUEUE, (t + 900 * MILLISECOND, blink_on))


uheapq.heappush(EVENT_QUEUE, (time.monotonic_ns() + SECOND, move_train))
uheapq.heappush(EVENT_QUEUE, (time.monotonic_ns() + SECOND, blink_on))

while EVENT_QUEUE:
    t, fn = uheapq.heappop(EVENT_QUEUE)
    time.sleep(max((t - time.monotonic_ns()) / SECOND, 0))
    fn(t)
