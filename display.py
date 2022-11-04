import pygame


class Display:
    def __init__(self, full_screen, error_color=(0, 0, 255)):
        self.error_color = error_color
        pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
        pygame.mixer.init()
        pygame.init()
        if full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1024, 600), 0, 32)
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.size = 0
        if self.width / 2 > self.height:
            self.size = self.height
        else:
            self.size = self.width / 2
        self.height_margin = (self.height - self.size) / 2
        if self.height_margin < 0:
            self.height_margin = 0

    def turn(self, turn):
        self.screen.fill((0, 0, 0))
        self.screen.blit(turn.left.image.pict, (0, self.height_margin))
        self.screen.blit(turn.right.image.pict, (self.width - self.size, self.height_margin))
        pygame.display.update()

    def error(self):
        self.__fill(self.error_color)

    def black(self):
        self.__fill((128, 128, 128))

    def __fill(self, color):
        self.screen.fill(color)
        pygame.display.update()
