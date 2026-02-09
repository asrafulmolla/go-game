import math
from go_logic import BLACK, WHITE, EMPTY

class GoAI:
    def __init__(self, depth=2):
        self.depth = depth

    def evaluate(self, game):
        black_score, white_score = game.score()
        
        # Additional weights for liberties
        black_libs = 0
        white_libs = 0
        
        visited = set()
        for r in range(game.size):
            for c in range(game.size):
                if game.board[r, c] != EMPTY and (r, c) not in visited:
                    libs, group = game.get_liberties(r, c)
                    if game.board[r, c] == BLACK:
                        black_libs += len(libs)
                    else:
                        white_libs += len(libs)
                    visited.update(group)
        
        # Heuristic: Score difference + liberty difference
        score = (black_score - white_score) + 0.5 * (black_libs - white_libs)
        return score

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate(game), None

        color = BLACK if maximizing_player else WHITE
        legal_moves = game.get_legal_moves(color)
        
        if not legal_moves:
            return self.evaluate(game), None

        best_move = None
        if maximizing_player:
            max_eval = -math.inf
            for move in legal_moves:
                # Simulate move
                game_copy = self.clone_game(game)
                game_copy.place_stone(move[0], move[1], color)
                
                eval, _ = self.minimax(game_copy, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in legal_moves:
                game_copy = self.clone_game(game)
                game_copy.place_stone(move[0], move[1], color)
                
                eval, _ = self.minimax(game_copy, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def clone_game(self, game):
        import copy
        import numpy as np
        from go_logic import GoGame
        
        new_game = GoGame(game.size)
        new_game.board = game.board.copy()
        new_game.captured_stones = game.captured_stones.copy()
        new_game.current_player = game.current_player
        new_game.history = [h.copy() for h in game.history]
        new_game.last_move = game.last_move
        return new_game

    def get_best_move(self, game):
        is_black = (game.current_player == BLACK)
        _, move = self.minimax(game, self.depth, -math.inf, math.inf, is_black)
        return move
