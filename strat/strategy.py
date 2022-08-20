import logging
import time

from clic import Clic, ClicMouse
from common import *
from images import Images
from rewarddistrib import RewardsDistributor


class Strategy:
    def __init__(self, config, display, db):
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
        while True:
            if time.time() - start > turn_duration:
                return self.__create_response(Answer.TIMEOUT, start)
            answer = self.__get_answer()
            if answer is None:
                continue
            if answer.left and answer.right:
                if turn.left.ok and turn.right.ok:
                    return self.__reward(start)
                else:
                    continue
            if turn.left.ok and answer.left or turn.right.ok and answer.right:
                return self.__reward(start)
            if turn.left.ok and answer.right or turn.right.ok and answer.left:
                if fail_action == FailAction.ERROR_SCREEN_AND_STEP_FORWARD:
                    self.display_error()
                    return self.__create_response(Answer.FAIL, start)
                else:
                    if fail_action == FailAction.BEEP_AND_STAY or \
                            fail_action == FailAction.ERROR_SCREEN_AND_STAY:
                        self.display_error()
                        self.display.turn(turn)
                        turn_duration += self.get(ConfigKey.FAIL_DURATION)
                    logging.info('{0} : {1}'.format(turn, Response(Answer.FAIL, time.time() - start)))
                    self.db.add_answer(self.__create_response(Answer.FAIL, start))

    def display_error(self):
        self.display.error()
        time.sleep(self.get(ConfigKey.FAIL_DURATION))
        # sound = pygame.mixer.Sound('../resources/sound/fail_trumpet.mp3')
        # sound.play()

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
