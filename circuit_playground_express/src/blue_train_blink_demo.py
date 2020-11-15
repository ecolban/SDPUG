import time
import board
import digitalio
import neopixel
import uheapq

BLUE = (0, 0, 100)
BLACK = (0, 0, 0)
DIRECTION = -1
NANOSECOND = 1
MICROSECOND = 1000 * NANOSECOND
MILLISECOND = 1000 * MICROSECOND
SECOND = 1000 * MILLISECOND
EVENT_QUEUE = []

PIXELS = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=True)
RED_LED = digitalio.DigitalInOut(board.D13)
RED_LED.direction = digitalio.Direction.OUTPUT

head, tail = 0, DIRECTION * (-4)


def move_train(t):
    global head, tail
    if head == 0:
        print(f'move = {time.monotonic():.2f}')
    PIXELS[head] = BLUE
    PIXELS[tail] = BLACK
    head = (head + DIRECTION) % 10
    tail = (tail + DIRECTION) % 10
    uheapq.heappush(EVENT_QUEUE, (t + 100 * MILLISECOND, move_train))


def blink_on(t):
    print(f'blink_on: {time.monotonic():.2f}')
    RED_LED.value = True
    uheapq.heappush(EVENT_QUEUE, (t + 100 * MILLISECOND, blink_off))


def blink_off(t):
    RED_LED.value = False
    uheapq.heappush(EVENT_QUEUE, (t + 900 * MILLISECOND, blink_on))


start = time.monotonic_ns()
uheapq.heappush(EVENT_QUEUE, (start + SECOND, move_train))
uheapq.heappush(EVENT_QUEUE, (start + SECOND + 1, blink_on))

while EVENT_QUEUE:
    t, fn = uheapq.heappop(EVENT_QUEUE)
    time.sleep(max((t - time.monotonic_ns()) / SECOND, 0))
    fn(t)
