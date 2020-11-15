import time
import board
import neopixel
import uheapq

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=True)
BLUE = (0, 0, 100)
BLACK = (0, 0, 0)
SECOND = 1000000000
MILLISECOND = 1000000
EVENT_QUEUE = []

direction = 1
head, tail = 0, direction * 5


def move_blue_train(t):
    global head, tail, direction
    if head == 0:
        print(f'move = {time.monotonic()}')
    pixels[head] = BLUE
    pixels[tail] = BLACK
    head = (head + direction) % 10
    tail = (tail + direction) % 10
    uheapq.heappush(EVENT_QUEUE, (t + 100 * MILLISECOND, move_blue_train))


uheapq.heappush(EVENT_QUEUE, (time.monotonic_ns(), move_blue_train))
while EVENT_QUEUE:
    # print('.', end='')
    t, fn = uheapq.heappop(EVENT_QUEUE)
    time.sleep(max((t - time.monotonic_ns()) / SECOND, 0))
    fn(t)
