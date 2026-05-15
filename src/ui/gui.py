# src/ui/gui.py
import pygame
import sys
import config
from config import BOARD_SIZE, PLAYER_X, PLAYER_O, EMPTY, BG_COLOR, BOARD_COLOR, GRID_COLOR, X_COLOR, O_COLOR, TEXT_COLOR, BTN_COLOR, BTN_HOVER_COLOR

CELL_SIZE = 50
MARGIN = 50
WIDTH = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * MARGIN + 120 # Chừa chỗ cho text và status bar

class GUI:
    def __init__(self, game):
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro AI - Bảng Gỗ")
        self.font = pygame.font.SysFont("segoe ui", 22, bold=True)
        self.large_font = pygame.font.SysFont("segoe ui", 28, bold=True)
        self.title_font = pygame.font.SysFont("segoe ui", 56, bold=True)
        self.restart_rect = None
        self.state = "MENU" # "MENU" or "PLAYING"
        
        # Các nút của màn hình Menu
        btn_w, btn_h = 280, 60
        self.menu_minimax_rect = pygame.Rect(WIDTH//2 - btn_w//2, HEIGHT//2 - 30, btn_w, btn_h)
        self.menu_alphabeta_rect = pygame.Rect(WIDTH//2 - btn_w//2, HEIGHT//2 + 50, btn_w, btn_h)
        
        self.btn_minus_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 150, 40, 40)
        self.btn_plus_rect = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 150, 40, 40)
        
        self.btn_adv_rect = pygame.Rect(WIDTH//2 - 140, HEIGHT//2 + 210, 280, 45)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.state == "MENU":
            self.draw_menu(mouse_pos)
        else:
            self.draw_playing(mouse_pos)

    def draw_menu(self, mouse_pos):
        self.screen.fill(BG_COLOR)
        
        # Vẽ tiêu đề có shadow
        title_text = self.title_font.render("CARO AI", True, TEXT_COLOR)
        shadow_text = self.title_font.render("CARO AI", True, (100, 50, 20))
        self.screen.blit(shadow_text, (WIDTH//2 - title_text.get_width()//2 + 3, HEIGHT//2 - 147))
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 150))
        
        subtitle_text = self.font.render("CHỌN CHẾ ĐỘ AI", True, TEXT_COLOR)
        self.screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, HEIGHT//2 - 80))
        
        # Hàm hỗ trợ vẽ nút
        def draw_btn(rect, text, is_hover):
            color = BTN_HOVER_COLOR if is_hover else BTN_COLOR
            # Đổ bóng
            pygame.draw.rect(self.screen, (100, 50, 20), rect.move(2, 4), border_radius=10)
            # Nút chính
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, (100, 50, 20), rect, 3, border_radius=10)
            
            txt_surf = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(txt_surf, (rect.x + (rect.width - txt_surf.get_width())//2, rect.y + (rect.height - txt_surf.get_height())//2))

        draw_btn(self.menu_minimax_rect, "THUẬT TOÁN MINIMAX", self.menu_minimax_rect.collidepoint(mouse_pos))
        draw_btn(self.menu_alphabeta_rect, "THUẬT TOÁN ALPHA-BETA", self.menu_alphabeta_rect.collidepoint(mouse_pos))
        
        # Nút thay đổi độ sâu AI
        depth_label = self.font.render("ĐỘ SÂU AI:", True, TEXT_COLOR)
        self.screen.blit(depth_label, (WIDTH//2 - depth_label.get_width()//2, HEIGHT//2 + 120))
        
        draw_btn(self.btn_minus_rect, "-", self.btn_minus_rect.collidepoint(mouse_pos))
        depth_val = self.large_font.render(str(config.MAX_DEPTH), True, TEXT_COLOR)
        self.screen.blit(depth_val, (WIDTH//2 - depth_val.get_width()//2, HEIGHT//2 + 152))
        draw_btn(self.btn_plus_rect, "+", self.btn_plus_rect.collidepoint(mouse_pos))
        
        # Nút AI Nâng Cao
        adv_text = "AI NÂNG CAO: BẬT" if config.USE_ADVANCED_HEURISTIC else "AI NÂNG CAO: TẮT"
        draw_btn(self.btn_adv_rect, adv_text, self.btn_adv_rect.collidepoint(mouse_pos))
        
        pygame.display.flip()
        
    def draw_playing(self, mouse_pos):
        self.screen.fill(BG_COLOR)
        
        # Vẽ nền bàn cờ gỗ đậm hơn
        board_rect = pygame.Rect(MARGIN, MARGIN, BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
        pygame.draw.rect(self.screen, BOARD_COLOR, board_rect)
        pygame.draw.rect(self.screen, GRID_COLOR, board_rect, 4) # Viền ngoài bàn cờ
        
        # Vẽ lưới
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(self.screen, GRID_COLOR, (MARGIN + i * CELL_SIZE, MARGIN), (MARGIN + i * CELL_SIZE, MARGIN + BOARD_SIZE * CELL_SIZE), 2)
            pygame.draw.line(self.screen, GRID_COLOR, (MARGIN, MARGIN + i * CELL_SIZE), (MARGIN + BOARD_SIZE * CELL_SIZE, MARGIN + i * CELL_SIZE), 2)
                             
        # Vẽ highlight nước đi cuối
        if getattr(self.game, 'last_move', None):
            r, c = self.game.last_move
            highlight_rect = pygame.Rect(MARGIN + c * CELL_SIZE + 2, MARGIN + r * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            s = pygame.Surface((CELL_SIZE-4, CELL_SIZE-4), pygame.SRCALPHA)
            s.fill((255, 255, 100, 100)) # Vàng mờ
            self.screen.blit(s, highlight_rect)

        # Vẽ hiệu ứng hover nếu đang là lượt người
        if not self.game.is_game_over and self.game.current_player == PLAYER_X:
            mx, my = mouse_pos
            if MARGIN <= mx < MARGIN + BOARD_SIZE * CELL_SIZE and MARGIN <= my < MARGIN + BOARD_SIZE * CELL_SIZE:
                c = (mx - MARGIN) // CELL_SIZE
                r = (my - MARGIN) // CELL_SIZE
                if self.game.board.grid[r][c] == EMPTY:
                    # Vẽ X mờ
                    self.draw_x(r, c, alpha=100)
                    
        # Vẽ các quân cờ
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.game.board.grid[r][c] == PLAYER_X:
                    self.draw_x(r, c)
                elif self.game.board.grid[r][c] == PLAYER_O:
                    self.draw_o(r, c)
                    
        # Vẽ đường chiến thắng nếu có
        if getattr(self.game, 'win_coords', None):
            coords = self.game.win_coords
            start_r, start_c = coords[0]
            end_r, end_c = coords[-1]
            start_pos = (MARGIN + start_c * CELL_SIZE + CELL_SIZE//2, MARGIN + start_r * CELL_SIZE + CELL_SIZE//2)
            end_pos = (MARGIN + end_c * CELL_SIZE + CELL_SIZE//2, MARGIN + end_r * CELL_SIZE + CELL_SIZE//2)
            pygame.draw.line(self.screen, (255, 50, 50), start_pos, end_pos, 8)
                    
        # Vẽ phần Status bar dưới cùng
        self.draw_status_bar(mouse_pos)
        pygame.display.flip()

    def draw_status_bar(self, mouse_pos):
        status_y = HEIGHT - 100
        
        if self.game.is_game_over:
            if self.game.winner == PLAYER_X:
                msg = "KẾT QUẢ: BẠN THẮNG!"
                color = X_COLOR
            elif self.game.winner == PLAYER_O:
                msg = "KẾT QUẢ: MÁY THẮNG!"
                color = O_COLOR
            else:
                msg = "KẾT QUẢ: HÒA!"
                color = TEXT_COLOR
                
            text = self.large_font.render(msg, True, color)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, status_y))
            
            # Nút Chơi Lại
            btn_text = self.font.render("CHƠI LẠI", True, (255, 255, 255))
            btn_w, btn_h = 160, 45
            btn_x, btn_y = WIDTH//2 - btn_w//2, status_y + 40
            self.restart_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            
            is_hover = self.restart_rect.collidepoint(mouse_pos)
            btn_color = BTN_HOVER_COLOR if is_hover else BTN_COLOR
            pygame.draw.rect(self.screen, (100, 50, 20), self.restart_rect.move(2, 3), border_radius=8)
            pygame.draw.rect(self.screen, btn_color, self.restart_rect, border_radius=8)
            pygame.draw.rect(self.screen, (100, 50, 20), self.restart_rect, 2, border_radius=8)
            
            self.screen.blit(btn_text, (btn_x + (btn_w - btn_text.get_width()) // 2, btn_y + (btn_h - btn_text.get_height()) // 2))
        else:
            if self.game.current_player == PLAYER_X:
                turn_str = "LƯỢT CỦA BẠN (X)"
                color = X_COLOR
            else:
                turn_str = "AI ĐANG SUY NGHĨ..."
                color = O_COLOR
                
            text = self.large_font.render(turn_str, True, color)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, status_y))
            
            if getattr(self.game, 'last_ai_time', 0) > 0:
                stats = self.font.render(f"AI: {self.game.last_ai_time:.0f}ms | Duyệt: {self.game.last_ai_nodes} node", True, TEXT_COLOR)
                self.screen.blit(stats, (WIDTH//2 - stats.get_width()//2, status_y + 45))
        
    def draw_x(self, row, col, alpha=255):
        center_x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        center_y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        offset = CELL_SIZE // 3 - 2
        
        surface = self.screen
        color = X_COLOR
        if alpha < 255:
            # Dùng surface phụ cho trong suốt
            surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            color = (*X_COLOR, alpha)
            center_x, center_y = CELL_SIZE // 2, CELL_SIZE // 2
        else:
            # Vẽ bóng đổ (shadow)
            pygame.draw.line(self.screen, (100, 50, 20), (center_x - offset + 2, center_y - offset + 3), (center_x + offset + 2, center_y + offset + 3), 6)
            pygame.draw.line(self.screen, (100, 50, 20), (center_x + offset + 2, center_y - offset + 3), (center_x - offset + 2, center_y + offset + 3), 6)
            
        pygame.draw.line(surface, color, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 5)
        pygame.draw.line(surface, color, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 5)
        
        if alpha < 255:
            self.screen.blit(surface, (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE))
        
    def draw_o(self, row, col):
        center_x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        center_y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 3
        
        # Vẽ bóng đổ (shadow)
        pygame.draw.circle(self.screen, (100, 50, 20), (center_x + 2, center_y + 3), radius, 5)
        # Vẽ hình chính
        pygame.draw.circle(self.screen, O_COLOR, (center_x, center_y), radius, 4)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1: continue # Chỉ bắt chuột trái
                x, y = event.pos
                
                if self.state == "MENU":
                    if self.menu_minimax_rect.collidepoint(x, y):
                        config.AI_ALGO = "minimax"
                        self.state = "PLAYING"
                        self.game.reset()
                    elif self.menu_alphabeta_rect.collidepoint(x, y):
                        config.AI_ALGO = "alphabeta"
                        self.state = "PLAYING"
                        self.game.reset()
                    elif self.btn_minus_rect.collidepoint(x, y):
                        config.MAX_DEPTH = max(1, config.MAX_DEPTH - 1)
                    elif self.btn_plus_rect.collidepoint(x, y):
                        config.MAX_DEPTH = min(5, config.MAX_DEPTH + 1)
                    elif self.btn_adv_rect.collidepoint(x, y):
                        config.USE_ADVANCED_HEURISTIC = not config.USE_ADVANCED_HEURISTIC
                else:
                    if self.game.is_game_over:
                        if getattr(self, 'restart_rect', None) and self.restart_rect.collidepoint(x, y):
                            self.game.reset()
                            self.state = "MENU"
                    elif not self.game.is_game_over and self.game.current_player == PLAYER_X:
                        if MARGIN <= x < MARGIN + BOARD_SIZE * CELL_SIZE and MARGIN <= y < MARGIN + BOARD_SIZE * CELL_SIZE:
                            col = (x - MARGIN) // CELL_SIZE
                            row = (y - MARGIN) // CELL_SIZE
                            self.game.handle_human_move(row, col)
