from random import randrange

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager

from utils import (
    cards_rng,
    check_answer,
    questions_easy,
    questions_hard,
    questions_medium,
    reload_game,
    signs_rng,
    skip,
)


class WindowManager(ScreenManager):
    def cards_help(self):
        self.children[0].ids.cards.disabled = True
        cards_rng(self.children[0])

    def signs_help(self):
        self.children[0].ids.signs.disabled = True
        if signs_rng():
            return self.children[0].question.answer
        else:
            return signs_rng(True, self.children[0].question.answer)

    def academicals_help(self):
        self.children[0].ids.academicals.disabled = True
        return self.children[0].question.answer

    def give_up(self):
        reload_game(self.children[0])


class FirstScreen(Screen):
    pass


class GameScreen(Screen):
    title = ObjectProperty(None)
    one = ObjectProperty(None)
    two = ObjectProperty(None)
    three = ObjectProperty(None)
    four = ObjectProperty(None)
    skip_1 = ObjectProperty(None)
    skip_2 = ObjectProperty(None)
    skip_3 = ObjectProperty(None)

    # makes an copy of the questions so they can be used again later
    game_easy = questions_easy[:]
    game_medium = questions_medium[:]
    game_hard = questions_hard[:]
    # loads the first question to start the game
    question = game_easy.pop(randrange(len(game_easy)))

    score = 0

    # option buttons
    def check_one(self):
        check_answer(self, 1)

    def check_two(self):
        check_answer(self, 2)

    def check_three(self):
        check_answer(self, 3)

    def check_four(self):
        check_answer(self, 4)

    # skip help buttons
    def skip1(self):
        skip(self, self.skip_1)

    def skip2(self):
        skip(self, self.skip_2)

    def skip3(self):
        skip(self, self.skip_3)

    def stop(self):
        reload_game(self)


class LoseScreen(Screen):
    pass


class WinScreen(Screen):
    pass


class ShowDoMilhao(App):
    def build(self):
        # blue background
        Window.clearcolor = (0, 135 / 255, 245 / 255, 1)
        return kv


if __name__ == "__main__":
    kv = Builder.load_file("main.kv")
    ShowDoMilhao().run()
