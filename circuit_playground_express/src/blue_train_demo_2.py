import time
import board
import neopixel
import uheapq

PIXELS = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=True)
BLUE = (0, 0, 100)
BLACK = (0, 0, 0)
EVENT_QUEUE = []
DIRECTION = 1

head, tail = 0, 5


def move_blue_train():
    global head, tail
    if head == 0:
        print(f'move = {time.monotonic()}')
    PIXELS[head] = BLUE
    PIXELS[tail] = BLACK
    head = (head + DIRECTION) % 10
    tail = (tail + DIRECTION) % 10
    uheapq.heappush(EVENT_QUEUE, (time.monotonic() + 0.1, move_blue_train))


uheapq.heappush(EVENT_QUEUE, (time.monotonic() + 1, move_blue_train))

while EVENT_QUEUE:
    t, fn = uheapq.heappop(EVENT_QUEUE)
    time.sleep(t - time.monotonic())
    fn()
