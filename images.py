import pathlib
import random
import re
from os import listdir
from os.path import isfile, join

import pygame
from common import Selection, Image


class Images:
    def __init__(self, path, size, criteria=None, root_path="resources/pict/"):
        self.images = {}
        self.image_keys = None
        self.black = None
        self.__load(size, path, criteria, root_path)

    def __load(self, size, path, criteria, root_path):
        root_pict_path = self.__get_path(root_path)
        path = root_pict_path + path
        pictures = [f for f in listdir(path) if isfile(join(path, f))]
        for pict in pictures:
            if pict.endswith(".jpg") or pict.endswith(".png"):
                if criteria is not None and not re.search(criteria, pict):
                    continue
                image = self.__load_one_image(pict, size, path)
                key = pict.split(".")[0]
                self.images[key] = image
        self.image_keys = list(self.images)
        black_image = self.__load_one_image("black.png", size, root_pict_path)
        self.black = Selection(black_image, False)

    def get_selection(self, key, ok=True):
        return Selection(self.images[key], ok)

    def get_random_selection(self, ok=True):
        image_key = random.choice(self.image_keys)
        return self.get_selection(image_key, ok)

    @staticmethod
    def __load_one_image(pict, size, path):
        img = pygame.image.load(path + "/" + pict)
        img = pygame.transform.scale(img, (size, size))
        image = Image(pict, img)
        return image

    @staticmethod
    def __get_path(root_path):
        current_path = pathlib.Path().resolve()
        return str(current_path) + "/" + root_path
