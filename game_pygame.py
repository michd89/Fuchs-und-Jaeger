import pygame

from fuchsundjaeger import FuchsUndJaeger

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

peice_size = 64
tile_size = 50

border_start_x = 100
border_start_y = 100
border_width = 406
border_height = 406
border_thickness = 6  # May cause display errors if odd

tiles_start_x = int(border_start_x + border_thickness / 2)
tiles_start_y = int(border_start_y + border_thickness / 2)

letter_width = 12  # Estimated, to put every letter roughly at the middle
# letter_height = ???
text_distance = 10  # Distance of text from board


class PieceType(object):
    def __init__(self, piece, start_x, start_y):
        self.rect = pygame.rect.Rect(start_x, start_y, peice_size, peice_size)
        self.piece = piece


class PieceSet:
    def __init__(self):
        self.image = pygame.image.load('chess.png').convert_alpha()
        image_width = 768
        image_height = 1536
        imace_scale = 0.5
        self.image = pygame.transform.scale(self.image,
                                            (int(image_width * imace_scale),
                                             int(image_height * imace_scale))
                                            )
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
    pieces.add_piece_tile(game.fuchs, peice_size, peice_size * 2)  # In chess.png the knight is to the right of the pawn
    pieces.add_piece_tile(game.jaeger[0], 0, peice_size)
    pieces.add_piece_tile(game.jaeger[1], 0, peice_size)
    pieces.add_piece_tile(game.jaeger[2], 0, peice_size)
    pieces.add_piece_tile(game.jaeger[3], 0, peice_size)
    return pieces


def draw_chessboard(screen, game, font):
    # Board border
    border_color = (102, 153, 153)
    pygame.draw.rect(screen, border_color,
                     (border_start_x, border_start_y, border_width, border_height), border_thickness)
    # Chess fields
    for x in range(len(game.board.squares)):
        for y in range(len(game.board.squares[x])):
            color = WHITE if (x + y) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (tiles_start_x + tile_size * x, tiles_start_y + tile_size * y,
                                             tile_size, tile_size), 0)
    # Coordinate labels
    letters_x = tiles_start_x + int(tile_size / 2) - int(letter_width / 2)
    # Maybe it looks more even when rather the text height considered
    letters_y_upper = tiles_start_y - border_thickness * 2 - letter_width - text_distance
    letters_y_lower = tiles_start_y + tile_size * 8 + border_thickness + text_distance
    for i, letter in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        text = font.render(letter, True, WHITE)
        screen.blit(text, (letters_x + i * tile_size, letters_y_lower))
        text = pygame.transform.rotate(text, 180)
        screen.blit(text, (letters_x + i * tile_size, letters_y_upper))

    numbers_y = tiles_start_y + int(tile_size / 2) - letter_width
    numbers_x_left = tiles_start_x - border_thickness - letter_width - text_distance
    numbers_x_right = tiles_start_x + tile_size * 8 + border_thickness + text_distance
    for i, letter in enumerate(['8', '7', '6', '5', '4', '3', '2', '1']):
        text = font.render(letter, True, WHITE)
        screen.blit(text, (numbers_x_left, numbers_y + i * tile_size))
        text = pygame.transform.rotate(text, 180)
        screen.blit(text, (numbers_x_right, numbers_y + i * tile_size))


def get_tile_start(pos_x, pos_y):
    offset_x = tiles_start_x - border_thickness - 1  # Put more in the middle with minus one
    offset_y = tiles_start_y - border_thickness - 1  # Put more in the middle with minus one
    return offset_x + tile_size * pos_x, offset_y + tile_size * pos_y


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
        [pygame.Rect((tiles_start_x + tile_size * x, tiles_start_y + tile_size * y), (tile_size, tile_size))
         for y in range(8)] for x in range(8)]
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
            pygame.draw.rect(screen,
                             (0, 200, 0),
                             (tiles_start_x + tile_size * selected_square[0],
                              tiles_start_y + tile_size * selected_square[1],
                              tile_size,
                              tile_size),
                             border_thickness)
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
