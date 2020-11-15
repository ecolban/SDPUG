def _sift_down(heap, i):
    n = len(heap)
    last_parent = (n - 2) // 2

    def child(j):
        left = 2 * j + 1
        right = left + 1
        return min((left, right), key=heap.__getitem__) if right < n else left

    c = child(i)
    while i <= last_parent and heap[i] > heap[c]:
        heap[c], heap[i] = heap[i], heap[c]
        i, c = c, child(c)


def _sift_up(heap, i):
    def parent(j):
        return (j - 1) // 2

    p = parent(i)
    while i > 0 and heap[p] > heap[i]:
        heap[p], heap[i] = heap[i], heap[p]
        i, p = p, parent(p)


def heapify(lst):
    """In place reordering of lst to satisfy heap ordering"""
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
