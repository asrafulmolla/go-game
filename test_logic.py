from go_logic import GoGame, BLACK, WHITE
from ai import GoAI

def test_ai_move():
    game = GoGame(5)
    ai = GoAI(depth=2)
    
    print("Placing Black stone at (2, 2)")
    game.place_stone(2, 2, BLACK)
    
    print("AI (White) is thinking...")
    move = ai.get_best_move(game)
    print(f"AI chose move: {move}")
    
    if move:
        game.place_stone(move[0], move[1], WHITE)
        print("Board state after AI move:")
        print(game.board)
    else:
        print("AI found no legal moves!")

if __name__ == "__main__":
    test_ai_move()
