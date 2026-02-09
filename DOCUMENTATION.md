# Go Game: Technical Documentation & Execution Flow

This document explains the internal working mechanism of the Go Game, detailing how the Human (Black) and AI (White) interact, and which functions are triggered in each iteration.

---

## 1. System Architecture

The project is divided into three core modules:

1.  **`main.py` (GUI & Controller):** Handles Pygame rendering, mouse inputs, and the main game loop.
2.  **`go_logic.py` (Rule Engine):** Manages the board state, validates moves, handles stone captures, and calculates scores.
3.  **`ai.py` (Intelligence):** Implements the Minimax algorithm with Alpha-Beta pruning to decide the AI's moves.

---

## 2. The Move Lifecycle (Step-by-Step)

### A. Human Turn (Black)

1.  **Input Detection:** The `main_loop` in `main.py` constantly listens for events. When you click the board, `pygame.MOUSEBUTTONDOWN` is triggered.
2.  **Coordinate Mapping:** The function `get_cell_from_pos(event.pos)` converts your pixel click (e.g., 250, 300) into a board grid coordinate (e.g., Row 4, Col 5).
3.  **Placement Request:** `self.game.place_stone(r, c, BLACK)` is called in `go_logic.py`.
    - **Validation:** It first calls `is_valid_move()`. This checks:
      - Is the spot empty?
      - **Suicide Rule:** Would placing this stone leave it with 0 liberties (and not capture anything)?
      - **Ko Rule:** Does this move repeat a previous board state?
    - **Executing Move:** If valid, the board is updated: `self.board[r, c] = BLACK`.
    - **Capture Check:** It looks at the 4 neighboring stones (Up, Down, Left, Right). If an opponent's group has 0 liberties (checked via `get_liberties()`), those stones are removed from the board.
    - **Turn Switch:** `self.current_player` is set to `WHITE`.

### B. AI Turn (White)

1.  **Turn Detection:** The `main_loop` sees `current_player == WHITE`.
2.  **Think Phase:** `ai.get_best_move(self.game)` is called in `ai.py`.
3.  **Search (Minimax):**
    - The AI looks ahead (Depth 2). It simulates every possible legal move.
    - **`clone_game()`:** For every simulation, it creates a virtual copy of the board so it doesn't mess up the real game.
    - **`evaluate()`:** For each simulated board, it calculates a score based on:
      - Stones on board + Territory.
      - **Liberties:** How "safe" or "breathable" its groups are.
    - **Alpha-Beta Pruning:** It ignores "bad" paths early to save processing time.
4.  **Action:** The AI returns the coordinate with the highest score.
5.  **Execution:** `self.game.place_stone(r, c, WHITE)` is called (using the same logic as the human turn).
6.  **Turn Switch:** `self.current_player` is set back to `BLACK`.

---

## 3. Key Functions Reference

### `go_logic.py`

| Function                   | Role                                                                                            |
| :------------------------- | :---------------------------------------------------------------------------------------------- |
| `get_liberties(r, c)`      | Uses a Stack-based Flood Fill to find all empty points (liberties) around a group of stones.    |
| `place_stone(r, c, color)` | The "Master" function for making a move. Orchestrates validation, capture, and turn management. |
| `is_valid_move(...)`       | The "Referee". Enforces Go rules (Ko, Suicide, Overlap).                                        |
| `get_territory()`          | Scans the board to see which empty areas are completely surrounded by one color.                |
| `score()`                  | Returns the final score: `Stones + Territory + Komi (6.5 for White)`.                           |

### `ai.py`

| Function           | Role                                                                                               |
| :----------------- | :------------------------------------------------------------------------------------------------- |
| `minimax(...)`     | Recursive function that builds a "tree" of possible future moves.                                  |
| `evaluate(game)`   | The "Judge". Decides if a board position is "Good" or "Bad" for the AI.                            |
| `clone_game(game)` | Essential for safety; allows the AI to "dream" about moves without changing the actual game board. |

### `main.py`

| Function       | Role                                                                         |
| :------------- | :--------------------------------------------------------------------------- |
| `draw_board()` | Renders the wood texture, grid lines, stones, and the "Last Move" indicator. |
| `main_loop()`  | The "Heartbeat". Runs at 30 FPS, checking for input and updating the UI.     |

---

## 4. Logical Flow Summary

`User Clicks` -> `main.py (GUI)` -> `go_logic.py (Rules)` -> `Capture/Score Update` -> `ai.py (Thinking)` -> `go_logic.py (AI Move)` -> `UI Update`.
