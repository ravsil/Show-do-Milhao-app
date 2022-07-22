import json
from random import randrange

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
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
    save_question,
    signs_rng,
    skip,
    validate_dict,
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


class AddQuestionScreen(Screen):
    title_add = ObjectProperty(None)
    option1_add = ObjectProperty(None)
    option2_add = ObjectProperty(None)
    option3_add = ObjectProperty(None)
    option4_add = ObjectProperty(None)

    difficulty = None

    def select_difficulty(self, difficulty):
        self.difficulty = difficulty

    def confirm(self):
        title = self.title_add.text
        options = [
            self.option1_add,
            self.option2_add,
            self.option3_add,
            self.option4_add,
        ]
        if title != "" and self.difficulty != None:
            for i, option in enumerate(options):
                if option.text == "":
                    Factory.WarningBad().open()
                    return
                else:
                    options[i] = option.text
            save_question(title, options, self.difficulty)
            self.title_add.text = ""
            self.option1_add.text = ""
            self.option2_add.text = ""
            self.option3_add.text = ""
            self.option4_add.text = ""
            Factory.WarningGood().open()
        else:
            Factory.WarningBad().open()


class AdvancedScreen(Screen):
    custom_json = ObjectProperty(None)

    def update_text(self):
        with open("custom_questions.json", "r") as f:
            tmp = f.read()
        self.custom_json.text = tmp

    def save_custom(self):
        try:
            tmp = validate_dict(json.loads(self.custom_json.text))
            with open("custom_questions.json", "w") as f:
                f.write(json.dumps(tmp, indent=4))
            Factory.WarningGood().open()
            self.custom_json.text = ""
            self.manager.current = "add_question"
        except json.decoder.JSONDecodeError:
            Factory.WarningBad().open()


class ShowDoMilhao(App):
    def build(self):
        # blue background
        Window.clearcolor = (0, 135 / 255, 245 / 255, 1)
        return kv


if __name__ == "__main__":
    kv = Builder.load_file("main.kv")
    ShowDoMilhao().run()
