import json
from random import randint, randrange, shuffle

from kivy.factory import Factory


class Question:
    def __init__(self, title, options):
        self.title = title
        self.options = options
        # makes the answer position different everytime
        shuffle(self.options)

        # gets the answer position
        for i, j in enumerate(self.options):
            if "*" in j:
                options[i] = j.replace("*", "")
                self.answer = i + 1


with open("questions.json", "r") as f:
    questions = json.loads(f.read())

questions_easy = []
questions_medium = []
questions_hard = []

for i in questions:
    if questions[i]["difficulty"] == "easy":
        questions_easy.append(
            Question(
                questions[i]["title"],
                questions[i]["options"],
            )
        )
    if questions[i]["difficulty"] == "medium":
        questions_medium.append(
            Question(
                questions[i]["title"],
                questions[i]["options"],
            )
        )
    if questions[i]["difficulty"] == "hard":
        questions_hard.append(
            Question(
                questions[i]["title"],
                questions[i]["options"],
            )
        )

# checks if selected option is right or wrong
def check_answer(obj, option):
    reload_options(obj)

    if obj.question.answer == option:
        obj.score += 1
        if obj.score < 3:
            new_question(obj, obj.game_easy)
        elif obj.score < 10:
            new_question(obj, obj.game_medium)
        elif obj.score < 14:
            new_question(obj, obj.game_hard)
        # last question has no help
        elif obj.score == 14:
            Factory.MilionMessage().open()
            disable_help(obj)
            new_question(obj, obj.game_hard)
        elif obj.score == 15:
            obj.score = 0
            obj.manager.current = "win"
            reload_game(obj)
    else:
        obj.manager.current = "lose"
        reload_game(obj)


# skips current question
def skip(obj, skip_btn):
    reload_options(obj)

    skip_btn.disabled = True
    if obj.score < 3:
        new_question(obj, obj.game_easy)
    elif obj.score < 10:
        new_question(obj, obj.game_medium)
    elif obj.score <= 14:
        new_question(obj, obj.game_hard)


def new_question(obj, question_difficulty):
    obj.question = question_difficulty.pop(randrange(len(question_difficulty)))
    obj.title.text = obj.question.title
    obj.one.text = f"1: {obj.question.options[0]}"
    obj.two.text = f"2: {obj.question.options[1]}"
    obj.three.text = f"3: {obj.question.options[2]}"
    obj.four.text = f"4: {obj.question.options[3]}"


def cards_rng(obj):
    odds = [1, 2, 2, 3]
    choice = odds.pop(randrange(len(odds)))
    options = [obj.one, obj.two, obj.three, obj.four]
    options.pop(obj.question.answer - 1)
    shuffle(options)
    for i in range(choice):
        options[i].disabled = True


def signs_rng(wrong_option=False, answer=None):
    choice = randint(1, 5)

    if not wrong_option:
        if choice != 5:
            return True
        else:
            return False
    else:
        options = [1, 2, 3, 4]
        options.remove(answer)
        return options.pop(randrange(len(options)))


def disable_help(obj):
    helps = [obj.cards, obj.signs, obj.academicals, obj.skip_1, obj.skip_2, obj.skip_3]
    obj.stop_btn.disabled = True
    for help in helps:
        help.disabled = True


def reload_game(obj):
    # displays the score and resets the game
    obj.manager.get_screen("lose").score_message.text = f"Pontuação: {obj.score}"
    obj.score = 0
    obj.game_easy = questions_easy[:]
    obj.game_medium = questions_medium[:]
    obj.game_hard = questions_hard[:]
    obj.cards.disabled = False
    obj.signs.disabled = False
    obj.academicals.disabled = False
    obj.skip_1.disabled = False
    obj.skip_2.disabled = False
    obj.skip_3.disabled = False
    obj.stop_btn.disabled = False
    new_question(obj, obj.game_easy)


def reload_options(obj):
    options = [obj.one, obj.two, obj.three, obj.four]
    for option in options:
        if option.disabled:
            option.disabled = False
