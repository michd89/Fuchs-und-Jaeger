# Fuchs und Jäger

Fuchs und Jäger (german for "Fox and Hunters", in english known as "Fox and Hounds", "Wolf and Sheep" etc.) is a game played e.g. on a chess board. The goal for the Fuchs (fox) is to break through the line of Jäger (hunters) while the Jägers' goal is catching the Fuchs.

## Prerequisites

By now a Python 3 interpreter is needed. A future version might include a graphical interface using the PyGame library.

## Rules

* A single Fuchs plays against four Jäger.  
* Both players place their piece(s) on their respective opposite end of the chess board, using squares of the same color only (this implementation uses the black squares).
* Both players move their pieces in a turn-based manner. The Fuchs gets the first move.
* The Fuchs can move diagonally in all four directions for one square.
* The Jäger can move diagonally at the (from their point of view) forward direction for one square.
* The Fuchs tries to reach the other end of the board and wins the game if all Jäger are passed.
* The Jäger win if they made the Fuchs unable to move (by encircling or trapping at the edge of the board).
