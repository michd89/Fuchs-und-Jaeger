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

        # Update display
        pygame.display.flip()

        # Limit frame rate
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
