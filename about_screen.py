from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class AboutScreen(Screen):
    # Окно с фотографией и подписью
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)
        
        # Внешний layout с отступами
        layout = BoxLayout(orientation='vertical', padding=[50, 40, 50, 75])
        
        # Изображение с отступами
        img = Image(source="windowsXP_dog.jpg", size_hint=(1, 0.7))  # Замените на путь к вашей фотографии
        
        # Заголовок
        title = Label(
            text="[b]Array Sorter by Sahalianov[/b]", 
            markup=True, 
            size_hint=(1, 0.1), 
            halign='left', 
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))  # Подгон текста под размер виджета
        
        # Описание
        description = Label(
            text="This program sorts an array of numbers from smallest to largest using different methods. Made as lab assignment 1.", 
            size_hint=(1, 0.2), 
            halign='left', 
            valign='top'
        )
        description.bind(size=description.setter('text_size'))  # Подгон текста под размер виджета

        layout.add_widget(img)
        layout.add_widget(title)
        layout.add_widget(description)

        self.add_widget(layout)