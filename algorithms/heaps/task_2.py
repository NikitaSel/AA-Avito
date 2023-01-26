import heapq
from collections import namedtuple

HeapElement = namedtuple('HeapElement', 'min_elem, start_ind, ind')

def get_help_heap(arrs: list) -> list:
    h = []
    for i, arr in enumerate(arrs):
        if arr:
            heap_elem = HeapElement(arr[0], 0, i)
            h.append(heap_elem)
    heapq.heapify(h)
    return h

def merge_k_sorted(arrs: list) -> list:
    merged_list = []
    h = get_help_heap(arrs)
    while len(h) > 1:
        min_elem, start_ind, ind = h[0]
        merged_list.append(min_elem)
    
        start_ind = start_ind + 1
        if start_ind < len(arrs[ind]):
            min_elem = arrs[ind][start_ind]
            heap_elem = HeapElement(min_elem, start_ind, ind)   
            heapq.heapreplace(h, heap_elem)
        else:
            heapq.heappop(h)
    if h:
        _, start_ind, ind = h[0]
        merged_list += arrs[ind][start_ind:]
    return merged_list
