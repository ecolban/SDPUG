def _sift_down(heap, i):
    n = len(heap)
    last_parent = (n - 2) // 2

    def next_child():
        left = 2 * i + 1
        right = left + 1
        if right < n:
            return left if heap[left] < heap[right] else right
        else:
            return left

    child = next_child()
    while i <= last_parent and heap[i] > heap[child]:
        heap[child], heap[i] = heap[i], heap[child]
        i = child
        child = next_child()


def _sift_up(heap, i):
    def next_parent():
        return (i - 1) // 2

    parent = next_parent()
    while i > 0 and heap[parent] > heap[i]:
        heap[parent], heap[i] = heap[i], heap[parent]
        i = parent
        parent = next_parent()


def heapify(lst):
    """In place reordering lst to satisfy heap ordering"""
    n = len(lst)
    if n < 2: return
    for j in reversed(range(n // 2)):
        _sift_down(lst, j)


def heappush(heap, element):
    n = len(heap)
    heap.append(element)
    _sift_up(heap, n)


def heappop(heap):
    """Raises an IndexError if the heap is empty."""
    if len(heap) <= 1:
        return heap.pop()
    x = heap.pop()
    res, heap[0] = heap[0], x
    _sift_down(heap, 0)
    return res
