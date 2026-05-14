# src/ui/gui.py
import pygame
import sys
import config
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
        self.algo_rect = None
        self.state = "MENU" # "MENU" or "PLAYING"
        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        
        # Các nút của màn hình Menu
        btn_w, btn_h = 300, 60
        self.menu_minimax_rect = pygame.Rect(WIDTH//2 - btn_w//2, HEIGHT//2 - 40, btn_w, btn_h)
        self.menu_alphabeta_rect = pygame.Rect(WIDTH//2 - btn_w//2, HEIGHT//2 + 40, btn_w, btn_h)

    def draw(self):
        if self.state == "MENU":
            self.draw_menu()
        else:
            self.draw_playing()

    def draw_menu(self):
        self.screen.fill(BG_COLOR)
        
        title_text = self.title_font.render("CARO AI", True, TEXT_COLOR)
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 150))
        
        subtitle_text = self.font.render("CHE DO AI:", True, TEXT_COLOR)
        self.screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, HEIGHT//2 - 80))
        
        # Nút Minimax
        pygame.draw.rect(self.screen, (100, 150, 200), self.menu_minimax_rect, border_radius=8)
        pygame.draw.rect(self.screen, (50, 100, 150), self.menu_minimax_rect, 3, border_radius=8)
        mm_text = self.font.render("MINIMAX", True, (255, 255, 255))
        self.screen.blit(mm_text, (self.menu_minimax_rect.x + (self.menu_minimax_rect.width - mm_text.get_width())//2, self.menu_minimax_rect.y + (self.menu_minimax_rect.height - mm_text.get_height())//2))
        
        # Nút Alpha-Beta
        pygame.draw.rect(self.screen, (200, 100, 100), self.menu_alphabeta_rect, border_radius=8)
        pygame.draw.rect(self.screen, (150, 50, 50), self.menu_alphabeta_rect, 3, border_radius=8)
        ab_text = self.font.render("ALPHA-BETA", True, (255, 255, 255))
        self.screen.blit(ab_text, (self.menu_alphabeta_rect.x + (self.menu_alphabeta_rect.width - ab_text.get_width())//2, self.menu_alphabeta_rect.y + (self.menu_alphabeta_rect.height - ab_text.get_height())//2))
        
        pygame.display.flip()
        
    def draw_playing(self):
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
                self.screen.blit(stats, (WIDTH//2 - stats.get_width()//2, status_y + 30))
                
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
                
                if self.state == "MENU":
                    if self.menu_minimax_rect.collidepoint(x, y):
                        config.AI_ALGO = "minimax"
                        self.state = "PLAYING"
                        self.game.reset()
                    elif self.menu_alphabeta_rect.collidepoint(x, y):
                        config.AI_ALGO = "alphabeta"
                        self.state = "PLAYING"
                        self.game.reset()
                else:
                    # Nếu game đã kết thúc, kiểm tra xem click vào nút chơi lại không
                    if self.game.is_game_over:
                        if self.restart_rect and self.restart_rect.collidepoint(x, y):
                            self.game.reset()
                            self.state = "MENU" # Về lại màn hình menu khi bấm chơi lại
                    # Nếu game chưa kết thúc và đang là lượt người chơi
                    elif not self.game.is_game_over and self.game.current_player == PLAYER_X:
                        if MARGIN <= x <= MARGIN + BOARD_SIZE * CELL_SIZE and MARGIN <= y <= MARGIN + BOARD_SIZE * CELL_SIZE:
                            col = (x - MARGIN) // CELL_SIZE
                            row = (y - MARGIN) // CELL_SIZE
                            self.game.handle_human_move(row, col)
