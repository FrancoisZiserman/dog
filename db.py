import time
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, text, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from common import Answer, ConfigKey

SQL_FILE = 'dog.db'
DB_PATH = "data/"


Base = declarative_base()


class RowGame(Base):
    __tablename__ = 'game'
    id = Column(Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    dog_name = Column(String(35), nullable=False)
    creation = Column(DateTime(), nullable=False)
    strategy = Column(String(25), nullable=False)
    description = Column(Text(), nullable=False)
    images = Column(Integer(), nullable=False)
    turn_count = Column(Integer(), nullable=False)
    timeout = Column(Integer(), nullable=False)
    interval = Column(Integer(), nullable=False)
    fail_action = Column(String(15), nullable=False)
    repeat_start = Column(Integer(), nullable=True)


class RowTurn(Base):
    __tablename__ = 'turn'
    id = Column(Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    game_id = Column(Integer(), ForeignKey("game.id"), nullable=False)
    pict_left = Column(String(25), nullable=False)
    pict_right = Column(String(25), nullable=False)
    ok_left = Column(Boolean(), nullable=False)
    ok_right = Column(Boolean(), nullable=False)
    start_duration = Column(Integer(), nullable=False)  # duration from the beginning of the turn
    final_success = Column(Boolean(), nullable=True)
    final_reason = Column(String(10), nullable=True)  # if fail : timeout or wrong answer
    duration = Column(Integer(), nullable=True)  # duration of the turn


class RowAnswer(Base):
    __tablename__ = 'answer'
    id = Column(Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    turn_id = Column(Integer(), ForeignKey("turn.id"), nullable=False)
    response = Column(String(10), nullable=True)  # OK, FAIL, TIMEOUT
    duration = Column(Integer(), nullable=False)  # duration from the start of the turn


class Db:
    def __init__(self):
        self.engine = create_engine('sqlite:///' + DB_PATH + SQL_FILE)
        Base.metadata.bind = self.engine
        Base.metadata.create_all(self.engine)
        self.session = Session()
        self.connection = self.engine.connect()

        self.__game = None
        self.__row_game = None
        self.__turn = None
        self.__row_turn = None

    def sql(self, command):
        try:
            self.connection.execute(text(command))
            return True
        except Exception as e:
            print("Error:" + str(e))
            return False

    def __insert(self, elt):
        self.session.add(elt)
        self.session.commit()

    def start_game(self, game):
        self.__game = game
        strategy = game.strategy
        self.__row_game = RowGame(
            creation=datetime.now(),
            dog_name=strategy.get(ConfigKey.DOG_NAME),
            strategy=strategy.__class__.__name__,
            description=strategy.get_description(),
            images=len(strategy.images.images),
            turn_count=strategy.get(ConfigKey.TURN_COUNT),
            timeout=strategy.get(ConfigKey.TURN_DURATION),
            interval=strategy.get(ConfigKey.INTERVAL),
            fail_action=str(strategy.get(ConfigKey.FAIL_ACTION)),
            repeat_start=strategy.get(ConfigKey.REPEAT_START)
        )
        self.__insert(self.__row_game)

    def end_game(self):
        self.__game = None
        self.__row_game = None

    def start_turn(self, turn):
        if self.__game is None or self.__row_game is None:
            raise ValueError("start_turn with no game")
        self.__turn = turn
        self.__row_turn = RowTurn(
            game_id=self.__row_game.id,
            pict_left=turn.left.image.name,
            pict_right=turn.right.image.name,
            ok_left=turn.left.ok,
            ok_right=turn.right.ok,
            start_duration=(time.time() - self.__game.start)
        )
        self.__insert(self.__row_turn)

    def end_turn(self, ret):
        q = self.session.query(RowTurn)
        q = q.filter(RowTurn.id == self.__row_turn.id)
        turn = q.one()

        turn.final_success = ret.answer == Answer.OK
        turn.final_reason = str(ret.answer.name)
        turn.duration = ret.delta

        self.session.commit()
        self.__turn = None
        self.__row_turn = None

    def add_answer(self, response):
        if self.__turn is None or self.__row_turn is None:
            raise ValueError("add_answer with no turn")
        row_answer = RowAnswer(
            turn_id=self.__row_turn.id,
            response=str(response.answer.name),
            duration=response.delta
        )
        self.__insert(row_answer)
