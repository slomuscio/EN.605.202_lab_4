import time 
import numpy as np 
from typing import Tuple

def shell_sort(data:np.ndarray, gap_values:list) -> Tuple[np.ndarray, float]:
    """Performs shell sort on data using gap_values. 

    Args:
        data (np.ndarray): Input data to sort. 
        gap_values (list): Gap values to use in the shell sort. 

    Returns:
        Tuple[np.ndarray, float]: Sorted array, time taken in SECONDS to perform the sort. 
    """
    # Get number of items to sort. 
    n = len(data)
    
    # Start time for timing metrics. 
    start_time = time.time()

    # Shell sort logic. 
    for gap in gap_values:  # Iterate over gap values. 
        for i in range(gap, n):  # Iterate over items from gap value index through end of data. 
            temp = data[i] 
            j = i 
            while j >= gap and data[j - gap] > temp:  # Compare and sort. 
                data[j] = data[j - gap]
                j -= gap 
            data[j] = temp

    # End time for timing metrics. 
    end_time = time.time()
    elapsed_time_s = end_time - start_time
    return data, elapsed_time_s


def heapify(heap:np.ndarray, n:int, idx:int):
    """Makes input tree (that was a max heap before the root node was removed) back into a max heap. 

    Args:
        heap (np.ndarray): Input to make into a heap. 
        n (int): Number of items in the heap. 
        idx (int): Index of root. 
    """
    while True: 
        maximum = idx  # Root index. 
        left = 2 * idx + 1  # Left child index. 
        right = 2 * idx + 2  # Right child index.

        if left < n and heap[left] > heap[maximum]:  # Reset maximum to left node. 
            maximum = left 
        
        if right < n and heap[right] > heap[maximum]:  # Reset maximum to right node. 
            maximum = right 

        if maximum != idx:  # If largest value is not the root...
            heap[idx], heap[maximum] = heap[maximum], heap[idx]  # Swap root with max value 
            idx = maximum 
        else: 
            break 


def build_max_heap(data:np.ndarray) -> np.ndarray:
    """Builds a maximum heap from the input data array. 

    Args:
        data (np.ndarray): Input data to be made into a max heap and then sorted. 

    Returns:
        np.ndarray: Input array reorganized into a maximum heap. 
    """
    n = len(data) 
    start = n//2 - 1  # Root node location. 
    for i in range(start, -1, -1):  
        heapify(data, n, i)  # Build heap. 
    return data


def heap_sort(data:np.ndarray) -> Tuple[np.ndarray, float]:
    """Performs heap sort on data. 

    Args:
        data (np.ndarray): Input data to sort. 

    Returns:
        Tuple[np.ndarray, float]: Sorted array, time taken in SECONDS to perform the sort. 
    """
    # Start time for timing metrics. 
    start_time = time.time()

    # Build max heap from input data array. 
    heap = build_max_heap(data)

    # Number of items in heap. 
    n = len(data)  

    for i in range(n-1, -1, -1):
        # Swap heap root (max value) with last value in heap. 
        heap[i], heap[0] = heap[0], heap[i]
        # Heapify all elements except the root that was just swapped to the end. 
        heapify(heap, i, 0)
    
    # End time for timing metrics. 
    end_time = time.time()
    elapsed_time_s = end_time - start_time

    return heap, elapsed_time_s 
