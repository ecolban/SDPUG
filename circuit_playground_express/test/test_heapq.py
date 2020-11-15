import os
import sys
from random import randrange

test_dir = os.path.dirname(__file__)
src_dir = os.path.join(test_dir, '..', 'src')
sys.path.append(src_dir)

from uheapq import heapify, heappush, heappop


def parent(i):
    return (i - 1) // 2


def assert_heap_ordered(heap):
    n = len(heap)
    for i in range(1, n):
        assert heap[parent(i)] <= heap[i]


def test_heapify():
    n = 1000
    a = [randrange(1000) for _ in range(n)]
    heapify(a)
    assert_heap_ordered(a)


def test_heappush():
    n = 1000
    a = []
    for i in range(n):
        heappush(a, randrange(1000))
    assert len(a) == n
    assert_heap_ordered(a)


def test_heappop():
    n = 1000
    a = [randrange(1000) for _ in range(n)]
    heapify(a)
    previous = heappop(a)
    pop_count = 1
    while a:
        assert previous <= (previous := heappop(a))
        pop_count += 1
    assert pop_count == n
    assert len(a) == 0
