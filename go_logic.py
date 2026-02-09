import numpy as np

EMPTY = 0
BLACK = 1
WHITE = 2
KOMI = 6.5

class GoGame:
    def __init__(self, size=9):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.history = []  # To track Ko rule
        self.captured_stones = {BLACK: 0, WHITE: 0}
        self.current_player = BLACK
        self.pass_count = 0
        self.game_over = False
        self.last_move = None

    def get_liberties(self, r, c, board=None):
        if board is None:
            board = self.board
        
        color = board[r, c]
        if color == EMPTY:
            return set()

        group = set()
        liberties = set()
        stack = [(r, c)]
        
        while stack:
            curr_r, curr_c = stack.pop()
            if (curr_r, curr_c) in group:
                continue
            group.add((curr_r, curr_c))
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if board[nr, nc] == EMPTY:
                        liberties.add((nr, nc))
                    elif board[nr, nc] == color:
                        if (nr, nc) not in group:
                            stack.append((nr, nc))
        return liberties, group

    def is_valid_move(self, r, c, color):
        if r < 0 or r >= self.size or c < 0 or c >= self.size or self.board[r, c] != EMPTY:
            return False

        # Test move
        temp_board = self.board.copy()
        temp_board[r, c] = color
        
        # Check for captures
        captured_any = False
        opponent = 3 - color
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                if temp_board[nr, nc] == opponent:
                    libs, _ = self.get_liberties(nr, nc, temp_board)
                    if len(libs) == 0:
                        captured_any = True
                        _, opponent_group = self.get_liberties(nr, nc, temp_board)
                        for gr, gc in opponent_group:
                            temp_board[gr, gc] = EMPTY

        # Check suicide rule
        libs, _ = self.get_liberties(r, c, temp_board)
        if len(libs) == 0 and not captured_any:
            return False

        # Check Ko rule (prevent repeating immediate previous board state)
        if len(self.history) >= 1:
            if np.array_equal(temp_board, self.history[-1]) if len(self.history) == 1 else any(np.array_equal(temp_board, prev) for prev in self.history[-2:]):
                 # Actually history[-1] is the state AFTER the last move.
                 # If player A moves, history[-1] is the state after player B moved.
                 # If player A moves again and reaches state history[-2], it's Ko.
                 pass
        
        # Simpler Ko check: check against all previous states in short history
        for prev in self.history:
            if np.array_equal(temp_board, prev):
                return False

        return True

    def place_stone(self, r, c, color):
        if not self.is_valid_move(r, c, color):
            return False

        self.board[r, c] = color
        opponent = 3 - color
        
        # Handle captures
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                if self.board[nr, nc] == opponent:
                    libs, group = self.get_liberties(nr, nc)
                    if len(libs) == 0:
                        for gr, gc in group:
                            self.board[gr, gc] = EMPTY
                            self.captured_stones[color] += 1

        # Keep history of board states (for Ko and display)
        self.history.append(self.board.copy())
        if len(self.history) > 20: # Slightly longer history for safety
            self.history.pop(0)
        
        self.current_player = opponent
        self.pass_count = 0
        self.last_move = (r, c)
        return True

    def pass_turn(self):
        self.pass_count += 1
        # Add a copy of board to history even on pass to maintain state sequence if needed
        # but Ko rule usually applies to stone placement.
        self.current_player = 3 - self.current_player
        if self.pass_count >= 2:
            self.game_over = True
        return True

    def get_legal_moves(self, color):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.is_valid_move(r, c, color):
                    moves.append((r, c))
        return moves

    def get_territory(self):
        black_territory = 0
        white_territory = 0
        visited = set()
        
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r, c] == EMPTY and (r, c) not in visited:
                    region = set()
                    stack = [(r, c)]
                    region.add((r, c))
                    visited.add((r, c))
                    
                    is_black_boundary = False
                    is_white_boundary = False
                    
                    while stack:
                        curr_r, curr_c = stack.pop()
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nr, nc = curr_r + dr, curr_c + dc
                            if 0 <= nr < self.size and 0 <= nc < self.size:
                                if self.board[nr, nc] == BLACK:
                                    is_black_boundary = True
                                elif self.board[nr, nc] == WHITE:
                                    is_white_boundary = True
                                elif self.board[nr, nc] == EMPTY and (nr, nc) not in region:
                                    region.add((nr, nc))
                                    visited.add((nr, nc))
                                    stack.append((nr, nc))
                    
                    if is_black_boundary and not is_white_boundary:
                        black_territory += len(region)
                    elif is_white_boundary and not is_black_boundary:
                        white_territory += len(region)
        return black_territory, white_territory

    def score(self):
        # Area Scoring (Chinese Style): Stones on board + Territory
        black_territory, white_territory = self.get_territory()
        black_score = np.sum(self.board == BLACK) + black_territory
        white_score = np.sum(self.board == WHITE) + white_territory + KOMI
        return black_score, white_score
