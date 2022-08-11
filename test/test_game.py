from unittest.mock import MagicMock

import pygame

from create_game import create_game
from display import Display


class DummyDisplay:
    pass


class DummyDb:
    pass


mock_display = DummyDisplay()
mock_display.error = MagicMock()
mock_display.black = MagicMock()
mock_display.turn = MagicMock()
mock_display.size = 200

mock_db = DummyDb()
mock_db.start_game = MagicMock()
mock_db.end_game = MagicMock()
mock_db.start_turn = MagicMock()
mock_db.end_turn = MagicMock()
mock_db.add_answer = MagicMock()


def test_create_game():
    j = {"strategy": "AllWhite", "dog_name": "Marcel",
         "input": "MOUSE", "with_motor": False, "full_screen": False,
         "turn_duration": 0.01, "interval": 0.01}
    pygame.init()
    game = create_game(j, mock_db, mock_display)
    assert game.strategy.__class__.__name__ == "AllWhite"
    game.run()