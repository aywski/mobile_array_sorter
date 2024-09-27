class SortingAlgorithms:
    @staticmethod
    def bubble_sort(data):
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                yield data, [j, j + 1]
        yield data, None

    @staticmethod
    def selection_sort(data):
        n = len(data)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if data[j] < data[min_idx]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
            yield data, [i, min_idx]
        yield data, None

    @staticmethod
    def quick_sort(data, low, high):
        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        if low < high:
            pi = partition(data, low, high)
            yield data, list(range(low, high + 1))
            yield from SortingAlgorithms.quick_sort(data, low, pi - 1)
            yield from SortingAlgorithms.quick_sort(data, pi + 1, high)

    @staticmethod
    def insertion_sort(data):
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
            yield data, [i, j + 1]
        yield data, None

    @staticmethod
    def heap_sort(data):
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
                yield from heapify(arr, n, largest)

        n = len(data)

        for i in range(n // 2 - 1, -1, -1):
            yield from heapify(data, n, i)

        for i in range(n - 1, 0, -1):
            data[0], data[i] = data[i], data[0]
            yield data, [0, i]
            yield from heapify(data, i, 0)

        yield data, None