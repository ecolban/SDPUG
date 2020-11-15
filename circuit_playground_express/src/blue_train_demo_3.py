import time
import board
import neopixel
import uheapq

PIXELS = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=True)
BLUE = (0, 0, 100)
BLACK = (0, 0, 0)
NANOSECOND = 1
MICROSECOND = 1000 * NANOSECOND
MILLISECOND = 1000 * MICROSECOND
SECOND = 1000 * MILLISECOND
EVENT_QUEUE = []
DIRECTION = 1

head, tail = 0, DIRECTION * (-4) % 10


def move_blue_train(t):
    global head, tail
    if head == 0:
        print(f'move = {time.monotonic()}')
    PIXELS[head] = BLUE
    PIXELS[tail] = BLACK
    head = (head + DIRECTION) % 10
    tail = (tail + DIRECTION) % 10
    uheapq.heappush(EVENT_QUEUE, (t + 100 * MILLISECOND, move_blue_train))


uheapq.heappush(EVENT_QUEUE, (time.monotonic_ns(), move_blue_train))
while EVENT_QUEUE:
    t, fn = uheapq.heappop(EVENT_QUEUE)
    time.sleep(max((t - time.monotonic_ns()) / SECOND, 0))
    fn(t)
