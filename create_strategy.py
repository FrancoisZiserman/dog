from dog_config import DogConfig
from strat.multipleimages import *
from strat.oneimage import *


def create_strategy_from_json(input_config, display, db):
    config = DogConfig(input_config)
    return create_strategy(config, display, db)


def create_strategy(config, display, db):
    klass = config.get(ConfigKey.STRATEGY)
    return globals()[klass](config, display, db)
