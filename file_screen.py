from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from plyer import filechooser

class FileScreen(Screen):
    def __init__(self, **kwargs):
        super(FileScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding = [20, 20, 20, 20])
        
        load_button = Button(text='Load File')
        load_button.bind(on_release=self.open_filechooser)
        layout.add_widget(load_button)
        
        show_button = Button(text='Show File Content')
        show_button.bind(on_release=self.show_content)
        layout.add_widget(show_button)
        
        self.content_label = Label(text='', size_hint_y=None, height=Window.height - 200)
        layout.add_widget(self.content_label)

        self.add_widget(layout)
        self.file_path = None
    
    def open_filechooser(self, instance):
        # Открытие системного диалога выбора файла
        filechooser.open_file(on_selection=self.load_file)
    
    def load_file(self, selection):
        if selection:
            self.file_path = selection[0]
    
    def show_content(self, instance):
        if self.file_path:
            try:
                with open(self.file_path, 'r') as file:
                    content = file.read()
                self.content_label.text = content
            except Exception as e:
                self.content_label.text = f"Error reading file: {e}"