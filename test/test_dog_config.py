from common import ConfigKey
from dog_config import DogConfig


def test_dog_config_get_ok():
    j = {"strategy": "LearnFromFirst", "dog_name": "Marcel"}
    config = DogConfig(j)
    assert config.get(ConfigKey.STRATEGY) == "LearnFromFirst"


def test_dog_config_get_none():
    j = {"strategy": "LearnFromFirst", "dog_name": "Marcel"}
    config = DogConfig(j)
    assert config.get(ConfigKey.PATH) is None
