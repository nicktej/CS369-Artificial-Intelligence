from copy import deepcopy


def diagram_to_state(diagram):
    """Converts a list of strings into a list of lists of characters (strings of length 1.)"""
    # TODO You have to write this
    return [list(a) for a in diagram]


INITIAL_STATE = diagram_to_state(['........',
                                  '........',
                                  '........',
                                  '...#O...',
                                  '...O#...',
                                  '........',
                                  '........',
                                  '........'])


def count_pieces(state):
    """Returns a dictionary of the counts of '#', 'O', and '.' in state."""
    # TODO You have to write this
    result = {'#': 0, 'O': 0, '.': 0}
    for row in state:
        for square in row:
            result[square] += 1
    return result


def prettify(state):
    """
    Returns a single human-readable string representing state, including row and column indices and counts of
    each color.
    """
    # TODO You have to write this
    result = ' 01234567\n'
    count = 0
    values = {'#': 0, 'O': 0, '.': 0}
    for row in state:
        result += str(count)
        for square in row:
            values[square] += 1
            result += str(square)
        result += str(count)
        result += '\n'
        count += 1
    result += ' 01234567\n'
    result += str(values)
    result += '\n'
    return result


def opposite(color):
    """opposite('#') returns 'O'. opposite('O') returns '#'."""
    # TODO You have to write this
    if color == '#':
        return 'O'
    if color == 'O':
        return '#'


def flips(state, r, c, color, dr, dc):
    """
    Returns a list of pieces that would be flipped if color played at r, c, but only searching along the line
    specified by dr and dc. For example, if dr is 1 and dc is -1, consider the line (r+1, c-1), (r+2, c-2), etc.

    :param state: The game state.
    :param r: The row of the piece to be  played.
    :param c: The column of the piece to be  played.
    :param color: The color that would play at r, c.
    :param dr: The amount to adjust r on each step along the line.
    :param dc: The amount to adjust c on each step along the line.
    :return A list of (r, c) pairs of pieces that would be flipped.
    """
    # TODO You have to write this
    if color == 'O':
        other = '#'
    if color == '#':
        other = 'O'
    flip = []
    counter = 0
    for xdirection, ydirection in [[dr, dc]]:
        x, y = r, c
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        if on_board(x, y) and state[x][y] == other:
            x += xdirection
            y += ydirection
            if not on_board(x, y):
                continue
            while state[x][y] == other:
                x += xdirection
                y += ydirection
                if not on_board(x, y):  # break out of while loop, then continue in for loop
                    break
            if not on_board(x, y):
                continue
            if state[x][y] == color:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == r and y == c:
                        break
                    flip.append((x, y))
                    counter += 1
    return flip


OFFSETS = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))


def flips_something(state, r, c, color):
    """Returns True if color playing at r, c in state would flip something."""
    # TODO You have to write this
    if color == 'O':
        other = '#'
    if color == '#':
        other = 'O'
    flip = []
    counter = 0
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = r, c
        x += xdirection  # first step in the direction
        y += ydirection  # first step in the direction
        if on_board(x, y) and state[x][y] == other:
            x += xdirection
            y += ydirection
            if not on_board(x, y):
                continue
            while state[x][y] == other:
                x += xdirection
                y += ydirection
                if not on_board(x, y):  # break out of while loop, then continue in for loop
                    break
            if not on_board(x, y):
                continue
            if state[x][y] == color:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == r and y == c:
                        break
                    flip.append([x, y])
                    counter += 1
    if len(flip) == 0:
        return False
    else:
        return True


def legal_moves(state, color):
    """
    Returns a list of legal moves ((r, c) pairs) that color can make from state. Note that a player must flip
    something if possible; otherwise they must play the special move 'pass'.
    """
    # TODO You have to write this
    get = []
    possible = []
    flag = 0
    ro = 0
    col = 0
    for row in state:
        for square in row:
            if square == color:
                get.append((ro, col))
            col += 1
        col = 0
        ro += 1
    if color == 'O':
        other = '#'
    elif color == '#':
        other = 'O'
    length = len(get)
    for i in range(length):
        cell = get[i]
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = cell[0], cell[1]
            flag = 0
            x += xdirection  # first step in the direction
            y += ydirection  # first step in the direction
            if on_board(x, y) and state[x][y] == other:
                x += xdirection
                y += ydirection
                if not on_board(x, y):
                    flag = 1
                    continue
                if state[x][y] == '.':
                    possible.append((x, y))
                    flag = 1
                    continue
                while state[x][y] == other or flag == 0 and on_board(x, y):
                    x += xdirection
                    y += ydirection
                    if on_board(x,y):
                        if state[x][y] == '.':
                            possible.append((x, y))
                            flag = 1
                            continue
                    if not on_board(x, y) or flag == 1:
                        break  # break out of while loop, then continue in for loop
    if len(possible) > 0:
        return possible
    else:
        return ['pass']


def successor(state, move, color):
    """
    Returns the state that would result from color playing move (which is either a pair (r, c) or 'pass'.
    Assumes move is legal.
    """
    # TODO You have to write this
    copy = deepcopy(state)
    if color == 'O':
        other = '#'
    if color == '#':
        other = 'O'
    if 'pass' in move:
        return state
    if 'pass' not in move:
        copy[move[0]][move[1]] = color
        flip = []
        counter = 0
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = move[0], move[1]
            x += xdirection  # first step in the direction
            y += ydirection  # first step in the direction
            if on_board(x, y) and copy[x][y] == other:
                x += xdirection
                y += ydirection
                if not on_board(x, y):
                    continue
                while copy[x][y] == other:
                    x += xdirection
                    y += ydirection
                    if not on_board(x, y):  # break out of while loop, then continue in for loop
                        break
                if not on_board(x, y):
                    continue
                if copy[x][y] == color:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == move[0] and y == move[1]:
                            break
                        flip.append([x, y])
                        counter += 1
        for i in range(0, counter):
            point = flip[i]
            x = point[0]
            y = point[1]
            copy[x][y] = color
        return copy


def on_board(x, y):
    # Returns True if the coordinates are located on the board.
    return 0 <= x <= 7 and 0 <= y <= 7


def score(state):
    """
    Returns the scores in state. More positive values (up to 64 for occupying the entire board) are better for '#'.
    More negative values (down to -64) are better for 'O'.
    """
    # TODO You have to write this
    values = {'#': 0, 'O': 0, '.': 0}
    for row in state:
        for square in row:
            values[square] += 1
    pound = values.get('#')
    circle = values.get('O')
    answer = pound - circle
    return answer


def game_over(state):
    """
    Returns true if neither player can flip anything.
    """
    # TODO You have to write this
    count = 0
    x = legal_moves(state, '#')
    y = legal_moves(state, 'O')
    if 'pass' not in x:
        count += 1
    if 'pass' not in y:
        count += 1
    if count > 0:
        return False
    else:
        return True



