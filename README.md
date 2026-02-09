# Go Game with Minimax AI

A premium Go game implementation in Python using the Minimax algorithm with Alpha-Beta pruning.

## Features

- **Core Go Logic**: Liberty calculation, stone capture, and Ko rule enforcement.
- **AI Opponent**: Minimax algorithm with Alpha-Beta pruning for efficient decision making.
- **Modern GUI**: Built with Pygame, featuring a realistic wood-textured board and smooth gameplay.
- **Heuristic Evaluation**: The AI evaluates the board position based on material (stones on board), liberties, and captured stones.

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

Install dependencies using pip:

```bash
pip install pygame numpy
```

## How to Play

Run the main script:

```bash
python main.py
```

- **Player 1 (Black)**: Human (You)
- **Player 2 (White)**: AI (Minimax)

Click on the intersections of the board to place your stones. The goal is to surround more territory than your opponent and capture their stones.

## AI Details

The AI uses a depth-limited Minimax search. Due to the high branching factor of Go, the current implementation uses a 7x7 board and a depth of 2 to maintain responsiveness. Performance can be adjusted in `main.py` and `ai.py`.
