from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
import time

from algorithms import SortingAlgorithms

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

        # Замена текущего блока добавления кнопки таймера
        self.timer_label_container = BoxLayout(size_hint=(1, 0.1), padding=[10, 0])  # Добавляем контейнер с отступами
        self.timer_label = Button(text="Time: 0.00s", size_hint=(1, 1), disabled=True)
        self.timer_label_container.add_widget(self.timer_label)  # Добавляем кнопку в контейнер
        self.layout.add_widget(self.timer_label_container)  # Добавляем контейнер в главный layout

        self.chart_widget = BoxLayout(size_hint=(1, 0.8))
        self.layout.add_widget(self.chart_widget)

        self.padding = (20, 20, 20, 20)
        
        self.i = 0
        self.j = 0
        self.quick_sort_stack = []
        self.heap_sort_state = None
    
    def update_data(self, new_data):
        self.data = new_data
        self.original_data = new_data[:]  # Сохраняем оригинальные данные
        self.draw_chart()  # Перерисовываем график с новыми данными

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
        Clock.unschedule(self.sorting_step)
        self.data = self.original_data[:]
        self.is_sorting = False
        self.sort_time = 0
        self.timer_label.text = "Time: 0.00s"
        self.draw_chart()

    def start_sorting(self, *args):
        self.reset_sorting()
        self.is_sorting = True
        self.start_time = time.time()
        Clock.schedule_interval(self.update_timer, 0.01)

        if self.current_method == "Bubble Sort":
            self.sorting_generator = SortingAlgorithms.bubble_sort(self.data)
        elif self.current_method == "Selection Sort":
            self.sorting_generator = SortingAlgorithms.selection_sort(self.data)
        elif self.current_method == "Quick Sort":
            self.sorting_generator = SortingAlgorithms.quick_sort(self.data, 0, len(self.data) - 1)
        elif self.current_method == "Insertion Sort":
            self.sorting_generator = SortingAlgorithms.insertion_sort(self.data)
        elif self.current_method == "Heap Sort":
            self.sorting_generator = SortingAlgorithms.heap_sort(self.data)

        Clock.schedule_interval(self.sorting_step, self.sort_interval)

    def update_timer(self, dt):
        if self.is_sorting:
            self.sort_time = time.time() - self.start_time
            self.timer_label.text = f"Time: {self.sort_time:.2f}s"

    def sorting_step(self, dt):
        try:
            self.data, highlight_indices = next(self.sorting_generator)
            if highlight_indices is not None:
                self.draw_chart(highlight_indices=highlight_indices)
            else:
                self.finish_sorting()
        except StopIteration:
            self.finish_sorting()

    def finish_sorting(self):
        self.is_sorting = False
        Clock.unschedule(self.update_timer)
        Clock.unschedule(self.sorting_step)
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