# mazegenerator

Ariadne - Maze Generator

Generates random mazes of arbitrary sizes

The way the maze generator works is to start with a grid that has
an odd number of rows and columns. Evern cell starts as a wall:


X X X X X

X X X X X

X X X X X

X X X X X

X X X X X


The defining characteristic of a maze is that there is one and only
one possible path between any two points in the maze. That means that
once two cells have a path between them, you can't add another path
between them or it breaks the rules of what a maze is. To take advantage
of that fact, we make every cell that is in both an even row and an
even column a floor tile, and assign it a unique group number:


X X X X X

X 1 X 2 X

X X X X X

X 3 X 4 X

X X X X X


Now we take the set of walls that are connecting the groups (the set of
tiles that have either an even row OR an even column, but not both and
also are not on the edge of the map) and randomly select one of them to
turn into a floor tile (O in the diagram below):


X X X X X

X 1 O 2 X

X X X X X

X 3 X 4 X

X X X X X


After selecting that tile, we check the adjacent tiles (not diagonals),
to see which group those tiles belong to. So long as no two adjacent floor
tiles share the same group, it is okay to connect those two groups. When
we connect the groups, we take the lowest of the two or more group numbers
that are being connected (it really doesn't matter what group number, but
using the lowest is a clean way of deciding) and recursively apply it to
all of the floor tiles that are connected to our newly made floor tile.
We then remove the wall we changed from our list of potential walls because
it isn't a wall anymore:


X X X X X

X 1 1 1 X

X X X X X

X 3 X 4 X

X X X X X


Now we repeat the process:


X X X X X

X 1 1 1 X

X X X O X

X 3 X 4 X

X X X X X


->


X X X X X

X 1 1 1 X

X X X 1 X

X 3 X 1 X

X X X X X


And repeat again:


X X X X X

X 1 1 1 X

X O X 1 X

X 3 X 1 X

X X X X X


->


X X X X X

X 1 1 1 X

X 1 X 1 X

X 1 X 1 X

X X X X X


And repeat again, but this time the wall we randomly select has two of
the same group number that it would be connecting if we were to turn it
into a floor tile:


X X X X X

X 1 1 1 X

X 1 X 1 X

X 1 O 1 X

X X X X X


If we turn the selected tile into a floor, we would end up with a closed
loop. Mazes, by definition, cannot have closed loops since there must be
one and only one path between any two tiles in the maze. Since we can't
turn this tile into a floor, we simply remove it from the list of potential
walls to change. Since we've also removed all of the walls that we already
changed, that leaves our list of potential walls to change empty, which means
that we are done.


TLDR: Every cell with (odd, odd) coordinates will always remain a wall. Every
tile that is on the edge of the board will always remain a wall. Every cell
with (even, even) coordinates will always be a floor, and starts with a unique
group number. Every cell with (even, odd) or (odd, even) coordinates that is
NOT on the edge of the board, is a potential connector that may end up as a
wall OR may end up as a connecting floor between our starter floor tiles.

Throw all potential connectors into a bag and randomly pull out one at a time.
If the pulled potential connector connects two floor tiles with the same group
number, throw it away and pull another. If the pulled connector does NOT connect
any two floor tiles with the same group number, turn it into a floor and change
all connected tiles to have the same group number. Then discard the tile from
the bag of potential connectors. When the bag is empty, there should be only one
group of connected floor tiles that every floor tile belongs to, and removing
any additional walls would result in either a closed loop or the border wall
around the edge of the board being opened. Done.
