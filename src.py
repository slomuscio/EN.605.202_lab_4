def shell_sort(data, gap_values):
    n = len(data)
    for gap in gap_values: 

        for i in range(gap, n):
            temp = data[i]  # second item in gap sequence 

            j = i 
            while j >= gap and data[j - gap] > temp:
                data[j] = data[j - gap]
                j -= gap 
            
            data[j] = temp
    print(data)


def heapify(heap, heap_size, idx):
    while True: 
        maximum = idx  # Root index. 
        left = 2 * idx + 1  # Left child index. 
        right = 2 * idx + 2  # Right child index.

        if left < heap_size and heap[left] > heap[idx]:
            maximum = left 
        
        if right < heap_size and heap[right] > heap[idx]:
            maximum = right 

        if maximum != idx:  # If largest value is not the root...
            heap[idx], heap[maximum] = heap[maximum], heap[idx]  # Swap root with max value 
        else: 
            break 
    # return heap 


def build_min_heap(data):
    start = len(data)//2 - 1

    for i in range(start, -1, -1):
        heap = heapify(data, len(data), i)

    return heap


def heap_sort(data):
    # heap = heapify(data, len(data), 0)  # make max heap from data
    heap = build_min_heap(data)

    n = len(heap)  # Number of items in heap. 
    for i in range(n-1, -1, -1):
        # Swap heap root (max value) with last value in heap. 
        heap[i], heap[0] = heap[0], heap[i]
        # Heapify all elements except the root that was just swapped to the end. 
        heapify(heap, i, 0)
    return heap 


if __name__=="__main__":
    # shell_sort([6,2,3,7,8,4,9,1,10,4,3,5], [3, 1])

    data = [6,2,3,7,8,4,9,1,10,4,3,5]

    heapify(data, len(data), len(data)//2-1)
    print(data)
    # heap = heap_sort(data)
    # print(heap)
