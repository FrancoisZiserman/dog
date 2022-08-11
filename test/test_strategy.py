import random
from unittest.mock import MagicMock

from create_strategy import create_strategy_from_json


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


def test_all_white():
    j = {"strategy": "AllWhite", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "AllWhite"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "white.png", "ok": True}, {"name": "white.png", "ok": True})


def test_reward_parameters():
    j = {"strategy": "AllWhite", "dog_name": "Marcel", "input": "MOUSE", "with_motor": True, "full_screen": False,
         "reward_parameters": {
             "left": 1,
             "right": 2,
             "neutral": 3,
             "sleep_after_left": 4,
             "sleep_after_right": 5,
             "sleep_after_neutral": 6
         }
    }
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.reward_distributor.left == 1
    assert strategy.reward_distributor.right == 2
    assert strategy.reward_distributor.neutral == 3
    assert strategy.reward_distributor.sleep_after_left == 4
    assert strategy.reward_distributor.sleep_after_right == 5
    assert strategy.reward_distributor.sleep_after_neutral == 6


def test_one_image_fix_right_default():
    j = {"strategy": "OneImageFixRight", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "OneImageFixRight"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "black.png", "ok": False}, {"name": "apple.png", "ok": True})


def test_one_image_fix_right_selection():
    j = {"strategy": "OneImageFixRight", "dog_name": "Marcel", "image_selection": "bringle", "input": "MOUSE", "with_motor": False,
         "full_screen": False}
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "OneImageFixRight"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "black.png", "ok": False}, {"name": "bringle.png", "ok": True})


def test_one_image_fix_left():
    j = {"strategy": "OneImageFixLeft", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "OneImageFixLeft"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "apple.png", "ok": True}, {"name": "black.png", "ok": False})


def test_one_image_fix_left_selection():
    j = {"strategy": "OneImageFixLeft", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False,
         "path": "all_picts", "image_selection": "bento"}
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "OneImageFixLeft"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "bento.png", "ok": True}, {"name": "black.png", "ok": False})


def test_one_image_fix_random():
    j = {"strategy": "OneImageFixRandom", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    random.seed(10)
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "OneImageFixRandom"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "lemon.png", "ok": True}, {"name": "black.png", "ok": False})


def test_one_image_alternate():
    j = {"strategy": "OneImageAlternate", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    random.seed(10)
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "OneImageAlternate"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "lemon.png", "ok": True}, {"name": "black.png", "ok": False})
    turn = strategy.get_turn(1)
    check_turn(turn, {"name": "black.png", "ok": False}, {"name": "lemon.png", "ok": True})


def test_one_image_random():
    j = {"strategy": "OneImageRandom", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    random.seed(10)
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "OneImageRandom"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "bringle.png", "ok": True}, {"name": "black.png", "ok": False})
    turn = strategy.get_turn(1)
    check_turn(turn, {"name": "black.png", "ok": False}, {"name": "bringle.png", "ok": True})


def test_fix_right():
    j = {"strategy": "FixRight", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    random.seed(10)
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "FixRight"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "black.png", "ok": False}, {"name": "bringle.png", "ok": True})


def test_fix_left():
    j = {"strategy": "FixLeft", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    random.seed(10)
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "FixLeft"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "bringle.png", "ok": True}, {"name": "black.png", "ok": False})


def test_fix_random():
    j = {"strategy": "FixRandom", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    random.seed(10)
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "FixRandom"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "lemon.png", "ok": True}, {"name": "black.png", "ok": False})


def test_fix_alternate():
    j = {"strategy": "Alternate", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    random.seed(10)
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "Alternate"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "lemon.png", "ok": True}, {"name": "black.png", "ok": False})


def test_fix_alternate():
    j = {"strategy": "Random", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    random.seed(10)
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "Random"
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "lemon.png", "ok": True}, {"name": "black.png", "ok": False})


def test_fix_learn_from_first():
    j = {"strategy": "LearnFromFirst", "dog_name": "Marcel", "input": "MOUSE", "with_motor": False, "full_screen": False}
    random.seed(10)
    strategy = create_strategy_from_json(j, mock_display, mock_db)
    assert strategy.__class__.__name__ == "LearnFromFirst"
    strategy.start()
    turn = strategy.get_turn(0)
    check_turn(turn, {"name": "bringle.png", "ok": True}, {"name": "black.png", "ok": False})


def check_turn(turn, left, right):
    assert turn.__class__.__name__ == "Turn"
    assert turn.left.image.name == left["name"]
    assert turn.left.ok == left["ok"]
    assert turn.right.image.name == right["name"]
    assert turn.right.ok == right["ok"]
