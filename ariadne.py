"""

Ariadne - Maze Generator

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

"""

import random


def main():
    #Width and height must be odd numbers to accomodate walls
    width = input("Please enter an odd number for the width >>> ")
    while not valid_input(width):
        width = input("Please enter an odd number for the width >>> ")
    height = input("Please enter an odd number for the height >>> ")
    while not valid_input(height):
        height = input("Please enter an odd number for the height >>> ")

    width = int(width)
    height = int(height)

    board = make_maze(width, height)

    draw_board(board, width, height)


def make_maze(width, height):
    #Initialize board with X for walls, and a unique number for floor tiles.
    board = []
    group_counter = 0
    for x in range(width):
        board.append([])
        for y in range(height):
            if is_perma_floor(x, y, width, height):
                board[x].append(str(group_counter))
                group_counter += 1
            else:
                board[x].append('X')

    #Gather potential connectors
    bag = []
    for x in range(width):
        for y in range(height):
            if is_connector(x, y, width, height):
                bag.append((x, y))


    #Loop through them
    while len(bag) > 0:
        #Pull a tuple containing x and y coordinates
        pull = bag[random.randrange(len(bag))]
        adjacents = get_adjacent_values(board, pull[0], pull[1], width, height)

        if adjacents_all_different_groups(adjacents):
            number_to_be = lowest_group_number(adjacents)
            board[pull[0]][pull[1]] = number_to_be

            change_tiles_recursively(board, pull[0], pull[1], width, height, number_to_be)

        bag.remove(pull)

    #When the bag is empty, we're done
    return board

def valid_input(text):
    #Validate whether input text is an odd number
    if not text.isdigit():
        return False
    if int(text) % 2 == 0:
        return False
    return True

def lowest_group_number(adjacents):
    #Get lowest group number, but return it as a string to keep values
    #of all the cells to be the same data type
    number = int(adjacents[0])

    for value in adjacents:
        if int(value) < number:
            number = int(value)

    return str(number)

def adjacents_all_different_groups(adjacents):
    #Compare all adjacents to see if they have the same group
    #Use this method because wall tiles aren't returned as adjacents,
    #so you don't necessarily know how many tiles you have in the list

    for first in range(len(adjacents)-1):
        for second in range(first+1, len(adjacents)):
            #Should always be a number, but cast to make sure
            if int(adjacents[first]) == int(adjacents[second]):
                return False
    return True

def get_adjacent_values(board, x, y, width, height):
    coordinates = get_adjacent_coordinates(board, x, y, width, height)

    result = []
    for coordinate in coordinates:
        if board[coordinate[0]][coordinate[1]].isdigit():
            result.append(board[coordinate[0]][coordinate[1]])

    return result

def get_adjacent_coordinates(board, x, y, width, height):
    #Return a list of tuples (x, y) of the coordinates of
    #the tiles adjacent to the given x and y. We don't have
    #to worry about edge tiles because we'll be checking for
    #tiles being walls later anyway, and edge tiles will always
    #be walls.
    result = []
    if x-1 >= 0:
        result.append((x-1, y))
    if x+1 < width:
        result.append((x+1, y))
    if y-1 >= 0:
        result.append((x, y-1))
    if y+1 < height:
        result.append((x, y+1))
    return result

def change_tiles_recursively(board, x, y, width, height, number_to_be):
    adjacents = get_adjacent_coordinates(board, x, y, width, height)

    #Check to see if adjacent tile is already the number to be. If it isn't and also isn't a wall,
    #change it to the new number and continue propogating changes.
    for coordinate in adjacents:
        if board[coordinate[0]][coordinate[1]] != number_to_be and board[coordinate[0]][coordinate[1]].isdigit():
            board[coordinate[0]][coordinate[1]] = number_to_be
            change_tiles_recursively(board, coordinate[0], coordinate[1], width, height, number_to_be)

def is_connector(x, y, width, height):
    if is_perma_wall(x, y, width, height):
        return False
    if is_perma_floor(x, y, width, height):
        return False
    return True

def is_edge(x, y, width, height):
    return x == 0 or y == 0 or x == width-1 or y == height-1

def is_perma_wall(x, y, width, height):
    #If tile is even on both dimensions, it must stay a wall
    return (x % 2 == 0 and y % 2 == 0) or is_edge(x, y, width, height)

def is_perma_floor(x, y, width, height):
    #If tile is odd on both dimensions it is already a floor
    return x % 2 == 1 and y % 2 == 1 and not is_edge(x, y, width, height)

def draw_board(board, width, height):
    output = "\n\n"

    #Loop y before x in order to make sure the width dimension matches up visually
    #with the width on the screen instead of the width and height getting visually swapped.
    for y in range(height):
        line = ""
        for x in range(width):
            #Take advantage of the fact that we keep the lowest group number
            #at each merge, meaning at the end of the generation, all floor
            #tiles will have a value of 0. Use that to make it prettier.
            if board[x][y] == '0':
                line += '  '
            else:
                line += board[x][y] + ' '
        output += line + "\n"

    print(output)


if __name__ == "__main__":
    main()