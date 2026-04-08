from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.core.audio import SoundLoader
import random

from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import requests


TOKEN_EMIL = "8694759403:AAHkyFoBI01dydIfRVn2EDnYSwQhQy9Ek9E"
TOKEN_MAMA = "8673495223:AAHorJk4mRaxe9X6KZ1hqpg6M3b4G4TEOdA"

CHAT_ID_EMIL = "7417931911"
CHAT_ID_MAMA = "7739694262"

class Game(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sounds_button = [
            SoundLoader.load("music/button-click/sound1.mp3"),
            SoundLoader.load("music/button-click/sound2.mp3"),
            SoundLoader.load("music/button-click/sound3.mp3")
        ]

        self.music = SoundLoader.load("music/fonMUSIC.mp3")
        if self.music:
            self.music.loop = True
            self.music.volume = 0.5
            self.music.play()

        # фон
        self.bg = Image(
            source="texturs/Lily.png",
            size_hint=(1, 1)
        )
        self.add_widget(self.bg)

        # кнопка play
        self.btn = Button(
            text="Play",
            size_hint=(None, None),
            size=(200, 100),
            pos=(300, 200),
            background_normal="",
            background_color=(0, 0, 0, 0)
        )

        with self.btn.canvas.before:
            Color(1, 0.4, 0.8, 1)
            self.rect = RoundedRectangle(
                pos=self.btn.pos,
                size=self.btn.size,
                radius=[40]
            )

        self.btn.bind(pos=self.update_rect, size=self.update_rect)
        self.btn.bind(on_press=self.start_game)

        self.add_widget(self.btn)

        # загрузка
        self.loading = ProgressBar(
            max=100,
            value=0,
            size_hint=(0.8, None),
            height=30,
            pos_hint={"center_x": 0.5, "y": 0.05}
        )

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def start_game(self, instance):

        sound = random.choice(self.sounds_button)
        if sound:
            sound.play()

        Animation(opacity=0, duration=1).start(self.btn)

        Animation(size_hint=(1.3, 1.3), duration=10).start(self.bg)

        self.add_widget(self.loading)

        Clock.schedule_interval(self.update_loading, 0.15)

    def update_loading(self, dt):

        if self.loading.value < 100:
            self.loading.value += 1

        else:
            Clock.unschedule(self.update_loading)

            sound = random.choice(self.sounds_button)
            if sound:
                sound.play()

            self.remove_widget(self.loading)

            btn_emil = Button(
                text="Эмиль",
                size_hint=(None, None),
                size=(250, 100),
                pos=(250, 300)
            )

            btn_mama = Button(
                text="Лиля",
                size_hint=(None, None),
                size=(250, 100),
                pos=(250, 150)
            )

            btn_emil.bind(on_press=self.open_chat_emil)
            btn_mama.bind(on_press=self.open_chat_mama)

            self.add_widget(btn_emil)
            self.add_widget(btn_mama)

    def open_chat_emil(self, instance):

        self.clear_widgets()

        self.chat = Label(
            text="Чат Эмиль\n",
            pos_hint={"center_x": 0.5, "top": 1}
        )

        self.input = TextInput(
            size_hint=(0.8, None),
            height=50,
            pos_hint={"center_x": 0.4, "y": 0.05}
        )

        send_btn = Button(
            text="Send",
            size_hint=(0.2, None),
            height=50,
            pos_hint={"x": 0.8, "y": 0.05}
        )

        send_btn.bind(on_press=self.send_to_mama)

        self.add_widget(self.chat)
        self.add_widget(self.input)
        self.add_widget(send_btn)

    def open_chat_mama(self, instance):

        self.clear_widgets()

        self.chat = Label(
            text="Чат Лиля\n",
            pos_hint={"center_x": 0.5, "top": 1}
        )

        self.input = TextInput(
            size_hint=(0.8, None),
            height=50,
            pos_hint={"center_x": 0.4, "y": 0.05}
        )

        send_btn = Button(
            text="Send",
            size_hint=(0.2, None),
            height=50,
            pos_hint={"x": 0.8, "y": 0.05}
        )

        send_btn.bind(on_press=self.send_to_emil)

        self.add_widget(self.chat)
        self.add_widget(self.input)
        self.add_widget(send_btn)

    def send_to_mama(self, instance):

        text = self.input.text

        requests.post(
            f"https://api.telegram.org/bot{TOKEN_EMIL}/sendMessage",
            data={
                "chat_id": CHAT_ID_MAMA,
                "text": text
            }
        )

        self.chat.text += "\nЭмиль: " + text
        self.input.text = ""

    def send_to_emil(self, instance):

        text = self.input.text

        requests.post(
            f"https://api.telegram.org/bot{TOKEN_MAMA}/sendMessage",
            data={
                "chat_id": CHAT_ID_EMIL,
                "text": text
            }
        )

        self.chat.text += "\nЛиля: " + text
        self.input.text = ""


class MyApp(App):
    def build(self):
        return Game()


MyApp().run()