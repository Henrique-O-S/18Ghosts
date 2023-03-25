import random
import math

from defines import *
from position import Position


def manhattan_distances(state):
    # returns the sum of manhattan distances from ghosts to their respective exits
    total = 0
    for ghost in state.ghosts:
        if ghost.player == state.currPlayer:
            if ghost.color == 'red' and state.currPlayer.colors_cleared.get('red') == 0:
                if state.board[RP_Y][RP_X].portal.direction == 0:
                    if ghost.index == Position(1, 0):
                        total += 5
                    elif ghost.index == Position(0, 0):
                        total += 6
                    else:
                        total += abs(ghost.index.x - RP_X + 1) + abs(ghost.index.y - RP_Y) + 1
                elif state.board[RP_Y][RP_X].portal.direction == 1:
                    if ghost.index == Position(1, 0):
                        total += 4
                    elif ghost.index == Position(0, 0):
                        total += 5
                    else:
                        total += abs(ghost.index.x - RP_X + 1) + abs(ghost.index.y - RP_Y)
                elif state.board[RP_Y][RP_X].portal.direction == 2:
                    total += abs(ghost.index.x - RP_X) + abs(ghost.index.y - RP_Y + 1)
                else:
                    if ghost.index == Position(3, 0):
                        total += 4
                    elif ghost.index == Position(4, 0):
                        total += 5
                    else:
                        total += abs(ghost.index.x - RP_X - 1) + abs(ghost.index.y - RP_Y)
            elif ghost.color == 'yellow' and state.currPlayer.colors_cleared.get('yellow') == 0:
                if state.board[YP_Y][YP_X].portal.direction == 0:
                    if ghost.index == Position(4, 3):
                        total += 4
                    elif ghost.index == Position(4, 4):
                        total += 5
                    else:
                        total += abs(ghost.index.x - YP_X) + abs(ghost.index.y - YP_Y - 1)
                elif state.board[YP_Y][YP_X].portal.direction == 1:
                    if ghost.index == Position(4, 1):
                        total += 5
                    elif ghost.index == Position(4, 0):
                        total += 6
                    else:
                        total += abs(ghost.index.x - YP_X) + abs(ghost.index.y - YP_Y + 1) + 1
                elif state.board[YP_Y][YP_X].portal.direction == 2:
                    if ghost.index == Position(4, 1):
                        total += 4
                    elif ghost.index == Position(4, 0):
                        total += 5
                    else:
                        total += abs(ghost.index.x - YP_X) + abs(ghost.index.y - YP_Y + 1)
                else:
                    total += abs(ghost.index.x - YP_X - 1) + abs(ghost.index.y - YP_Y)
            elif ghost.color == 'blue' and state.currPlayer.colors_cleared.get('blue') == 0:
                if state.board[BP_Y][BP_X].portal.direction == 0:
                    total += abs(ghost.index.x - BP_X) + abs(ghost.index.y - BP_Y - 1)
                elif state.board[BP_Y][BP_X].portal.direction == 1:
                    if ghost.index == Position(1, 4):
                        total += 4
                    elif ghost.index == Position(0, 4):
                        total += 5
                    else:
                        total += abs(ghost.index.x - BP_X + 1) + abs(ghost.index.y - BP_Y)
                elif state.board[BP_Y][BP_X].portal.direction == 2:
                    if ghost.index == Position(3, 4):
                        total += 5
                    elif ghost.index == Position(4, 4):
                        total += 6
                    else:
                        total += abs(ghost.index.x - BP_X - 1) + abs(ghost.index.y - BP_Y) + 1
                else:
                    if ghost.index == Position(3, 4):
                        total += 4
                    elif ghost.index == Position(4, 4):
                        total += 5
                    else:
                        total += abs(ghost.index.x - BP_X - 1) + abs(ghost.index.y - BP_Y)
    for ghost in state.dungeon.ghosts:
        if ghost.player == state.currPlayer:
            if ghost.color == 'red' and state.currPlayer.colors_cleared.get('red') == 0:
                total += 8
            elif ghost.color == 'yellow' and state.currPlayer.colors_cleared.get('yellow') == 0:
                total += 8
            elif ghost.color == 'blue' and state.currPlayer.colors_cleared.get('blue') == 0:
                total += 8
    return total

