import random

from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.properties import OptionProperty
from kivy.clock import Clock

from basic_board import BasicBoard
from ai import Random as RandomAI


FPS = 1 / 10


class Board(GridLayout, BasicBoard):
    texture = Image(source="board.png").texture
    player = OptionProperty("yellow", options=BasicBoard.COLORS)

    def __init__(self, **kwargs):
        BasicBoard.__init__(self)
        super().__init__(cols=11, **kwargs)
        self.texture.mag_filter = "nearest"
        self.ai = RandomAI(board=self)
        self.images = {}

        for y in range(self.cols):
            for x in range(self.cols):
                img = Image(allow_stretch=True, source='none.png')
                img.texture.mag_filter = "nearest"
                self.add_widget(img)
                self.images[(x, y)] = img

        self.reset()
        self.move_schedule = Clock.schedule_interval(lambda dt: self.make_turn(), FPS)

    def reset(self):
        for pieces in self.pieces.values():
            for x, y in pieces:
                self.images[(x, y)].source = 'none.png'
            pieces.clear()

        for color, path in self.PATHS.items():
            self.pieces[color].clear()
            for x, y in path[:4]:
                self.images[(x, y)].source = f"{color}.png"
                self.pieces[color].append((x, y))

    def finish(self):
        super().finish()
        self.move_schedule.cancel()
