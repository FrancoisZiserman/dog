import random
from common import *
from strat.strategy import Strategy


class OneImage(Strategy):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)


class AllWhite(OneImage):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)

    def get_description(self):
        return '''Entrainement de démarrage, pour apprendre à mettre sa truffe sur l'écran. 
        L'écran est affiché tout blanc, et tout l'écran est actif.'''

    def get_turn(self, index):
        return Turn(index, Selection(self.images.images["white"], True), Selection(self.images.images["white"], True))

    def get_path(self):
        return ""

    def get_image_selection(self):
        return "white"


class OneImageFixRight(OneImage):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)
        self.ok_selection = self.images.get_random_selection()

    def get_description(self):
        return '''Une image est affichée à droite et il n'y a pas d'image à gauche'''

    def get_turn(self, index):
        return Turn(index, self.images.black, self.ok_selection)

    def get_image_selection(self):
        return "apple"


class OneImageFixLeft(OneImage):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)
        self.ok_selection = self.images.get_random_selection()

    def get_description(self):
        return '''Une image est affichée à gauche et il n'y a pas d'image à droite'''

    def get_turn(self, index):
        return Turn(index, self.ok_selection, self.images.black)

    def get_image_selection(self):
        return "apple"


class OneImageFixRandom(OneImage):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)
        self.ok_selection_side = random.choice(list(Side))
        self.ok_selection = self.images.get_random_selection()

    def get_description(self):
        return '''Une image est affichée d'un côté et il n'y a pas d'image de l'autre. 
        Le choix du côté est aléatoire, au lancement du jeu'''

    def get_turn(self, index):
        if self.ok_selection_side == Side.LEFT:
            return Turn(index, self.ok_selection, self.images.black)
        else:
            return Turn(index, self.images.black, self.ok_selection)


class OneImageAlternate(OneImage):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)
        self.ok_selection_side = random.choice(list(Side))
        self.ok_selection = self.images.get_random_selection()

    def get_description(self):
        return '''Une image est affichée d'un côté et il n'y a pas d'image de l'autre. 
        La composition s'inverse d'ou tour à l'autre'''

    def get_turn(self, index):
        if self.ok_selection_side == Side.LEFT:
            if index % 2 == 0:
                return Turn(index, self.ok_selection, self.images.black)
            else:
                return Turn(index, self.images.black, self.ok_selection)
        if self.ok_selection_side == Side.RIGHT:
            if index % 2 == 0:
                return Turn(index, self.images.black, self.ok_selection)
            else:
                return Turn(index, self.ok_selection, self.images.black)


class OneImageRandom(OneImage):
    def __init__(self, config, display, db):
        super().__init__(config, display, db)
        self.ok_selection = self.images.get_random_selection()

    def get_description(self):
        return '''Une image est affichée d'un côté et il n'y a pas d'image de l'autre. 
        Le choix du côté est aléatoire à chaque tour.'''

    def get_turn(self, index):
        ok_selection_side = random.choice(list(Side))
        if ok_selection_side == Side.LEFT:
            return Turn(index, self.ok_selection, self.images.black)
        else:
            return Turn(index, self.images.black, self.ok_selection)
