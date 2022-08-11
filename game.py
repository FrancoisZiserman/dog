import logging
import time

from common import ConfigKey


class Game:
    def __init__(self, strategy, display, db):
        self.db = db
        self.start = None
        self.strategy = strategy
        self.display = display

    def run(self):
        logging.basicConfig(filename="data/log.txt", filemode="a", level=logging.DEBUG, format='%(asctime)s: %(message)s')
        logging.info('Start')
        self.start = time.time()
        self.db.start_game(self)
        self.strategy.start()
        for turn_index in range(self.strategy.get(ConfigKey.TURN_COUNT)):
            turn = self.strategy.get_turn(turn_index)
            self.db.start_turn(turn)
            self.display.turn(turn)
            ret = self.strategy.get_answer_or_timeout(turn)
            logging.info('{0} : {1}'.format(turn, ret))
            self.db.add_answer(ret)
            self.db.end_turn(ret)
            if turn_index+1 < self.strategy.get(ConfigKey.TURN_COUNT):
                self.display.black()
                time.sleep(self.strategy.get(ConfigKey.INTERVAL))
        logging.info('End')
        self.db.end_game()

