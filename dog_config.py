from common import Input, ConfigKey, FailAction


class DogConfig:
    __input = Input.BUTTON
    __with_motor = True
    __full_screen = True

    def __init__(self, config_as_json):
        self.json_config = config_as_json
        if ConfigKey.STRATEGY.value not in config_as_json:
            raise "Invalid config : strategy is mandatory"
        if ConfigKey.DOG_NAME.value not in config_as_json:
            raise "Invalid config : dog_name is mandatory"

    def get(self, key):
        if key.value in self.json_config:
            return self.__format(key, self.json_config[key.value])
        if key == ConfigKey.INPUT:
            return self.__input
        if key == ConfigKey.WITH_MOTOR:
            return self.__with_motor
        if key == ConfigKey.FULL_SCREEN:
            return self.__full_screen
        return None

    def __format(self, key, value):
        if key == ConfigKey.FAIL_ACTION:
            return FailAction[value]
        if key == ConfigKey.INPUT:
            return Input[value]
        return value
