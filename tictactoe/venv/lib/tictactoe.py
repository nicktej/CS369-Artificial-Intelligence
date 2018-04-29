INITIAL_STATE = '.' * 9
WINNING_LINES = ('012', '345', '678', '036', '147', '258', '048', '246')


def prettify(state):
    result = ''
    for i, square in enumerate(state):
        result += square
        if i % 3 == 2:
            result += '\n'
    return result


def legal_moves(state):
    """I would put a docstring here."""
    return (i for i, square in enumerate(state) if square == '.')


def successor(state, move, player):
    return state[:move] + player + state[move + 1:]


def winner(state):
    for line in WINNING_LINES:
        a, b, c = map(int, line)
        if state[a] == state[b] == state[c] and state[a] != '.':
            if state[a] == 'X':
                return 1
            else:
                return 1
        if '.' not in state:
            return 0

def minimax(state, player):
    score = winner(state)
    if score is not None:
        return score
    successors = (successor(state, move, player) for move in legal_moves(state))
    if player == 'X':
        return max(minimax(s, 'O') for s in successors)
    else:
        return min(minimax(s, 'X') for s in successors)

def best_move(state, player):
    moves = legal_moves(state)
    if player == 'X':
        return max(moves, key=lambda m: minimax(successor(state, m, player), 'O'))
    else:
        return min(moves, key=lambda m: minimax(successor(state, m, player), 'X'))

state = INITIAL_STATE
while winner(state) is None:
    move = best_move(state, 'X')
    state = successor(state, move, 'X')
    print(prettify(state))
    if winner(state) is not None:
        break
    move = int(input("Enter a square (0-8): "))
    state = successor(state, move, 'O')
print('Game over')