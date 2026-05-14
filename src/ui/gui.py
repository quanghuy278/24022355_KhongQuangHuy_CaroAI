# src/ui/gui.py
import pygame
import sys
from config import BOARD_SIZE, PLAYER_X, PLAYER_O, EMPTY, BG_COLOR, GRID_COLOR, X_COLOR, O_COLOR, TEXT_COLOR

CELL_SIZE = 50
MARGIN = 50
WIDTH = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * MARGIN + 100 # Chừa chỗ cho text

class GUI:
    def __init__(self, game):
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro AI - Minimax & Alpha-Beta")
        self.font = pygame.font.SysFont("arial", 24)
        self.large_font = pygame.font.SysFont("arial", 32, bold=True)
        self.restart_rect = None
        
    def draw_board(self):
        self.screen.fill(BG_COLOR)
        
        # Vẽ lưới
        for i in range(BOARD_SIZE + 1):
            # Đường dọc
            pygame.draw.line(self.screen, GRID_COLOR, 
                             (MARGIN + i * CELL_SIZE, MARGIN), 
                             (MARGIN + i * CELL_SIZE, MARGIN + BOARD_SIZE * CELL_SIZE), 2)
            # Đường ngang
            pygame.draw.line(self.screen, GRID_COLOR, 
                             (MARGIN, MARGIN + i * CELL_SIZE), 
                             (MARGIN + BOARD_SIZE * CELL_SIZE, MARGIN + i * CELL_SIZE), 2)
                             
        # Vẽ các quân cờ
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.game.board.grid[r][c] == PLAYER_X:
                    self.draw_x(r, c)
                elif self.game.board.grid[r][c] == PLAYER_O:
                    self.draw_o(r, c)
                    
        # Vẽ thông báo
        status_y = HEIGHT - 80
        if self.game.is_game_over:
            if self.game.winner == PLAYER_X:
                msg = "Ket qua: NGUOI CHOI (X) THANG!"
                color = X_COLOR
            elif self.game.winner == PLAYER_O:
                msg = "Ket qua: MAY (O) THANG!"
                color = O_COLOR
            else:
                msg = "Ket qua: HOA (DRAW)!"
                color = TEXT_COLOR
                
            text = self.large_font.render(msg, True, color)
            
            # Vẽ nút Chơi Lại
            btn_text = self.font.render(" CHOI LAI ", True, (255, 255, 255))
            btn_w = btn_text.get_width() + 40
            btn_h = btn_text.get_height() + 20
            btn_x = WIDTH//2 - btn_w//2
            btn_y = status_y + 40
            
            self.restart_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            
            # Vẽ nền nút màu xanh lá đậm
            pygame.draw.rect(self.screen, (40, 160, 40), self.restart_rect, border_radius=8)
            # Vẽ viền nút
            pygame.draw.rect(self.screen, (20, 100, 20), self.restart_rect, 2, border_radius=8)
            
            # Căn giữa chữ trong nút
            text_x = btn_x + (btn_w - btn_text.get_width()) // 2
            text_y = btn_y + (btn_h - btn_text.get_height()) // 2
            self.screen.blit(btn_text, (text_x, text_y))
        else:
            if self.game.current_player == PLAYER_X:
                turn_str = "Luot cua: Nguoi choi (X)"
            else:
                turn_str = "Luot cua: AI (O) dang suy nghi..."
                
            text = self.font.render(turn_str, True, TEXT_COLOR)
            
            if self.game.last_ai_time > 0:
                stats = self.font.render(f"AI: {self.game.last_ai_time:.0f}ms | Duyet: {self.game.last_ai_nodes} nodes", True, TEXT_COLOR)
                self.screen.blit(stats, (MARGIN, status_y + 30))
                
        self.screen.blit(text, (WIDTH//2 - text.get_width()//2, status_y))
        pygame.display.flip()
        
    def draw_x(self, row, col):
        center_x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        center_y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        offset = CELL_SIZE // 4
        pygame.draw.line(self.screen, X_COLOR, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 4)
        pygame.draw.line(self.screen, X_COLOR, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 4)
        
    def draw_o(self, row, col):
        center_x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        center_y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 3
        pygame.draw.circle(self.screen, O_COLOR, (center_x, center_y), radius, 4)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Nếu game đã kết thúc, kiểm tra xem click vào nút chơi lại không
                if self.game.is_game_over:
                    if self.restart_rect and self.restart_rect.collidepoint(x, y):
                        self.game.reset()
                
                # Nếu game chưa kết thúc và đang là lượt người chơi
                elif not self.game.is_game_over and self.game.current_player == PLAYER_X:
                    if MARGIN <= x <= MARGIN + BOARD_SIZE * CELL_SIZE and MARGIN <= y <= MARGIN + BOARD_SIZE * CELL_SIZE:
                        col = (x - MARGIN) // CELL_SIZE
                        row = (y - MARGIN) // CELL_SIZE
                        self.game.handle_human_move(row, col)
