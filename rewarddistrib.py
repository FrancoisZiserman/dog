from time import sleep

try:
    import RPi.GPIO as GPIO
    gpio_ok = True
except ImportError as error:
    gpio_ok = False


class RewardsDistributor:
    __SERVO_PIN = 12
    left = 2.5
    right = 12
    neutral = 12
    sleep_after_left = 0.2
    sleep_after_right = 0.2
    sleep_after_neutral = 0.2

    def __init__(self, parameters):
        self.left = parameters["left"]
        self.right = parameters["right"]
        self.neutral = parameters["neutral"]
        self.sleep_after_left = parameters["sleep_after_left"]
        self.sleep_after_right = parameters["sleep_after_right"]
        self.sleep_after_neutral = parameters["sleep_after_neutral"]
        if not gpio_ok:
            return
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__SERVO_PIN, GPIO.OUT)
        if parameters is None:
            return


    def run(self):
        if not gpio_ok:
            return
        pwm = GPIO.PWM(self.__SERVO_PIN, 50)
        pwm.start(0)
        pwm.ChangeDutyCycle(self.left)
        sleep(self.sleep_after_left)
        pwm.ChangeDutyCycle(self.neutral)
        sleep(self.sleep_after_neutral)
        pwm.ChangeDutyCycle(self.right)
        sleep(self.sleep_after_right)
        pwm.stop()