def evaluate(state):
    cost = 1
    if state.gameState == GameState.PICKING:
        return cost
    else:
        cost = manhattan_distances(state)
        for ghost in state.ghosts:
            if ghost.player != state.currPlayer:
                cost += 1
            #elif ghost.player == state.currPlayer:
                #cost += 1
                #if ghost.player.colors_cleared.get(ghost.color) == 0:
                    #for near_by_ghost in state.ghosts:
                        #if near_by_ghost.player != state.currPlayer and near_by_ghost.winsFight(ghost) and (ghost.index.x - 1 <= near_by_ghost.index.x <= ghost.index.x + 1 and ghost.index.y - 1 <= near_by_ghost.index.y <= ghost.index.y + 1) and (near_by_ghost.index.x != ghost.index.x and near_by_ghost.index.y != ghost.index.y):
                            #cost += 8
        for ghost in state.dungeon.ghosts:
            if ghost.player == state.currPlayer:
                cost += 1
    value = 1000 - cost
    return value

def execute_real_move(game, pos):
    if game.state.gameState == GameState.PLAYING:
        game.selectGhost(pos)
    elif game.state.gameState == GameState.PICKING:
        game.chooseGhostTile(pos)

def execute_random_move(game):
    if game.state.gameState == GameState.PLAYING:
        respawns = game.state.possibleRespawns()
        if respawns:
            id = random.choice(game.state.possibleRespawns())
            game.state = game.state.respawn(id)
            return
        playerGhosts = game.state.playerGhostIDs()
        if playerGhosts:
            id = random.choice(playerGhosts)
            moves = game.state.possibleMoves(game.state.ghosts[id])
            if moves:
                move = random.choice(moves)
                game.state = game.state.move(id, move)
                return
    elif game.state.gameState == GameState.PICKING:
        index = random.choice(game.state.possiblePlacements())
        game.state = game.state.place(index)

def execute_minimax_move(game, evaluate_func, depth):
    alpha = -100
    beta = 100
    maximizing = True  # The top-level call to minimax is always a maximization step
    best_value = -100
    best_state = None
    if game.state.gameState == GameState.PLAYING:
        #print("Respawn moves:")
        for id in game.state.possibleRespawns():
            new_state = game.state.respawn(id)
            new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_func)
            #print("Minimax result:")
            #print(new_value)
            #print("Direct heuristic result:")
            #print(evaluate(new_state))
            if new_value > best_value:
                best_value = new_value
                best_state = new_state
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        #print("Regular moves:")
        for id in range(len(game.state.ghosts)):
            if game.state.ghosts[id].player == game.state.currPlayer:
                for move in game.state.possibleMoves(game.state.ghosts[id]):
                    new_state = game.state.move(id, move)
                    new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_func)
                    #print("Minimax result:")
                    #print(new_value)
                    #print("Direct heuristic result:")
                    #print(evaluate(new_state))
                    if new_value > best_value:
                        best_value = new_value
                        best_state = new_state
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
    elif game.state.gameState == GameState.PICKING:
        #print("Picking moves:")
        for index in game.state.possiblePlacements():
            new_state = game.state.place(index)
            new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_func)
            #print("Minimax result:")
            #print(new_value)
            #print("Direct heuristic result:")
            #print(evaluate(new_state))
            if new_value > best_value:
                best_value = new_value
                best_state = new_state
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
    game.state = best_state
    #print("Best state:")
    #print(evaluate(best_state))

def minimax(state, depth, alpha, beta, maximizing, evaluate_func):
    # Base case: return the evaluation of the state if it's a leaf node or max depth is reached
    if depth == 0 or (state.gameState == GameState.PLAYING and state.checkWinner()):
        return evaluate_func(state)        
    # Initialize best_value based on whether we're maximizing or minimizing
    if maximizing:
        best_value = float('-inf')
    else:
        best_value = float('inf')
    # Iterate over all possible actions
    if state.gameState == GameState.PLAYING:
        for id in state.possibleRespawns():
            # Calculate the value of the resulting state after taking this action
            new_state = state.respawn(id)
            new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_func)
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
        for id in range(len(state.ghosts)):
            if state.ghosts[id].player == state.currPlayer:
                for move in state.possibleMoves(state.ghosts[id]):
                    # Calculate the value of the resulting state after taking this action
                    new_state = state.move(id, move)
                    new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_func)
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
    elif state.gameState == GameState.PICKING:
        for index in state.possiblePlacements():
            # Calculate the value of the resulting state after taking this action
            new_state = state.place(index)
            new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_func)
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
