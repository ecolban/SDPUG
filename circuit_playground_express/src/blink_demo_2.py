import board
import digitalio
import time
import uheapq

RED_LED = digitalio.DigitalInOut(board.D13)
RED_LED.direction = digitalio.Direction.OUTPUT
NANOSECOND = 1
MICROSECOND = 1000 * NANOSECOND
MILLISECOND = 1000 * MICROSECOND
SECOND = 1000 * MILLISECOND
EVENT_QUEUE = []


def blink_on(t):
    print(f'blink = {time.monotonic()}')
    RED_LED.value = True
    uheapq.heappush(EVENT_QUEUE, (t + 100 * MILLISECOND, blink_off))


def blink_off(t):
    RED_LED.value = False
    uheapq.heappush(EVENT_QUEUE, (t + 900 * MILLISECOND, blink_on))


uheapq.heappush(EVENT_QUEUE, (time.monotonic_ns(), blink_on))
while EVENT_QUEUE:
    t, fn = uheapq.heappop(EVENT_QUEUE)
    time.sleep(max((t - time.monotonic_ns()) / SECOND, 0))
    fn(t)
