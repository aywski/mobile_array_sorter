from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from plyer import filechooser

class FileScreen(Screen):
    arr_to_sort = [] 
    
    def __init__(self, arr_to_sort, **kwargs):
        super(FileScreen, self).__init__(**kwargs)
        
        self.layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=10)
        
        self.content_label = Label(text='', size_hint_y=None, height=300)
        self.layout.add_widget(self.content_label)

        # Поле ввода для ввода данных вручную
        self.input_field = TextInput(hint_text='Enter an array of numbers separated by spaces', multiline=False)
        self.layout.add_widget(self.input_field)

        # Кнопка для применения введенного массива
        apply_button = Button(text='Apply')
        apply_button.bind(on_release=self.apply_manual_array)
        self.layout.add_widget(apply_button)

        self.top_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1), spacing=10)
        self.layout.add_widget(self.top_layout)

        # Кнопка для сохранения массива в файл
        save_button = Button(text='Save file', size_hint=(1/2, 1))
        save_button.bind(on_release=self.save_to_file)
        self.top_layout.add_widget(save_button)

        load_button = Button(text='Load file', size_hint=(1/2, 1))
        load_button.bind(on_release=self.open_filechooser)
        self.top_layout.add_widget(load_button)

        self.add_widget(self.layout)
        self.file_path = None
    
    def open_filechooser(self, instance):
        # Открытие системного диалога выбора файла
        filechooser.open_file(on_selection=self.load_file)
    
    def load_file(self, selection):
        if selection:
            self.file_path = selection[0]
            try:
                with open(self.file_path, 'r') as file:
                    content = file.read()
                    # Предполагаем, что содержимое файла – это числа, разделенные пробелами
                    self.arr_to_sort[:] = list(map(int, content.split(' ')))  # Обновляем arrToSort

                    bar_chart_widget = self.parent.parent.get_screen('screen1').children[0]  # Получаем BarChartWidget
                    bar_chart_widget.update_data(self.arr_to_sort)  # Обновляем данные в BarChartWidget

                    # Обновление отображаемого содержимого
                    self.update_content_label()
                    
            except Exception as e:
                self.content_label.text = f"Error reading file: {e}"

    def update_content_label(self):
        # Отображение первых 5 элементов массива
        display_content = ' '.join(map(str, self.arr_to_sort[:5]))
        self.content_label.text = f"Array: {display_content}"

    def apply_manual_array(self, instance):
        try:
            # Преобразование введенного текста в массив чисел
            self.arr_to_sort[:] = list(map(int, self.input_field.text.split()))
            self.update_content_label()
            
            bar_chart_widget = self.parent.parent.get_screen('screen1').children[0]  # Получаем BarChartWidget
            bar_chart_widget.update_data(self.arr_to_sort)  # Обновляем данные в BarChartWidget
            self.input_field.text = ''  # Очищаем поле ввода
            
        except ValueError:
            self.content_label.text = "Please enter valid numbers"

    def save_to_file(self, instance):
        # Открытие диалога выбора пути для сохранения файла
        filechooser.save_file(on_selection=self.save_file)

    def save_file(self, selection):
        if selection:
            file_path = selection[0]
            try:
                with open(file_path, 'w') as file:
                    # Сохранение массива в файл
                    file.write(' '.join(map(str, self.arr_to_sort)))
                    self.content_label.text = "The array was saved successfully!"
            except Exception as e:
                self.content_label.text = f"Error saving file: {e}"
