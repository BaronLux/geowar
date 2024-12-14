import kivy
kivy.require('1.0.6')  # замените на вашу текущую версию kivy
from game import game, game_state
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class ChatApp(App):
    font_size = '40sp'

    def build(self):
        self.title = 'GeoWar'
        self.layout = BoxLayout(orientation='vertical')

        # Создаем ScrollView для отображения истории сообщений
        self.messages_scroll = ScrollView()
        self.messages_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.messages_box.bind(minimum_height=self.messages_box.setter('height'))
        self.messages_scroll.add_widget(self.messages_box)

        self.layout.add_widget(self.messages_scroll)

        # Создаем строку для ввода сообщения
        self.input_box = BoxLayout(size_hint_y=None, height=80)
        self.text_input = TextInput(
            hint_text='Input message', font_size=self.font_size,
            multiline=False, )
        self.send_button = Button(text='Send', font_size=self.font_size)
        self.send_button.bind(on_press=self.send_message)

        self.input_box.add_widget(self.text_input)
        self.input_box.add_widget(self.send_button)

        self.layout.add_widget(self.input_box)
        self.update_screen()
        return self.layout

    def update_screen(self):
        state = next(game_state)
        while not game.wait_for_input:
            self.add_message(state)
            game.messages += [state]
            state = next(game_state)

    def add_message(self, message):
        label = Label(text=message, size_hint_y=None,
                      height=60, font_size=self.font_size)
        self.messages_box.add_widget(label)

    def send_message(self, instance):
        message = self.text_input.text
        if message:
            # Добавляем сообщение в историю
            self.add_message(message)
            game.get_user_message(self.text_input.text)
            self.update_screen()
            self.text_input.text = ''  # Очищаем поле ввода

            # Прокручиваем вниз, чтобы видеть новое сообщение
            # self.messages_scroll.scroll_to(self.messages_box)


if __name__ == '__main__':
    ChatApp().run()
