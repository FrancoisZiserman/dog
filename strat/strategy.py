import logging
import time
import pathlib
import pygame

from clic import Clic, ClicMouse
from common import *
from images import Images
from rewarddistrib import RewardsDistributor


class Strategy:
    def __init__(self, config, display, db):
        self.sound_path = str(pathlib.Path().resolve()) + "/resources/sound/"

        self.images = None
        self.db = db
        self.config = config
        self.display = display
        self.clic = self.__create_clic()
        self.images = Images(self.get(ConfigKey.PATH), self.display.size, self.get(ConfigKey.IMAGE_SELECTION))
        if self.get(ConfigKey.WITH_MOTOR):
            self.reward_distributor = RewardsDistributor(self.config.get(ConfigKey.REWARD_PARAMETERS))

    def get_description(self):
        raise ValueError("strategy get_description must be defined")

    def start(self):
        pass

    def get_turn(self, index):
        raise ValueError("strategy get_turn must be defined")

    def get_answer_or_timeout(self, turn):
        start = time.time()
        fail_action = self.get(ConfigKey.FAIL_ACTION)
        turn_duration = self.get(ConfigKey.TURN_DURATION)
        self.display_turn(turn)
        while True:
            if time.time() - start > turn_duration:
                return self.__create_response(Answer.TIMEOUT, start)
            answer = self.__get_answer()
            if answer is None:
                continue
            if (turn.left.ok and turn.right.ok) and (answer.left or answer.right):
                return self.__reward(start)
            if turn.left.ok and answer.left or turn.right.ok and answer.right:
                return self.__reward(start)
            if turn.left.ok and answer.right or turn.right.ok and answer.left:
                if fail_action == FailAction.ERROR_SCREEN_AND_STEP_FORWARD:
                    self.display_error_simple()
                    return self.__create_response(Answer.FAIL, start)
                else:
                    logging.info('{0} : {1}'.format(turn, Response(Answer.FAIL, time.time() - start)))
                    self.db.add_answer(self.__create_response(Answer.FAIL, start))
                    if fail_action == FailAction.ERROR_SCREEN_AND_STAY:
                        turn_duration += self.display_error(turn, start)
                        self.display_turn(turn)

    def display_turn(self, turn):
        self.display.turn(turn)
        if self.get(ConfigKey.START_SOUND):
            self.__play_sound("invalid_keypress")

    def display_error_simple(self):
        self.display.error()
        if self.get(ConfigKey.FAIL_SOUND):
            self.__play_sound("fail_trumpet")

    def display_error(self, turn, start):
        start_display_error = time.time()
        self.display_error_simple()
        time_to_sleep = self.get(ConfigKey.FAIL_DURATION)
        time_to_sleep_remain = time_to_sleep
        while time_to_sleep_remain > 0:
            time.sleep(0.1)
            time_to_sleep_remain -= 0.1
            if self.__get_answer() is not None:
                logging.info('{0} : {1}'.format(turn, Response(Answer.TRY_DURING_ERROR, time.time() - start)))
                self.db.add_answer(self.__create_response(Answer.TRY_DURING_ERROR, start))
                time_to_sleep_remain = time_to_sleep
                self.__play_sound("fail_trumpet")
        return time.time() - start_display_error

    def __play_sound(self, sound_name):
        file = f'{self.sound_path}{sound_name}.mp3'
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        pygame.event.wait()

    def __reward(self, start):
        if self.get(ConfigKey.WITH_MOTOR):
            self.reward_distributor.run()
        return self.__create_response(Answer.OK, start)

    @staticmethod
    def __create_response(answer, start):
        return Response(answer, time.time() - start)

    def __get_answer(self):
        return self.clic.read()

    def get(self, key):
        rep = self.config.get(key)
        if rep is not None:
            return rep
        return getattr(self, "get_" + key.value)()

    def get_path(self):
        return "FiveImages"

    def get_image_selection(self):
        return ""

    def get_turn_count(self):
        return 5

    def get_turn_duration(self):
        return 1

    def get_interval(self):
        return 0.3

    def get_fail_action(self):
        return FailAction.ERROR_SCREEN_AND_STAY

    def __create_clic(self):
        if self.get(ConfigKey.INPUT) == Input.BUTTON:
            return Clic()
        else:
            return ClicMouse(self.display.size)
