import board
import digitalio
import time
import uheapq

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
SECOND = 1000000000
MILLISECOND = 1000000
EVENT_QUEUE = []


def blink_on(t):
    print(time.monotonic())
    led.value = True
    uheapq.heappush(EVENT_QUEUE, (t + 100 * MILLISECOND, blink_off))


def blink_off(t):
    led.value = False
    uheapq.heappush(EVENT_QUEUE, (t + 900 * MILLISECOND, blink_on))


uheapq.heappush(EVENT_QUEUE, (time.monotonic_ns(), blink_on))
while EVENT_QUEUE:
    # print('.', end='')
    t, fn = uheapq.heappop(EVENT_QUEUE)
    time.sleep((t - time.monotonic_ns()) / SECOND)
    fn(t)
