import sys
from create_game import create_game_from_file
from help import print_help


class Main:
    help = False

    def __init__(self):
        if len(sys.argv) == 1 or sys.argv[1] == "help":
            self.help = True

    def run(self):
        if self.help:
            print_help()
            return

        file_name = sys.argv[1]
        game = create_game_from_file(file_name)
        game.run()


main = Main()
main.run()
