import heapq


def get_kth_element(arr: list, k: int) -> int:
    heapq.heapify(arr)        
    for _ in range(k):
        heapq.heappop(arr)
    return arr[0]
