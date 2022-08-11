import pigpio
import pygame

from common import Action


class Clic:
    __IO_LEFT = 2
    __IO_RIGHT = 3

    def __init__(self):
        self.pigio_ok = True
        try:
            self.pi = pigpio.pi()  # Connect to pigpiod daemon
            # Set up pins as an output
            self.pi.set_mode(self.__IO_LEFT, pigpio.INPUT)
            self.pi.set_mode(self.__IO_RIGHT, pigpio.INPUT)
            self.pi.set_pull_up_down(self.__IO_LEFT, pigpio.PUD_DOWN)
            self.pi.set_pull_up_down(self.__IO_RIGHT, pigpio.PUD_DOWN)
        except:
            self.pigio_ok = False

    def read(self):
        if not self.pigio_ok:
            return
        left = self.pi.read(self.__IO_LEFT)
        right = self.pi.read(self.__IO_RIGHT)
        if left != 0 and right != 0:
            return None
        return Action(left=left == 0, right=right == 0)


class ClicMouse:
    def __init__(self, size):
        self.__size = size

    def read(self):
        width = pygame.display.Info().current_w
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x = pygame.mouse.get_pos()[0]
                return Action(left=pos_x < self.__size, right=pos_x > width - self.__size)
        return None
