from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

class BarChartWidget(Screen):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.current_method = "Метод 1"
        
        # Создаем основной BoxLayout
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        
        # Создаем верхний BoxLayout для кнопок
        self.top_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=[5, 5, 5, 5])
        self.layout.add_widget(self.top_layout)
        
        # Кнопка "Отрисовать" занимает 1/3 ширины
        self.draw_button = Button(text="Start", size_hint=(1/3, 1))
        self.draw_button.bind(on_press=self.draw_chart)
        self.top_layout.add_widget(self.draw_button)
        
        # Кнопка выбора метода занимает 2/3 ширины
        self.method_button = Button(text="Choose Sort Method", size_hint=(2/3, 1))
        self.method_button.bind(on_press=self.show_method_selection)
        self.top_layout.add_widget(self.method_button)
        
        # Создаем виджет для графика
        self.chart_widget = BoxLayout(size_hint=(1, 0.9))
        self.layout.add_widget(self.chart_widget)

        # Установите отступы для графика
        self.padding = (20, 20, 20, 20)  # (left, top, right, bottom)
    
    def draw_chart(self, instance):
        self.chart_widget.canvas.clear()
        
        max_value = max(self.data) if self.data else 1
        bar_width = (self.chart_widget.width - self.padding[0] - self.padding[2]) / len(self.data) if self.data else 0
        
        with self.chart_widget.canvas:
            for i, value in enumerate(self.data):
                Color(0, 0, 1, 1)  # Синий цвет
                bar_height = (value / max_value) * (self.chart_widget.height - self.padding[1] - self.padding[3])
                
                x = self.padding[0] + i * bar_width
                y = self.padding[3]
                width = bar_width
                height = bar_height
                
                Rectangle(pos=(x, y), size=(width, height))
    
    def show_method_selection(self, instance):
        content = BoxLayout(orientation='vertical')
        popup = Popup(title='Choose a method', content=content, size_hint=(0.8, 0.8))
        
        for i in range(1, 6):
            btn = Button(text=f'Метод {i}')
            btn.bind(on_press=lambda x, method=f'Метод {i}': self.select_method(method, popup))
            content.add_widget(btn)
        
        popup.open()
    
    def select_method(self, method, popup):
        self.current_method = method
        self.method_button.text = f"{method}"
        popup.dismiss()
