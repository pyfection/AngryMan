import random

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty

from basic_board import BasicBoard


class AI(EventDispatcher):
    board = ObjectProperty()


class Random(AI):
    def move(self, number):
        pieces = self.board.pieces[self.board.player]
        for piece in random.sample(pieces, len(pieces)):
            if piece in self.board.PATHS[self.board.player][:4]:
                continue
            if self.board.move_piece(piece, number):
                return piece


class MinMax(AI):
    def move(self, number):
        own_player = self.board.player
        board = BasicBoard(pieces={c: v.copy() for c, v in self.board.pieces.items()})
        self.minmax(own_player, board, 5)

    def minmax(self, own_player, board, itr):
        pass
