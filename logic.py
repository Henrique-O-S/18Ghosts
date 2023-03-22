import random

from defines import *
from state import State
from game import Game
from position import Position

def manhattan_distances(state : State):
    # returns the sum of manhattan distances from ghosts to their respective exits
    board = state.board
    total = 0
    for ghost in state.ghosts:
        if ghost.player == state.currPlayer:
            if ghost.color == 'red' and state.currPlayer.colors_cleared.get('red') == 0:
                if state.board[RP_Y][RP_X].portal.direction == 0:
                    total += abs(ghost.index.x - state.board[RP_Y][RP_X].index.x + 1) + abs(ghost.index.y - state.board[RP_Y][RP_X].index.y)
                elif state.board[RP_Y][RP_X].portal.direction == 1:
                    total += abs(ghost.index.x - state.board[RP_Y][RP_X].index.x + 1) + abs(ghost.index.y - state.board[RP_Y][RP_X].index.y)
                elif state.board[RP_Y][RP_X].portal.direction == 2:
                    total += abs(ghost.index.x - state.board[RP_Y][RP_X].index.x) + abs(ghost.index.y - state.board[RP_Y][RP_X].index.y + 1)
                else:
                    total += abs(ghost.index.x - state.board[RP_Y][RP_X].index.x - 1) + abs(ghost.index.y - state.board[RP_Y][RP_X].index.y)
            elif ghost.color == 'yellow' and state.currPlayer.colors_cleared.get('yellow') == 0:
                if state.board[YP_Y][YP_X].portal.direction == 0:
                    total += abs(ghost.index.x - state.board[YP_Y][YP_X].index.x) + abs(ghost.index.y - state.board[YP_Y][YP_X].index.y - 1)
                elif state.board[YP_Y][YP_X].portal.direction == 1:
                    total += abs(ghost.index.x - state.board[YP_Y][YP_X].index.x) + abs(ghost.index.y - state.board[YP_Y][YP_X].index.y + 1)
                elif state.board[YP_Y][YP_X].portal.direction == 2:
                    total += abs(ghost.index.x - state.board[YP_Y][YP_X].index.x) + abs(ghost.index.y - state.board[YP_Y][YP_X].index.y + 1)
                else:
                    total += abs(ghost.index.x - state.board[YP_Y][YP_X].index.x - 1) + abs(ghost.index.y - state.board[YP_Y][YP_X].index.y)
            elif ghost.color == 'blue' and state.currPlayer.colors_cleared.get('blue') == 0:
                if state.board[BP_Y][BP_X].portal.direction == 0:
                    total += abs(ghost.index.x - state.board[BP_Y][BP_X].index.x) + abs(ghost.index.y - state.board[BP_Y][BP_X].index.y - 1)
                elif state.board[BP_Y][BP_X].portal.direction == 1:
                    total += abs(ghost.index.x - state.board[BP_Y][BP_X].index.x + 1) + abs(ghost.index.y - state.board[BP_Y][BP_X].index.y)
                elif state.board[BP_Y][BP_X].portal.direction == 2:
                    total += abs(ghost.index.x - state.board[BP_Y][BP_X].index.x - 1) + abs(ghost.index.y - state.board[BP_Y][BP_X].index.y)
                else:
                    total += abs(ghost.index.x - state.board[BP_Y][BP_X].index.x - 1) + abs(ghost.index.y - state.board[BP_Y][BP_X].index.y)
    for ghost in state.dungeon.ghosts:
        if ghost.player == state.currPlayer:
            if ghost.color == 'red' and state.currPlayer.colors_cleared.get('red') == 0:
                total += 8
            elif ghost.color == 'yellow' and state.currPlayer.colors_cleared.get('yellow') == 0:
                total += 8
            elif ghost.color == 'blue' and state.currPlayer.colors_cleared.get('blue') == 0:
                total += 8
    return total

def play_evaluation(state : State):
    cost = state.manhattan_distances(state, state.currPlayer)
    for ghost in state.ghosts:
        if ghost.player != state.currPlayer:
            cost += 1
        elif ghost.player == state.currPlayer:
            cost += 1
            if ghost.player.colors_cleared.get(ghost.color) == 0:
                for near_by_ghost in state.ghosts:
                    if near_by_ghost.player != state.currPlayer and near_by_ghost.winsFight(ghost) and (ghost.index.x - 1 <= near_by_ghost.index.x <= ghost.index.x + 1 and ghost.index.y - 1 <= near_by_ghost.index.y <= ghost.index.y + 1) and (near_by_ghost.index.x != ghost.index.x and near_by_ghost.index.y != ghost.index.y):
                        cost += 8
    for ghost in state.dungeon.ghosts:
        if ghost.player == state.currPlayer:
            cost += 1
    return cost

def execute_real_move(game : Game, pos : Position):
    if game.state.gameState == GameState.PLAYING:
        game.selectGhost(pos)
    elif game.state.gameState == GameState.PICKING:
        game.chooseGhostTile(pos)

def execute_random_move(game : Game):
    if game.state.gameState == GameState.PLAYING:
        id = random.choice(game.state.playerGhostIDs())
        move = random.choice(game.state.possibleMoves(game.state.ghosts[id]))
        game.state = game.state.move(id, move)
    elif game.state.gameState == GameState.PICKING:
        index = random.choice(game.state.possiblePlacements())
        game.state = game.state.place(index)

def execute_minimax_move(evaluate_func, depth):
    return True

def minimax(state : State, depth, alpha, beta, maximizing, player, evaluate_func):
    # Base case: return the evaluation of the state if it's a leaf node or max depth is reached
    if depth == 0 or is_leaf_node(state):
        return evaluate_func(state, player)        
    # Initialize best_value based on whether we're maximizing or minimizing
    if maximizing:
        best_value = float('-inf')
    else:
        best_value = float('inf')
    # Iterate over all possible actions
    for action in get_possible_actions(state):
        # Calculate the value of the resulting state after taking this action
        new_state = apply_action(state, action)
        new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, player, evaluate_func)
        # Update best_value and alpha/beta based on whether we're maximizing or minimizing
        if maximizing:
            best_value = max(best_value, new_value)
            alpha = max(alpha, best_value)
        else:
            best_value = min(best_value, new_value)
            beta = min(beta, best_value)
        # Alpha-beta pruning: if alpha >= beta, prune the rest of the subtree
        if alpha >= beta:
            break
    return best_value

def is_leaf_node(state):
    return True

def get_possible_actions(state):
    return state

def apply_action(state, action):
    return state
