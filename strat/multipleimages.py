import random
from common import *
from strat.strategy import Strategy


class FixRight(Strategy):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)

    def get_description(self):
        return '''Une image est affichée à droite, choisie parmi 5 images et il n'y a pas d'image à gauche'''

    def get_turn(self, index):
        return Turn(index, self.images.black, self.images.get_random_selection())


class FixLeft(Strategy):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)

    def get_description(self):
        return '''Une image est affichée à gauche choisie parmi 5 images et il n'y a pas d'image à droite'''

    def get_turn(self, index):
        return Turn(index, self.images.get_random_selection(), self.images.black)


class FixRandom(Strategy):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)
        self.ok_selection_side = random.choice(list(Side))

    def get_description(self):
        return '''Une image est affichée d'un côté et il n'y a pas d'image de l'autre. 
        Le choix du côté est aléatoire, au lancement du jeu'''

    def get_turn(self, index):
        if self.ok_selection_side == Side.LEFT:
            return Turn(index, self.images.get_random_selection(), self.images.black)
        else:
            return Turn(index, self.images.black, self.images.get_random_selection())


class Alternate(Strategy):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)
        self.ok_selection_side = random.choice(list(Side))

    def get_description(self):
        return '''Une image est affichée d'un côté et il n'y a pas d'image de l'autre. 
        La composition s'inverse d'ou tour à l'autre'''

    def get_turn(self, index):
        if self.ok_selection_side == Side.LEFT:
            if index % 2 == 0:
                return Turn(index, self.images.get_random_selection(), self.images.black)
            else:
                return Turn(index, self.images.black, self.images.get_random_selection())
        if self.ok_selection_side == Side.RIGHT:
            if index % 2 == 0:
                return Turn(index, self.images.black, self.images.get_random_selection())
            else:
                return Turn(index, self.images.get_random_selection(), self.images.black)


class Random(Strategy):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)

    def get_description(self):
        return '''Une pomme est affichée d'un côté et il n'y a pas d'image de l'autre. 
        Le choix du côté est aléatoire à chaque tour.'''

    def get_turn(self, index):
        ok_selection_side = random.choice(list(Side))
        if ok_selection_side == Side.LEFT:
            return Turn(index, self.images.get_random_selection(), self.images.black)
        else:
            return Turn(index, self.images.black, self.images.get_random_selection())


class LearnFromFirst(Strategy):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)
        self.elected_image = None
        self.elected_image_key = None

    def get_description(self):
        return '''Une image est choisie au démarrage. Elle est affichée seule au début. 
        Elle est affichée avec une autre image choisie au hasard ensuite.
        L'image choisie est affichée seule pendant ''' + str(self.get_repeat_start()) + " tours."

    def start(self):
        super().start()
        self.elected_image_key = random.choice(self.images.image_keys)
        self.elected_image = self.images.get_selection(self.elected_image_key)
        self.images.image_keys.remove(self.elected_image_key)

    def get_turn(self, index):
        side = random.choice(list(Side))
        if index < self.get_repeat_start():
            other = self.images.black
        else:
            other = self.images.get_random_selection(ok=False)
        if side == Side.LEFT:
            return Turn(index, self.elected_image, other)
        else:
            return Turn(index, other, self.elected_image)

    def get_repeat_start(self):
        rep = self.config.get(ConfigKey.REPEAT_START)
        if rep is not None:
            return rep
        return 3
