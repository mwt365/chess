import chess
import random

# chess is a 2 player game
NUM_AGENTS = 2

def minimax(board, max_plies=5, curr_depth=0,
        alpha=float("-inf"), beta=float("inf")):
    """ Performs minimax search through board up to max_plies
    Uses alpha-beta pruning

    Keyword arguments:
    board      -- the current state of the game (required)
    max_plies  -- the number of plies to descend before evaluating
                  state (default 5)
    curr_depth -- parameter to keep track of how deep we are (default 0)
    alpha      -- alpha parameter for pruning (default -inf)
    beta       -- beta parameter for pruning (default inf)
    """

    max_depth = max_plies * NUM_AGENTS

    if curr_depth >= max_depth or board.is_game_over():
        return (evaluation_function(board), None)

    curr_agent = curr_depth % NUM_AGENTS

    legal_actions = list(board.legal_moves)

    best_action = None
    v = 0

    if curr_agent == 0:
        # maximizing layer
        v = float("-inf")

        for i in range(len(legal_actions)):
            action = legal_actions[i]

            # simulate the move to pass to children
            successor = board.copy()
            successor.push(action)

            successor_val = minimax(successor, max_plies, curr_depth + 1,
                    alpha, beta)[0]

            if successor_val > v:
                best_action = action
                v = successor_val

            # beta pruning case, stop considering branch
            # return value doesn't matter; we won't be using it
            if v > beta:
                return (v, best_action)

            alpha = max(alpha, v)

    else:
        # minimizing layer
        v = float("inf")

        for i in range(len(legal_actions)):
            action = legal_actions[i]
            successor = board.copy()
            successor.push(action)

            successor_val = minimax(successor, max_plies, curr_depth + 1,
                    alpha, beta)[0]

            if successor_val < v:
                best_action = action
                v = successor_val

            # alpha pruning case, stop considering branch
            # return value doesn't matter; we won't be using it
            if v < alpha:
                return (v, best_action)

            beta = min(beta, v)

    # return most optimized child along with action to take
    return (v, best_action)

def evaluation_function(board):
    """
    Counts number of pieces white has more than black and also whether
    white or black has won the game
    """

    # will be replaced later by better evaluation function

    white_won = 1 if board.result() == '1-0' else 0
    black_won = 1 if board.result() == '0-1' else 0

    pieces = [ board.piece_at(x) for x in chess.SQUARES ]
    white_material = [ piece for piece in pieces if piece == chess.WHITE ]
    black_material = [ piece for piece in pieces if piece == chess.BLACK ]

    return (white_won * 100) + len(white_material) - len(black_material)
