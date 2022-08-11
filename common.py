from enum import Enum


class Answer(Enum):
    TIMEOUT = 1
    FAIL = 2
    OK = 3


class Input(Enum):
    MOUSE = 1
    BUTTON = 2


class ConfigKey(Enum):
    DOG_NAME = "dog_name"
    STRATEGY = "strategy"
    PATH = "path"
    IMAGE_SELECTION = "image_selection"
    TURN_COUNT = "turn_count"
    INTERVAL = "interval"
    TURN_DURATION = "turn_duration"
    REPEAT_START = "repeat_start"
    FAIL_ACTION = "fail_action"
    FAIL_DURATION = "fail_duration"
    FULL_SCREEN = "full_screen"
    WITH_MOTOR = "with_motor"
    INPUT = "input"
    REWARD_PARAMETERS = "reward_parameters"


class FailAction(Enum):
    ERROR_SCREEN_AND_STEP_FORWARD = 1
    BEEP_AND_STAY = 2
    ERROR_SCREEN_AND_STAY = 3
    STAY_IN_SILENCE = 4


class Response:
    def __init__(self, answer, delta):
        self.answer = answer
        self.delta = delta

    def __str__(self):
        return str(self.answer) + " in " + format(self.delta, '.2f') + " s"


class Side(Enum):
    LEFT = 0
    RIGHT = 1


class Image:
    def __init__(self, name, pict):
        self.name = name
        self.pict = pict


class Selection:
    def __init__(self, image, ok):
        self.image = image
        self.ok = ok

    def __str__(self):
        if self.ok:
            return self.image.name + "*"
        else:
            return self.image.name


class Turn:
    def __init__(self, index, left, right):
        self.index = index
        self.left = left
        self.right = right

    def __str__(self):
        return "Turn[" + str(self.index) + "]{ " + str(self.left) + ", " + str(self.right) + " }"


class Action:
    def __init__(self, left, right):
        self.left = left
        self.right = right
