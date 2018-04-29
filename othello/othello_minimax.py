from othello_rules import *


def evaluate(state):
    """
    Returns 1 if '#' has won, -1 if 'O' has won, and 0 if the game has ended in a draw.
    If the game is not over, returns score / 100, giving a number from -0.64 to 0.64.
    This way, search will prefer winning to merely being ahead by any amount.
    """
    # TODO You have to write this
    result = {'#': 0, 'O': 0, '.': 0}
    for row in state:
        for square in row:
            result[square] += 1
    if result['.'] == 0:
        if result['#'] > result['O']:
            return 1
        elif result['#'] < result['O']:
            return -1
        else:
            return 1
    else:
        x = result['#']
        y = result['O']
        return (x - y) / 100


def minimax(state, player, max_depth):
    """
    Returns the value of state with player to play. max_depth gives the search depth; if 0, returns the evaluation
    of state.
    """
    # TODO You have to write this
    score = evaluate(state)
    if max_depth == 0:
        return score
    successors = (successor(state, move, player) for move in legal_moves(state, player))
    if max_depth > 0:
        max_depth -= 1
        if player == '#':
            return max(minimax(s, 'O', max_depth) for s in successors)
        else:
            return min(minimax(s, '#', max_depth) for s in successors)


def best_move(state, player, max_depth):
    """Returns player's best move. max_depth, which must be at least 1, gives the search depth."""
    # TODO You have to write this
    moves = legal_moves(state, player)
    if max_depth >= 1:
        if player == '#':
            return max(moves, key=lambda m: minimax(successor(state, m, player), 'O', max_depth-1))
        if player == 'O':
            return min(moves, key=lambda m: minimax(successor(state, m, player), '#', max_depth-1))


if __name__ == '__main__':
    game = INITIAL_STATE
    while not game_over(game):
        print('# to play')
        print(prettify(game))
        print('Thinking...')
        m = best_move(game, '#', 5)
        print(m)
        game = successor(game, m, '#')
        if not game_over(game):
            while True:
                print('O to play')
                print(prettify(game))
                m = input('Enter row and column (0-7, separated by a space) or pass: ')
                if m != 'pass':
                    m = tuple([int(n) for n in m.split()])
                print(m)
                if m in legal_moves(game, 'O'):
                    break
            game = successor(game, m, 'O')
    print(prettify(game))
    result = score(game)
    if result > 0:
        print('# wins!')
    elif result == 0:
        print('Draw.')
    else:
        print('O wins!')
