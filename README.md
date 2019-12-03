# Fuchs und Jäger

Fuchs und Jäger (german for "Fox and Hunters", in english known as "Fox and Hounds", "Wolf and Sheep" etc.) is a game played e.g. on a chess board. The goal for the Fuchs (fox) is to break through the line of Jäger (hunters) while the Jägers' goal is catching the Fuchs.

## Prerequisites

* Python 3 interpreter
* [PyGame](https://www.pygame.org) for the graphics mode

## Rules

* A single Fuchs plays against four Jäger.  
* Both players place their piece(s) on their respective opposite end of the chess board, using squares of the same color only (this implementation uses the black squares).
* Both players move their pieces in a turn-based manner. The Fuchs gets the first move.
* The Fuchs can move diagonally in all four directions for one square.
* The Jäger can move diagonally at the (from their point of view) forward direction for one square.
* The Fuchs tries to reach the other end of the board and wins the game if all Jäger are passed.
* The Jäger win if they made the Fuchs unable to move (by encircling or trapping at the edge of the board).

## Usage

The game is started by executing one of the following scripts:
* `game_terminal.py` for playing the game in terminal mode.
* `game_pygame.py` for playing in the graphics mode. This requires the `PyGame` library.

## Copyright/Attribution Notice

* "Colorful Chess Pieces" by Brian Provan licensed CC-BY 3.0, GPL 2.0, or GPL 3.0: https://opengameart.org/content/colorful-chess-pieces