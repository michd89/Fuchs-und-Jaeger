class PieceAlreadyPlacedException(Exception):
    pass


class PieceNotPlacedException(Exception):
    pass


class Piece:
    def __init__(self):
        self.pos_x = -1
        self.pos_y = -1


class Fuchs(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.value = 'F'


class Jaeger(Piece):
    def __init__(self, number):
        Piece.__init__(self)
        self.value = str(number)


class Chessboard:
    def __init__(self):
        self.squares = [['w' if (x + y) % 2 == 0 else 'b' for y in range(8)]
                        for x in range(8)]

    def place_piece(self, piece, x, y):
        if piece.pos_x != -1 and piece.pos_y != -1:
            raise PieceAlreadyPlacedException
        self.squares[x][y] = piece.value
        piece.pos_x = x
        piece.pos_y = y

    def remove_piece(self, piece):
        if piece.pos_x == -1 and piece.pos_y == -1:
            raise PieceNotPlacedException
        self.squares[piece.pos_x][piece.pos_y] = 'w' \
            if (piece.pos_x + piece.pos_y) % 2 == 0 else 'b'
        piece.pos_x = -1
        piece.pos_y = -1

    def move_piece(self, piece, x, y):
        self.remove_piece(piece)
        self.place_piece(piece, x, y)

    # Each horizontal row of squares is called a rank,
    # each vertical column of squares is called a file
    def print_board(self):
        print('# x 0 1 2 3 4 5 6 7')
        print('y + ---------------')
        for rank in range(len(self.squares)):
            print(str(rank) + ' | ', end='')
            for file in self.squares:
                print(file[rank] + ' ', end='')
            print()


# http://hrkll.ch/WordPress/lernen-durch-mitmachen/vorlaeufer/wolf-und-schafe/das-spiel
class FuchsUndJaeger:
    def __init__(self):
        self.board = Chessboard()
        self.fuchs = Fuchs()
        self.jaeger = [Jaeger(0), Jaeger(1), Jaeger(2), Jaeger(3)]
        # 'F' - Fuchs turn
        # 'J' - Jäger turn
        # 'WF' - Fuchs win
        # 'WJ' - Jäger win
        self.state = 'F'  # Fuchs begins

    # Fuchs can move in all directions
    def is_fuchs_move_valid(self, x, y):
        if 0 <= x <= 7 and 0 <= y <= 7:
            if abs(x - self.fuchs.pos_x) == 1 \
                    and abs(y - self.fuchs.pos_y) == 1 \
                    and self.board.squares[x][y] == 'b':
                return True
            else:
                return False
        else:
            return False

    # Jäger can move forward only (increasing y-coordinate)
    def is_jaeger_move_valid(self, x, y, j_no):
        if 0 <= x <= 7 and 0 <= y <= 7:
            if y - self.jaeger[j_no].pos_y == 1 and abs(
                    x - self.jaeger[j_no].pos_x) == 1 and \
                    self.board.squares[x][y] == 'b':
                return True
            else:
                return False
        else:
            return False

    # TODO: Reset
    def new_game(self, pos):
        try:
            for counter, jaeger in enumerate(self.jaeger):
                self.board.place_piece(jaeger, (counter * 2) + 1, 0)
            self.board.place_piece(self.fuchs, (pos * 2), 7)
            self.state = 'F'
        except PieceAlreadyPlacedException:
            pass

    def move(self, x, y, j_no=-1):
        if self.state == 'F':
            if self.is_fuchs_move_valid(x, y):
                self.board.move_piece(self.fuchs, x, y)

                # Check if Fuchs won (passed all Jäger or reached the end)
                if all([self.fuchs.pos_y <= self.jaeger[i].pos_y for i in
                        range(4)]):
                    self.state = 'WF'
                    return True
                else:
                    self.state = 'J'
                return True
            else:
                return False

        elif self.state == 'J':
            # Check for valid Jäger-number
            if not 0 <= j_no <= 3:
                return False
            if self.is_jaeger_move_valid(x, y, j_no):
                self.board.move_piece(self.jaeger[j_no], x, y)

                # Check if Jäger won (Fuchs became unable to move)
                if not (self.is_fuchs_move_valid(self.fuchs.pos_x + 1,
                                                 self.fuchs.pos_y + 1) \
                        or self.is_fuchs_move_valid(self.fuchs.pos_x + 1,
                                                    self.fuchs.pos_y - 1) \
                        or self.is_fuchs_move_valid(self.fuchs.pos_x - 1,
                                                    self.fuchs.pos_y + 1) \
                        or self.is_fuchs_move_valid(self.fuchs.pos_x - 1,
                                                    self.fuchs.pos_y - 1)):
                    self.state = 'WJ'
                    return True
                else:
                    self.state = 'F'
                return True
            else:
                return False

        # Game Over
        else:
            return False
