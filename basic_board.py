import random


path = [
    (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0), (5, 0),
    (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (10, 5),
    (10, 6), (9, 6), (8, 6), (7, 6), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (5, 10),
    (4, 10), (4, 9), (4, 8), (4, 7), (4, 6), (3, 6), (2, 6), (1, 6), (0, 6), (0, 5),
]


class BasicBoard:
    COLORS = ("yellow", "green", "red", "black")
    player = COLORS[0]
    PATHS = {
        "yellow": [(0, 1), (1, 1), (0, 0), (1, 0)] + path + [(1, 5), (2, 5), (3, 5), (4, 5)],
        "green": [(9, 1), (10, 1), (9, 0), (10, 0)] + path[10:] + path[:10] + [(5, 1), (5, 2), (5, 3), (5, 4)],
        "red": [(9, 10), (10, 10), (9, 9), (10, 9)] + path[20:] + path[:20] + [(9, 5), (8, 5), (7, 5), (6, 5)],
        "black": [(0, 10), (1, 10), (0, 9), (1, 9)] + path[30:] + path[:30] + [(5, 9), (5, 8), (5, 7), (5, 6)],
    }

    def __init__(self, pieces=None):
        self.pieces = pieces or {
            "yellow": [],
            "green": [],
            "red": [],
            "black": [],
        }

    def finish(self):
        print("All players reached home")

    @property
    def enemy_pieces(self):
        return [p for color, sublist in self.pieces.items() for p in sublist if color != self.player]

    @property
    def next_player(self):
        i = (self.COLORS.index(self.player) + 1) % len(self.COLORS)
        for color in self.COLORS[i:] + self.COLORS[:i]:
            if set(self.pieces[color]) != set(self.PATHS[color][-4:]):
                return color

    def make_turn(self):
        self.move()
        color = self.next_player
        if color:
            self.player = color
        else:
            self.finish()

    def move(self):
        number = random.randint(1, 6)
        if number == 6:
            piece = self.leave_house()
            if not piece:
                piece = self.ai.move(number)
            self.move()
        else:
            piece = self.ai.move(number)

        if piece:
            for color, pieces in self.pieces.items():
                if color == self.player:
                    continue
                try:
                    i = pieces.index(piece)
                except ValueError:
                    pass
                else:
                    self.throw_enemy(color, pieces[i])

    def leave_house(self):
        pieces = self.pieces[self.player]
        start_location = self.PATHS[self.player][4]
        piece = next((p for p in pieces if p in self.PATHS[self.player][:4]), None)
        if piece and start_location not in pieces:
            pieces[pieces.index(piece)] = start_location
            self.images[piece].source = 'none.png'
            self.images[start_location].source = f'{self.player}.png'
        return piece

    def move_piece(self, piece, number):
        pieces = self.pieces[self.player]
        i = self.PATHS[self.player].index(piece)
        try:
            x, y = self.PATHS[self.player][i + number]
        except IndexError:
            return
        if (x, y) in pieces:
            return
        pieces[pieces.index(piece)] = x, y
        self.images[piece].source = 'none.png'
        self.images[(x, y)].source = f'{self.player}.png'
        return piece

    def throw_enemy(self, enemy, piece):
        i = self.pieces[enemy].index(piece)
        self.pieces[enemy][i] = pos = next(pos for pos in self.PATHS[enemy][:4] if pos not in self.pieces[enemy])
        self.images[pos].source = f'{enemy}.png'
