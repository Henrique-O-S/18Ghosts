import random
import math
from copy import deepcopy

import numpy as np

from state import State
from defines import *
from position import Position

def manhattan_distances(state):
    # returns the sum of manhattan distances from ghosts to their respective exits
    total = 0
    for ghost in state.ghosts:
        if ghost.index is not None:
            if ghost.player == state.currPlayer:
                if ghost.color == 'red' and state.currPlayer.colors_cleared.get('red') == 0:
                    if state.board[RP_Y][RP_X].portal.direction == 0:
                        if ghost.index == Position(1, 0):
                            total += 5
                        elif ghost.index == Position(0, 0):
                            total += 6
                        else:
                            total += abs(ghost.index.x - (RP_X + 1)) + abs(ghost.index.y - RP_Y) + 1
                    elif state.board[RP_Y][RP_X].portal.direction == 1:
                        if ghost.index == Position(1, 0):
                            total += 4
                        elif ghost.index == Position(0, 0):
                            total += 5
                        else:
                            total += abs(ghost.index.x - (RP_X + 1)) + abs(ghost.index.y - RP_Y)
                    elif state.board[RP_Y][RP_X].portal.direction == 2:
                        total += abs(ghost.index.x - RP_X) + abs(ghost.index.y - (RP_Y + 1))
                    else:
                        if ghost.index == Position(3, 0):
                            total += 4
                        elif ghost.index == Position(4, 0):
                            total += 5
                        else:
                            total += abs(ghost.index.x - (RP_X - 1)) + abs(ghost.index.y - RP_Y)
                elif ghost.color == 'yellow' and state.currPlayer.colors_cleared.get('yellow') == 0:
                    if state.board[YP_Y][YP_X].portal.direction == 0:
                        if ghost.index == Position(4, 3):
                            total += 4
                        elif ghost.index == Position(4, 4):
                            total += 5
                        else:
                            total += abs(ghost.index.x - YP_X) + abs(ghost.index.y - (YP_Y - 1))
                    elif state.board[YP_Y][YP_X].portal.direction == 1:
                        if ghost.index == Position(4, 1):
                            total += 5
                        elif ghost.index == Position(4, 0):
                            total += 6
                        else:
                            total += abs(ghost.index.x - YP_X) + abs(ghost.index.y - (YP_Y + 1)) + 1
                    elif state.board[YP_Y][YP_X].portal.direction == 2:
                        if ghost.index == Position(4, 1):
                            total += 4
                        elif ghost.index == Position(4, 0):
                            total += 5
                        else:
                            total += abs(ghost.index.x - YP_X) + abs(ghost.index.y - (YP_Y + 1))
                    else:
                        total += abs(ghost.index.x - (YP_X - 1)) + abs(ghost.index.y - YP_Y)
                elif ghost.color == 'blue' and state.currPlayer.colors_cleared.get('blue') == 0:
                    if state.board[BP_Y][BP_X].portal.direction == 0:
                        total += abs(ghost.index.x - BP_X) + abs(ghost.index.y - (BP_Y - 1))
                    elif state.board[BP_Y][BP_X].portal.direction == 1:
                        if ghost.index == Position(1, 4):
                            total += 4
                        elif ghost.index == Position(0, 4):
                            total += 5
                        else:
                            total += abs(ghost.index.x - (BP_X + 1)) + abs(ghost.index.y - BP_Y)
                    elif state.board[BP_Y][BP_X].portal.direction == 2:
                        if ghost.index == Position(3, 4):
                            total += 5
                        elif ghost.index == Position(4, 4):
                            total += 6
                        else:
                            total += abs(ghost.index.x - (BP_X - 1)) + abs(ghost.index.y - BP_Y) + 1
                    else:
                        if ghost.index == Position(3, 4):
                            total += 4
                        elif ghost.index == Position(4, 4):
                            total += 5
                        else:
                            total += abs(ghost.index.x - (BP_X - 1)) + abs(ghost.index.y - BP_Y)
    for ghost in state.dungeon.ghosts:
        if ghost.player == state.currPlayer:
            if ghost.color == 'red' and state.currPlayer.colors_cleared.get('red') == 0:
                total += 8
            elif ghost.color == 'yellow' and state.currPlayer.colors_cleared.get('yellow') == 0:
                total += 8
            elif ghost.color == 'blue' and state.currPlayer.colors_cleared.get('blue') == 0:
                total += 8
    return total

def evaluate_easy(state):
    cost = manhattan_distances(state)

    value = 1000 - cost
    return value

def evaluate_medium(state):
    cost = manhattan_distances(state)

    if state.currPlayer == state.player1:
        if state.player2.colors_cleared.get('red') != 0:
            cost += 4
        if state.player2.colors_cleared.get('yellow') != 0:
            cost += 4
        if state.player2.colors_cleared.get('blue') != 0:
            cost += 4
    elif state.currPlayer == state.player2:
        if state.player2.colors_cleared.get('red') != 0:
            cost += 4
        if state.player2.colors_cleared.get('yellow') != 0:
            cost += 4
        if state.player2.colors_cleared.get('blue') != 0:
            cost += 4

    value = 1000 - cost
    return value

