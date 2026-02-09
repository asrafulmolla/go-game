import pygame
import sys
from go_logic import GoGame, BLACK, WHITE, EMPTY
from ai import GoAI

# Constants
BOARD_SIZE = 7
CELL_SIZE = 60
MARGIN = 60
GRID_SIZE = (BOARD_SIZE - 1) * CELL_SIZE
WINDOW_WIDTH = GRID_SIZE + 2 * MARGIN
WINDOW_HEIGHT = WINDOW_WIDTH + 150

# Colors
WOOD_COLOR = (210, 166, 121)
WOOD_DARK = (180, 140, 100)
LINE_COLOR = (45, 34, 22)
BLACK_STONE = (30, 30, 30)
WHITE_STONE = (245, 245, 245)
ACCENT_COLOR = (70, 50, 40)
TEXT_COLOR = (45, 34, 22)
BUTTON_COLOR = (139, 69, 19)
BUTTON_HOVER = (160, 82, 45)

class GoGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Go AI - Minimax Master")
        self.clock = pygame.time.Clock()
        self.game = GoGame(BOARD_SIZE)
        self.ai = GoAI(depth=2)
        try:
            self.font = pygame.font.SysFont("Segoe UI", 24, bold=True)
            self.small_font = pygame.font.SysFont("Segoe UI", 18)
        except:
            self.font = pygame.font.SysFont("Arial", 24, bold=True)
            self.small_font = pygame.font.SysFont("Arial", 18)
        self.running = True

    def draw_button(self, text, x, y, w, h, hover=False):
        color = BUTTON_HOVER if hover else BUTTON_COLOR
        pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=8)
        pygame.draw.rect(self.screen, LINE_COLOR, (x, y, w, h), 2, border_radius=8)
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(x + w/2, y + h/2))
        self.screen.blit(text_surf, text_rect)

    def draw_board(self):
        # Draw background shadow
        pygame.draw.rect(self.screen, WOOD_DARK, (MARGIN-10, MARGIN-10, GRID_SIZE+20, GRID_SIZE+20), border_radius=4)
        pygame.draw.rect(self.screen, WOOD_COLOR, (MARGIN-5, MARGIN-5, GRID_SIZE+10, GRID_SIZE+10))
        
        # Draw grid
        for i in range(BOARD_SIZE):
            pygame.draw.line(self.screen, LINE_COLOR, 
                             (MARGIN, MARGIN + i * CELL_SIZE), 
                             (MARGIN + GRID_SIZE, MARGIN + i * CELL_SIZE), 2)
            pygame.draw.line(self.screen, LINE_COLOR, 
                             (MARGIN + i * CELL_SIZE, MARGIN), 
                             (MARGIN + i * CELL_SIZE, MARGIN + GRID_SIZE), 2)

        # Draw hover ghost stone
        if not self.game.game_over and self.game.current_player == BLACK:
            mouse_pos = pygame.mouse.get_pos()
            cell = self.get_cell_from_pos(mouse_pos)
            if cell and self.game.board[cell[0], cell[1]] == EMPTY:
                pos = (MARGIN + cell[1] * CELL_SIZE, MARGIN + cell[0] * CELL_SIZE)
                ghost_color = (0, 0, 0, 100) if self.game.current_player == BLACK else (255, 255, 255, 100)
                # Draw translucent circle
                s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(s, ghost_color, (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE // 2 - 4)
                self.screen.blit(s, (pos[0] - CELL_SIZE//2, pos[1] - CELL_SIZE//2))

        # Draw stones
        last_move_pos = None
        if self.game.history:
            # Check most recent board difference to find last move
            pass # We could also modify GoGame to store last_move
            
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                state = self.game.board[r, c]
                if state != EMPTY:
                    pos = (MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE)
                    # Shadow
                    pygame.draw.circle(self.screen, (0, 0, 0, 30), (pos[0]+2, pos[1]+2), CELL_SIZE // 2 - 4)
                    
                    color = BLACK_STONE if state == BLACK else WHITE_STONE
                    pygame.draw.circle(self.screen, color, pos, CELL_SIZE // 2 - 4)
                    if state == WHITE:
                        pygame.draw.circle(self.screen, LINE_COLOR, pos, CELL_SIZE // 2 - 4, 1)
                    
                    # Last move indicator
                    if hasattr(self.game, 'last_move') and self.game.last_move == (r, c):
                        indicator_color = (255, 0, 0)
                        pygame.draw.circle(self.screen, indicator_color, pos, 4)

    def draw_ui(self):
        # Score Panel
        black_score, white_score = self.game.score()
        
        panel_y = WINDOW_WIDTH + 20
        pygame.draw.rect(self.screen, (240, 230, 210), (MARGIN, panel_y, GRID_SIZE, 100), border_radius=10)
        pygame.draw.rect(self.screen, LINE_COLOR, (MARGIN, panel_y, GRID_SIZE, 100), 2, border_radius=10)

        # Current Turn
        turn_text = "BLACK'S TURN (YOU)" if self.game.current_player == BLACK else "WHITE'S TURN (AI)"
        if self.game.game_over:
            winner = "Black wins!" if black_score > white_score else "White wins!"
            turn_text = f"GAME OVER - {winner}"
        
        turn_surf = self.font.render(turn_text, True, TEXT_COLOR)
        self.screen.blit(turn_surf, (MARGIN + 20, panel_y + 15))

        # Scores
        score_surf = self.small_font.render(f"Black: {black_score}  |  White: {white_score} (incl. 6.5 Komi)", True, ACCENT_COLOR)
        self.screen.blit(score_surf, (MARGIN + 20, panel_y + 55))

        # Pass Button
        mouse_pos = pygame.mouse.get_pos()
        btn_x, btn_y, btn_w, btn_h = WINDOW_WIDTH - MARGIN - 100, panel_y + 25, 100, 50
        hover = btn_x <= mouse_pos[0] <= btn_x + btn_w and btn_y <= mouse_pos[1] <= btn_y + btn_h
        self.draw_button("PASS", btn_x, btn_y, btn_w, btn_h, hover)
        return (btn_x, btn_y, btn_w, btn_h)

    def get_cell_from_pos(self, pos):
        x, y = pos
        # Adjust for margin and cell size
        c = round((x - MARGIN) / CELL_SIZE)
        r = round((y - MARGIN) / CELL_SIZE)
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            # Check if distance to intersection is small enough
            target_x = MARGIN + c * CELL_SIZE
            target_y = MARGIN + r * CELL_SIZE
            dist = ((x - target_x)**2 + (y - target_y)**2)**0.5
            if dist < CELL_SIZE // 2:
                return r, c
        return None

    def main_loop(self):
        pass_btn_rect = (0, 0, 0, 0)
        while self.running:
            self.screen.fill((255, 253, 245)) # Off-white background
            
            # AI Turn
            if not self.game.game_over and self.game.current_player == WHITE:
                pygame.display.set_caption("AI is thinking...")
                move = self.ai.get_best_move(self.game)
                if move:
                    self.game.place_stone(move[0], move[1], WHITE)
                else:
                    self.game.pass_turn()
                pygame.display.set_caption("Go AI - Minimax Master")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if not self.game.game_over and event.type == pygame.MOUSEBUTTONDOWN and self.game.current_player == BLACK:
                    # Check pass button
                    bx, by, bw, bh = pass_btn_rect
                    if bx <= event.pos[0] <= bx + bw and by <= event.pos[1] <= by + bh:
                        self.game.pass_turn()
                    else:
                        cell = self.get_cell_from_pos(event.pos)
                        if cell:
                            self.game.place_stone(cell[0], cell[1], BLACK)

            self.draw_board()
            pass_btn_rect = self.draw_ui()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gui = GoGUI()
    gui.main_loop()
