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


class RemoveQuestionScreen(Screen):
    rq_title = ObjectProperty(None)
    rq_option1 = ObjectProperty(None)
    rq_option2 = ObjectProperty(None)
    rq_option3 = ObjectProperty(None)
    rq_option4 = ObjectProperty(None)

    questions = questions_easy[:] + questions_medium[:] + questions_hard[:]
    index = 0
    index_limit = len(questions) - 1

    def next_question(self):
        question = self.questions[self.index]
        option_indexes = [0, 1, 2, 3]
        option_indexes.remove(question.answer - 1)

        self.rq_title.text = question.title
        self.rq_option1.text = question.options[question.answer - 1]
        self.rq_option2.text = question.options[option_indexes[0]]
        self.rq_option3.text = question.options[option_indexes[1]]
        self.rq_option4.text = question.options[option_indexes[2]]

        if self.index < self.index_limit:
            self.index += 1
        else:
            self.index = 0


class ShowDoMilhao(App):
    def build(self):
        # blue background
        Window.clearcolor = (0, 135 / 255, 245 / 255, 1)
        return kv


if __name__ == "__main__":
    kv = Builder.load_file("main.kv")
    ShowDoMilhao().run()
