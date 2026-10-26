import sys
import time
import tracemalloc
import random
import csv

# Aumentar límite de recursión para árboles profundos
sys.setrecursionlimit(200000)

# 1. Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

# 2. Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

# 3. Tree Sort
class Node:
    __slots__ = ['val', 'left', 'right']
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def tree_sort(arr):
    if not arr:
        return arr
    root = Node(arr[0])
    for val in arr[1:]:
        curr = root
        while True:
            if val < curr.val:
                if curr.left is None:
                    curr.left = Node(val)
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = Node(val)
                    break
                curr = curr.right
    
    res = []
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        res.append(curr.val)
        curr = curr.right
    return res

# 4. Heap Sort
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

# 5. Counting Sort Adaptado para Reales
def counting_sort_reals(arr, buckets=50000):
    if not arr:
        return arr
    min_v = min(arr)
    max_v = max(arr)
    range_v = max_v - min_v
    if range_v == 0:
        return arr
    
    b = [[] for _ in range(buckets)]
    for v in arr:
        idx = int((v - min_v) / range_v * (buckets - 1))
        b[idx].append(v)
    
    res = []
    for bucket in b:
        bucket.sort()
        res.extend(bucket)
    return res

def run_benchmark(sort_fn, data):
    tracemalloc.start()
    start_time = time.perf_counter()
    
    _ = sort_fn(data)
    
    elapsed_time = time.perf_counter() - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return elapsed_time, peak_memory / (1024 * 1024)

if __name__ == "__main__":
    sizes = [100000, 1000000, 10000000]
    
    with open('resultados_python.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritmo", "Tamaño", "Tiempo_s", "Memoria_MB"])
        
        for n in sizes:
            print(f"\nGenerando datos para N={n}...")
            original = [random.uniform(0.0, 1000000.0) for _ in range(n)]
            
            # Merge Sort
            data_copy = original.copy()
            tiempo, memoria = run_benchmark(merge_sort, data_copy)
            writer.writerow(["MergeSort", n, tiempo, memoria])
            print(f"MergeSort listo para N={n}")
            
            # Heap Sort
            data_copy = original.copy()
            tiempo, memoria = run_benchmark(heap_sort, data_copy)
            writer.writerow(["HeapSort", n, tiempo, memoria])
            print(f"HeapSort listo para N={n}")
            
            # Tree Sort (restringido a 100,000 para evitar agotar recursión/memoria)
            if n <= 100000:
                data_copy = original.copy()
                tiempo, memoria = run_benchmark(tree_sort, data_copy)
                writer.writerow(["TreeSort", n, tiempo, memoria])
                print(f"TreeSort listo para N={n}")
                
            # Counting Sort
            data_copy = original.copy()
            tiempo, memoria = run_benchmark(counting_sort_reals, data_copy)
            writer.writerow(["CountingSort", n, tiempo, memoria])
            print(f"CountingSort listo para N={n}")
            
    print("\nResultados de Python guardados en resultados_python.csv")