def evaluate_hard(state):
    cost = manhattan_distances(state)

    for ghost in state.ghosts:
        if ghost.player != state.currPlayer:
            cost += 1

    if state.currPlayer == state.player1:
        if state.player2.colors_cleared.get('red') != 0:
            cost += 4
        if state.player2.colors_cleared.get('yellow') != 0:
            cost += 4
        if state.player2.colors_cleared.get('blue') != 0:
            cost += 4
    elif state.currPlayer == state.player2:
        if state.player2.colors_cleared.get('red') != 0:
            cost += 4
        if state.player2.colors_cleared.get('yellow') != 0:
            cost += 4
        if state.player2.colors_cleared.get('blue') != 0:
            cost += 4

    value = 1000 - cost
    return value


'''
def evaluate(state):
    if state.gameState == GameState.PICKING:
        return 0
    p1 = [i for i in range(len(state.ghosts)) if state.ghosts[i].player.name == "Player 1"]
    p2 = [i for i in range(len(state.ghosts)) if state.ghosts[i].player.name == "Player 2"]
    if state.currPlayer.name == "Player 1":
        return len(p2) - len(p1)
    else:
        return len(p1) - len(p2)
'''

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

def execute_minimax_move(game, evaluate_hard_func, depth):
    alpha = -10000
    beta = 10000
    maximizing = True  # The top-level call to minimax is always a maximization step
    best_value = -10000
    best_state = None
    if game.state.gameState == GameState.PLAYING:
        for id in game.state.possibleRespawns():
            new_state = game.state.respawn(id)
            new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_hard_func)
            if new_value > best_value:
                best_value = new_value
                best_state = new_state
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        for id in range(len(game.state.ghosts)):
            if game.state.ghosts[id].player == game.state.currPlayer:
                for move in game.state.possibleMoves(game.state.ghosts[id]):
                    new_state = game.state.move(id, move)
                    new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_hard_func)
                    if new_value > best_value:
                        best_value = new_value
                        best_state = new_state
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
    elif game.state.gameState == GameState.PICKING:
        for index in game.state.possiblePlacements():
            new_state = game.state.place(index)
            new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_hard_func)
            if new_value > best_value:
                best_value = new_value
                best_state = new_state
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
    game.state = best_state
def minimax(state, depth, alpha, beta, maximizing, evaluate_hard_func):
    # Base case: return the evaluation of the state if it's a leaf node or max depth is reached
    if depth == 0 or (state.gameState == GameState.OVER):
        return evaluate_hard_func(state)
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
            new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_hard_func)
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
                    new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_hard_func)
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
            new_value = minimax(new_state, depth - 1, alpha, beta, not maximizing, evaluate_hard_func)
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


def UCB1(state):
    if state.n == 0:
        return float('inf')
    return state.t / state.n + 2 * math.sqrt(np.log(state.parent.n) / state.n)


def treeTransversal(game, root):
    selectedState = root
    if game.state.gameState == GameState.PICKING:
        while game.state.gameState == GameState.PICKING and selectedState.children != []:
            selectedState = max(selectedState.children, key=UCB1)
        return selectedState
    elif game.state.gameState == GameState.PLAYING:
        while game.state.gameState == GameState.PLAYING and selectedState.children != []:
            selectedState = max(selectedState.children, key=UCB1)
        return selectedState

def simulation(game, evaluate_func):
    if game.state.gameState == GameState.PICKING:
        while game.state.gameState == GameState.PICKING:
            execute_random_move(game)
        return evaluate_func(game.state)
    elif game.state.gameState == GameState.PLAYING:
        player = game.state.currPlayer
        while game.state.gameState == GameState.PLAYING:
            curr_state = game.state
            execute_random_move(game)
            next_state = game.state
            if next_state.player1 == player:
                if sum(map(lambda x : next_state.player1.colors_cleared[x] > 0, next_state.player1.colors_cleared)) > sum(map(lambda x : curr_state.player1.colors_cleared[x] > 0, curr_state.player1.colors_cleared)):
                    break
            else:
                if sum(map(lambda x : next_state.player2.colors_cleared[x] > 0, next_state.player2.colors_cleared)) > sum(map(lambda x : curr_state.player2.colors_cleared[x] > 0, curr_state.player2.colors_cleared)):
                    break

        return evaluate_func(game.state)
def rollout(state, value):
    while True:

        state.n += 1
        state.t += value
        if state.parent:
            state = state.parent
        else:
            break

def expandNode(game):
    children = set()
    if game.state.gameState == GameState.PLAYING:
        playerGhosts = game.state.playerGhostIDs()
        for id in playerGhosts:
            for move in game.state.possibleMoves(game.state.ghosts[id]):
                new_state = game.state.move(id, move)
                game.state.addChild(new_state)
                children.add(new_state)
        for id in game.state.possibleRespawns():
            new_state = game.state.respawn(id)
            game.state.addChild(new_state)
            children.add(new_state)

    elif game.state.gameState == GameState.PICKING:
        for index in game.state.possiblePlacements():
            new_state = game.state.place(index)
            children.add(new_state)
            game.state.addChild(new_state)
    game.state.children = children


def mcts(game, evaluate_func, nIterations):
    root = game.state
    expandNode(game)
    for i in range(nIterations):
        game.state = treeTransversal(game, root)
        if game.state.n == 0:
            a = game.state
            if game.state.gameState == root.gameState:
                rollout(game.state, simulation(game, evaluate_func))
            game.state = a

        else:
            a = game.state
            expandNode(game)
            game.state = a
            game.state = treeTransversal(game, root)
            a = game.state
            if game.state.gameState == root.gameState:
                rollout(game.state, simulation(game, evaluate_func))
            game.state = a
    selectedState = max(root.children, key=UCB1)
    game.state = selectedState
