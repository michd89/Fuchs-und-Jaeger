import pygame

from fuchsundjaeger import FuchsUndJaeger

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class PieceType(object):
    def __init__(self, piece, start_x, start_y):
        self.rect = pygame.rect.Rect(start_x, start_y, 64, 64)
        self.piece = piece


class PieceSet:
    def __init__(self):
        self.image = pygame.image.load('chess.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(768 / 2), int(1536 / 2)))
        self.piece_tile_list = list()

    def add_piece_tile(self, piece, start_x, start_y):
        self.piece_tile_list.append(PieceType(piece, start_x, start_y))

    def get_piece_tile(self, num):
        return self.piece_tile_list(num)

    def get_piece_tiles(self):
        for piece in self.piece_tile_list:
            yield piece


def init_pieceset(game):
    pieces = PieceSet()
    pieces.add_piece_tile(game.fuchs, 64, 128)
    pieces.add_piece_tile(game.jaeger[0], 0, 64)
    pieces.add_piece_tile(game.jaeger[1], 0, 64)
    pieces.add_piece_tile(game.jaeger[2], 0, 64)
    pieces.add_piece_tile(game.jaeger[3], 0, 64)
    return pieces


def draw_chessboard(screen, game, font):
    # Board border
    pygame.draw.rect(screen, (102, 153, 153), (100, 100, 406, 406), 5)
    # Chess fields
    for x in range(len(game.board.squares)):
        for y in range(len(game.board.squares[x])):
            color = WHITE if (x + y) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (103 + 50 * x, 103 + 50 * y, 50, 50), 0)
    # Coordinate labels
    for i, letter in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        text = font.render(letter, True, WHITE)
        screen.blit(text, (122 + i * 50, 520))
        text = pygame.transform.rotate(text, 180)
        screen.blit(text, (122 + i * 50, 60))
    for i, letter in enumerate(['8', '7', '6', '5', '4', '3', '2', '1', ]):
        text = font.render(letter, True, WHITE)
        screen.blit(text, (70, 117 + i * 50))
        text = pygame.transform.rotate(text, 180)
        screen.blit(text, (520, 117 + i * 50))


def get_tile_start(pos_x, pos_y):
    return 96 + 50 * pos_x, 96 + 50 * pos_y


def draw_pieces(screen, pieceset):
    for piece_tile in pieceset.get_piece_tiles():
        piece_tile_start = get_tile_start(piece_tile.piece.pos_x, piece_tile.piece.pos_y)
        screen.blit(pieceset.image, piece_tile_start, piece_tile.rect)


def get_clicked_piece(pieceset, x, y):
    for piece_tile in pieceset.get_piece_tiles():
        if piece_tile.piece.pos_x == x and piece_tile.piece.pos_y == y:
            return piece_tile.piece
    return None


def handle_click(square_rects, selected_square, target_square):
    for x, i in zip(square_rects, range(8)):
        for y, j in zip(x, range(8)):
            if y.collidepoint(pygame.mouse.get_pos()):  # Clicked at square (i, j)
                if not selected_square:
                    return (i, j), target_square
                else:
                    return selected_square, (i, j)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Fuchs und Jäger")
    font = pygame.font.SysFont('Courier New', 20, False, False)
    done = False

    # Initializations
    game = FuchsUndJaeger()
    game.new_game(2)
    square_rects = [
        [pygame.Rect((103 + 50 * x, 103 + 50 * y), (50, 50)) for y in range(8)] for x in range(8)]
    selected_square = None
    target_square = None
    pieceset = init_pieceset(game)

    while not done:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break

            # Don't accept any more input if the game is over
            # TODO: Restart
            if game.state == 'WF' or game.state == 'WJ':
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selected_square, target_square = \
                    handle_click(square_rects, selected_square, target_square)

        # Game logic
        if selected_square:
            if target_square and (selected_square != target_square):
                j_no = -1  # Fuchs always uses -1 as j_no
                if game.state == 'J':
                    # TODO: Optimize moving Jaeger (or moving in general)
                    for x, i in zip(square_rects, range(8)):
                        for _, _ in zip(x, range(8)):
                            for jaeger, jaeger_no in zip(game.jaeger, range(4)):
                                if (jaeger.pos_x, jaeger.pos_y) == selected_square:
                                    j_no = jaeger_no
                game.move(target_square[0], target_square[1], j_no)
                selected_square = target_square = None

        # Clear (new) frame
        screen.fill((30, 30, 30))

        # Render graphics
        draw_chessboard(screen, game, font)
        draw_pieces(screen, pieceset)
        if selected_square:
            pygame.draw.rect(screen, (0, 200, 0), (
            103 + 50 * selected_square[0], 103 + 50 * selected_square[1], 50, 50), 4)
        if game.state == 'F':
            state = 'Turn Fuchs'
        elif game.state == 'J':
            state = 'Turn Jäger'
        elif game.state == 'WF':
            state = 'Fuchs wins'
        else:
            state = 'Jäger wins'
        text = font.render(state, True, WHITE)
        screen.blit(text, (20, 20))

        # Update display
        pygame.display.flip()

        # Limit frame rate
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
