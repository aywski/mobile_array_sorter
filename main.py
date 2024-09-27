from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from about_screen import AboutScreen
from bar_chart_screen import BarChartWidget
from file_screen import FileScreen

arrToSort = [386, 235, 51, 200, 471, 339, 450, 117, 135, 150, 224, 419, 43, 378, 313, 44, 344, 106, 93, 36, 369, 262, 28, 401, 326, 245, 152, 315, 125, 220, 212, 354, 107, 388, 300, 193, 487, 184, 426, 293, 166, 223, 298, 356, 219, 380, 495, 130, 391, 334] 

class NavigationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Создаем FloatLayout как основной layout
        main_layout = FloatLayout()
        
        # Добавляем фоновое изображение
        background = Image(source='space.png')
        main_layout.add_widget(background)
        
        # Инициализация ScreenManager
        self.screen_manager = ScreenManager(transition=SlideTransition(duration=0.2))
        self.screen_manager.size_hint = (1, 0.9)
        self.screen_manager.pos_hint = {'top': 1}

        # Текущий активный экран
        self.current_screen = 1

        # Создаем экраны
        screen1 = Screen(name='screen1')
        screen1.add_widget(BarChartWidget(data=arrToSort))

        screen2 = Screen(name='screen2')
        screen2.add_widget(FileScreen(name='file_screen'))

        screen3 = Screen(name='screen3')
        screen3.add_widget(AboutScreen(name="image"))

        # Добавляем экраны в ScreenManager
        self.screen_manager.add_widget(screen1)
        self.screen_manager.add_widget(screen2)
        self.screen_manager.add_widget(screen3)

        # Добавляем ScreenManager в основной layout
        main_layout.add_widget(self.screen_manager)

        # Создаем кнопки навигации
        self.create_navigation_buttons(main_layout)

        # Добавляем основной layout в виджет
        self.add_widget(main_layout)

    def create_navigation_buttons(self, layout):
        # Создаем горизонтальный макет для кнопок
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'bottom': 1})

        # Создаем кнопки
        button1 = Button(text='Visualization')
        button2 = Button(text='Choose File')
        button3 = Button(text='About App')

        # Привязываем переключение экрана к кнопкам
        button1.bind(on_release=lambda x: self.switch_screen(1))
        button2.bind(on_release=lambda x: self.switch_screen(2))
        button3.bind(on_release=lambda x: self.switch_screen(3))

        # Добавляем кнопки в макет
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)
        button_layout.add_widget(button3)

        # Добавляем макет с кнопками в основной layout
        layout.add_widget(button_layout)

    def switch_screen(self, target_screen):
        if target_screen != self.current_screen:
            if target_screen > self.current_screen:
                self.screen_manager.transition.direction = 'left'
            else:
                self.screen_manager.transition.direction = 'right'
            self.screen_manager.current = f'screen{target_screen}'
            self.current_screen = target_screen

class MyApp(App):
    def build(self):
        # Инициализация ScreenManager
        screen_manager = ScreenManager()

        screen_manager.add_widget(NavigationScreen())
        
        return screen_manager


if __name__ == "__main__":
    # Устанавливаем размеры окна для тестирования на ПК
    Window.size = (750/2, 1334/2)
    MyApp().run()
