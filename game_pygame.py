import pygame

from fuchsundjaeger import FuchsUndJaeger


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Fuchs und Jäger")
    done = False

    # Init stuff
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    game = FuchsUndJaeger()
    game.board.print_board()
    testbild = pygame.image.load('chess.png').convert_alpha()
    testbild = pygame.transform.scale(testbild, (int(768/2), int(1536/2)))
    font = pygame.font.SysFont('Courier New', 20, False, False)

    while not done:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Game logic
        # ...

        # Clear (new) frame
        screen.fill((30, 30, 30))

        # Render graphics
        # Board border
        pygame.draw.rect(screen, (102, 153, 153), (100, 100, 406, 406), 5)
        # Chess fields
        for x in range(len(game.board.squares)):
            for y in range(len(game.board.squares[x])):
                color = BLACK if game.board.squares[x][y] == 'b' else WHITE
                pygame.draw.rect(screen, color, (103+50*x, 103+50*y, 50, 50), 0)
        # Coordinate labels
        for i, letter in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            text = font.render(letter, True, WHITE)
            screen.blit(text, (122+i*50, 520))
            text = pygame.transform.rotate(text, 180)
            screen.blit(text, (122+i*50, 60))
        for i, letter in enumerate(['8', '7', '6', '5', '4', '3', '2', '1', ]):
            text = font.render(letter, True, WHITE)
            screen.blit(text, (70, 117+i*50))
            text = pygame.transform.rotate(text, 180)
            screen.blit(text, (520, 117+i*50))


        # Test
        # screen.blit(testbild, [100, 100])

        # Update display
        pygame.display.flip()

        # Limit frame rate
        clock.tick(60)

        # game.board.print_board()

    pygame.quit()


if __name__ == '__main__':
    main()
