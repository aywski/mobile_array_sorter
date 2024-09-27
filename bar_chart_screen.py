from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
import random
import time

class BarChartWidget(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.original_data = data[:]
        self.current_method = "Bubble Sort"
        self.is_sorting = False

        self.start_time = 0
        self.sort_time = 0
        self.sort_interval = 0.01

        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        
        self.top_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=[5, 5, 5, 5])
        self.layout.add_widget(self.top_layout)
        
        self.draw_button = Button(text="Start", size_hint=(1/3, 1))
        self.draw_button.bind(on_press=self.start_sorting)
        self.top_layout.add_widget(self.draw_button)
        
        self.method_button = Button(text="Choose Sort Method", size_hint=(2/3, 1))
        self.method_button.bind(on_press=self.show_method_selection)
        self.top_layout.add_widget(self.method_button)

        self.timer_label = Button(text="Time: 0.00s", size_hint=(1, 0.1), disabled=True)
        self.layout.add_widget(self.timer_label)
        
        self.chart_widget = BoxLayout(size_hint=(1, 0.8))
        self.layout.add_widget(self.chart_widget)

        self.padding = (20, 20, 20, 20)
        
        self.i = 0
        self.j = 0
        self.quick_sort_stack = []
        self.heap_sort_state = None
    
    def draw_chart(self, highlight_indices=None, sorted=False):
        self.chart_widget.canvas.clear()
        
        max_value = max(self.data) if self.data else 1
        bar_width = (self.chart_widget.width - self.padding[0] - self.padding[2]) / len(self.data) if self.data else 0
        
        with self.chart_widget.canvas:
            for i, value in enumerate(self.data):
                if sorted:
                    Color(0, 1, 0, 1)
                elif highlight_indices and i in highlight_indices:
                    Color(1, 0, 0, 1)
                else:
                    Color(0, 0, 1, 1)
                
                bar_height = (value / max_value) * (self.chart_widget.height - self.padding[1] - self.padding[3])
                
                x = self.padding[0] + i * bar_width
                y = self.padding[3]
                width = bar_width
                height = bar_height
                
                Rectangle(pos=(x, y), size=(width, height))

    def reset_sorting(self):
        Clock.unschedule(self.bubble_sort_step)
        Clock.unschedule(self.selection_sort_step)
        Clock.unschedule(self.quick_sort_step)
        Clock.unschedule(self.insertion_sort_step)
        Clock.unschedule(self.heap_sort_step)
        
        self.i = 0
        self.j = 0
        self.quick_sort_stack = []
        self.heap_sort_state = None
        
        self.data = self.original_data[:]
        self.is_sorting = False
        self.sort_time = 0
        self.timer_label.text = "Time: 0.00s"
        self.draw_chart()

    def start_sorting(self, *args):
        self.reset_sorting()
        
        self.is_sorting = True
        self.start_time = time.time()
        Clock.schedule_interval(self.update_timer, 0.1)

        if self.current_method == "Bubble Sort":
            Clock.schedule_interval(self.bubble_sort_step, self.sort_interval)
        elif self.current_method == "Selection Sort":
            Clock.schedule_interval(self.selection_sort_step, self.sort_interval)
        elif self.current_method == "Quick Sort":
            self.quick_sort_stack = [(0, len(self.data) - 1)]
            Clock.schedule_interval(self.quick_sort_step, self.sort_interval)
        elif self.current_method == "Insertion Sort":
            Clock.schedule_interval(self.insertion_sort_step, self.sort_interval)
        elif self.current_method == "Heap Sort":
            self.heap_sort_state = {'phase': 'build', 'i': len(self.data) // 2 - 1}
            Clock.schedule_interval(self.heap_sort_step, self.sort_interval)

    def update_timer(self, dt):
        if self.is_sorting:
            self.sort_time = time.time() - self.start_time
            self.timer_label.text = f"Time: {self.sort_time:.2f}s"

    def bubble_sort_step(self, dt):
        if self.i < len(self.data):
            if self.j < len(self.data) - self.i - 1:
                if self.data[self.j] > self.data[self.j + 1]:
                    self.data[self.j], self.data[self.j + 1] = self.data[self.j + 1], self.data[self.j]
                self.draw_chart(highlight_indices=[self.j, self.j + 1])
                self.j += 1
            else:
                self.j = 0
                self.i += 1
        else:
            Clock.unschedule(self.bubble_sort_step)
            self.finish_sorting()

    def selection_sort_step(self, dt):
        if self.i < len(self.data):
            min_idx = self.i
            for j in range(self.i + 1, len(self.data)):
                if self.data[j] < self.data[min_idx]:
                    min_idx = j
            self.data[self.i], self.data[min_idx] = self.data[min_idx], self.data[self.i]
            self.draw_chart(highlight_indices=[self.i, min_idx])
            self.i += 1
        else:
            Clock.unschedule(self.selection_sort_step)
            self.finish_sorting()

    def quick_sort_step(self, dt):
        if not self.quick_sort_stack:
            Clock.unschedule(self.quick_sort_step)
            self.finish_sorting()
            return

        low, high = self.quick_sort_stack.pop()
        if low < high:
            pi = self.partition(self.data, low, high)
            self.quick_sort_stack.append((low, pi - 1))
            self.quick_sort_stack.append((pi + 1, high))

        self.draw_chart(highlight_indices=list(range(low, high + 1)))

    def partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def insertion_sort_step(self, dt):
        if self.i < len(self.data):
            key = self.data[self.i]
            self.j = self.i - 1
            while self.j >= 0 and key < self.data[self.j]:
                self.data[self.j + 1] = self.data[self.j]
                self.j -= 1
            self.data[self.j + 1] = key
            self.draw_chart(highlight_indices=[self.i, self.j + 1])
            self.i += 1
        else:
            Clock.unschedule(self.insertion_sort_step)
            self.finish_sorting()

    def heap_sort_step(self, dt):
        if self.heap_sort_state['phase'] == 'build':
            if self.heap_sort_state['i'] >= 0:
                self.heapify(len(self.data), self.heap_sort_state['i'])
                self.heap_sort_state['i'] -= 1
            else:
                self.heap_sort_state = {'phase': 'sort', 'i': len(self.data) - 1}
        elif self.heap_sort_state['phase'] == 'sort':
            if self.heap_sort_state['i'] > 0:
                self.data[0], self.data[self.heap_sort_state['i']] = self.data[self.heap_sort_state['i']], self.data[0]
                self.heapify(self.heap_sort_state['i'], 0)
                self.heap_sort_state['i'] -= 1
            else:
                Clock.unschedule(self.heap_sort_step)
                self.finish_sorting()
                return

        self.draw_chart(highlight_indices=[0, self.heap_sort_state['i']])

    def heapify(self, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and self.data[left] > self.data[largest]:
            largest = left

        if right < n and self.data[right] > self.data[largest]:
            largest = right

        if largest != i:
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            self.heapify(n, largest)

    def finish_sorting(self):
        self.is_sorting = False
        Clock.unschedule(self.update_timer)
        self.draw_chart(sorted=True)
        self.timer_label.text = f"Finished in {self.sort_time:.2f}s"

    def show_method_selection(self, instance):
        content = BoxLayout(orientation='vertical')
        popup = Popup(title='Choose a method', content=content, size_hint=(0.8, 0.8))

        methods = ["Bubble Sort", "Selection Sort", "Quick Sort", "Insertion Sort", "Heap Sort"]
        for method in methods:
            btn = Button(text=method)
            btn.bind(on_press=lambda x, method=method: self.select_method(method, popup))
            content.add_widget(btn)
        
        popup.open()
    
    def select_method(self, method, popup):
        self.current_method = method
        self.method_button.text = f"{method}"
        popup.dismiss()