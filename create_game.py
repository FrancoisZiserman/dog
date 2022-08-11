import json

from common import ConfigKey
from create_strategy import create_strategy
from db import Db
from display import Display
from dog_config import DogConfig
from game import Game


def create_game_from_file(file_name):
    with open(file_name, 'r') as f:
        input_config = json.load(f)
        return create_game(input_config)


def create_game(input_config, db=None, display=None):
    config = DogConfig(input_config)
    if display is None:
        display = Display(config.get(ConfigKey.FULL_SCREEN))
    if db is None:
        db = Db()
    strategy = create_strategy(config, display, db)
    game = Game(strategy, display, db)
    return game
