from Python.PygameTest.FuchsUndJaeger.fuchsundjaeger import FuchsUndJaeger


def main():
    game = FuchsUndJaeger()
    game.new_game(2)
    while game.state == 'F' or game.state == 'J':
        game.board.print_board()
        if game.state == 'F':
            coord_val = int(input('Neue xy-Koordinate Fuchs: '))
            j_no = -1
        else:
            j_no = int(input('Nummer des Jägers (0-3): '))
            coord_val = int(input('Neue xy-Koordinate Jäger: '))
        if game.move(coord_val // 10, coord_val % 10, j_no):
            print('Zug erfolgreich.')
        else:
            print('Zug oder Eingabe ungültig. Nochmal.')
        print('===================')
    game.board.print_board()
    if game.state == 'WF':
        print('Fuchs gewinnt.')
    elif game.state == 'WJ':
        print('Jäger gewinnen.')


if __name__ == '__main__':
    main()
