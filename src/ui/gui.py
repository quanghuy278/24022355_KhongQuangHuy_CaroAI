# src/ui/gui.py - Giao diện đồ họa Pygame cho game Caro AI
import pygame
import sys
import config
from config import BOARD_SIZE, PLAYER_X, PLAYER_O, EMPTY, BG_COLOR, BOARD_COLOR, GRID_COLOR, X_COLOR, O_COLOR, TEXT_COLOR, BTN_COLOR, BTN_HOVER_COLOR

# ── Hằng số kích thước giao diện ────────────────────────────
CELL_SIZE = 50                                          # Kích thước mỗi ô (pixel)
MARGIN = 50                                             # Lề xung quanh bàn cờ
WIDTH = BOARD_SIZE * CELL_SIZE + 2 * MARGIN             # Chiều rộng cửa sổ
HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * MARGIN + 120      # Chiều cao cửa sổ (thêm thanh trạng thái)


class GUI:
    """Lớp quản lý toàn bộ giao diện đồ họa (Menu + Màn hình chơi)."""

    def __init__(self, game):
        """
        Khởi tạo Pygame, tạo cửa sổ và định nghĩa vị trí các nút bấm.
        game: đối tượng Game để đọc trạng thái và gọi các hàm xử lý.
        """
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro AI - Bảng Gỗ")
        self.font = pygame.font.SysFont("segoe ui", 22, bold=True)
        self.large_font = pygame.font.SysFont("segoe ui", 28, bold=True)
        self.title_font = pygame.font.SysFont("segoe ui", 56, bold=True)
        self.restart_rect = None
        self.state = "MENU"  # Trạng thái giao diện: "MENU" hoặc "PLAYING"

        # Vị trí và kích thước các nút bấm trên màn hình Menu
        btn_w, btn_h = 280, 60
        self.menu_minimax_rect = pygame.Rect(WIDTH//2 - btn_w//2, HEIGHT//2 - 30, btn_w, btn_h)
        self.menu_alphabeta_rect = pygame.Rect(WIDTH//2 - btn_w//2, HEIGHT//2 + 50, btn_w, btn_h)

        self.btn_minus_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 150, 40, 40)   # Nút giảm độ sâu
        self.btn_plus_rect = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 150, 40, 40)    # Nút tăng độ sâu

        self.btn_adv_rect = pygame.Rect(WIDTH//2 - 140, HEIGHT//2 + 210, 280, 45)   # Nút bật/tắt AI nâng cao

    def draw(self):
        """Điều hướng vẽ màn hình: gọi draw_menu() hoặc draw_playing() tùy state."""
        mouse_pos = pygame.mouse.get_pos()
        if self.state == "MENU":
            self.draw_menu(mouse_pos)
        else:
            self.draw_playing(mouse_pos)

    def draw_menu(self, mouse_pos):
        """
        Vẽ màn hình Menu chọn chế độ AI.
        Hiển thị tiêu đề, các nút chọn thuật toán, điều chỉnh độ sâu và bật/tắt AI nâng cao.
        """
        self.screen.fill(BG_COLOR)

        # Vẽ tiêu đề có bóng đổ (shadow effect)
        title_text = self.title_font.render("CARO AI", True, TEXT_COLOR)
        shadow_text = self.title_font.render("CARO AI", True, (100, 50, 20))
        self.screen.blit(shadow_text, (WIDTH//2 - title_text.get_width()//2 + 3, HEIGHT//2 - 147))
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 150))

        subtitle_text = self.font.render("CHỌN CHẾ ĐỘ AI", True, TEXT_COLOR)
        self.screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, HEIGHT//2 - 80))

        # Hàm nội bộ: vẽ một nút bấm có bóng đổ và hiệu ứng hover
        def draw_btn(rect, text, is_hover):
            color = BTN_HOVER_COLOR if is_hover else BTN_COLOR
            pygame.draw.rect(self.screen, (100, 50, 20), rect.move(2, 4), border_radius=10)  # Bóng
            pygame.draw.rect(self.screen, color, rect, border_radius=10)                      # Nền nút
            pygame.draw.rect(self.screen, (100, 50, 20), rect, 3, border_radius=10)           # Viền nút
            txt_surf = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(txt_surf, (rect.x + (rect.width - txt_surf.get_width())//2,
                                        rect.y + (rect.height - txt_surf.get_height())//2))

        draw_btn(self.menu_minimax_rect, "THUẬT TOÁN MINIMAX", self.menu_minimax_rect.collidepoint(mouse_pos))
        draw_btn(self.menu_alphabeta_rect, "THUẬT TOÁN ALPHA-BETA", self.menu_alphabeta_rect.collidepoint(mouse_pos))

        # Nhóm điều chỉnh độ sâu AI
        depth_label = self.font.render("ĐỘ SÂU AI:", True, TEXT_COLOR)
        self.screen.blit(depth_label, (WIDTH//2 - depth_label.get_width()//2, HEIGHT//2 + 120))

        draw_btn(self.btn_minus_rect, "-", self.btn_minus_rect.collidepoint(mouse_pos))
        depth_val = self.large_font.render(str(config.MAX_DEPTH), True, TEXT_COLOR)
        self.screen.blit(depth_val, (WIDTH//2 - depth_val.get_width()//2, HEIGHT//2 + 152))
        draw_btn(self.btn_plus_rect, "+", self.btn_plus_rect.collidepoint(mouse_pos))

        # Nút bật/tắt AI Nâng Cao
        adv_text = "AI NÂNG CAO: BẬT" if config.USE_ADVANCED_HEURISTIC else "AI NÂNG CAO: TẮT"
        draw_btn(self.btn_adv_rect, adv_text, self.btn_adv_rect.collidepoint(mouse_pos))

        pygame.display.flip()

    def draw_playing(self, mouse_pos):
        """
        Vẽ màn hình chơi cờ chính gồm:
        - Nền bàn cờ gỗ và lưới kẻ ô
        - Highlight ô vừa đánh (màu vàng mờ)
        - Hiệu ứng hover: hiện X mờ tại ô chuột đang trỏ (lượt người)
        - Tất cả quân X và O đang trên bàn
        - Đường thắng (gạch đỏ) nếu game kết thúc
        - Thanh trạng thái phía dưới
        """
        self.screen.fill(BG_COLOR)

        # Vẽ nền và viền bàn cờ
        board_rect = pygame.Rect(MARGIN, MARGIN, BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
        pygame.draw.rect(self.screen, BOARD_COLOR, board_rect)
        pygame.draw.rect(self.screen, GRID_COLOR, board_rect, 4)

        # Vẽ lưới
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(self.screen, GRID_COLOR, (MARGIN + i * CELL_SIZE, MARGIN), (MARGIN + i * CELL_SIZE, MARGIN + BOARD_SIZE * CELL_SIZE), 2)
            pygame.draw.line(self.screen, GRID_COLOR, (MARGIN, MARGIN + i * CELL_SIZE), (MARGIN + BOARD_SIZE * CELL_SIZE, MARGIN + i * CELL_SIZE), 2)

        # Highlight ô vừa đánh (vàng mờ)
        if getattr(self.game, 'last_move', None):
            r, c = self.game.last_move
            highlight_rect = pygame.Rect(MARGIN + c * CELL_SIZE + 2, MARGIN + r * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            s = pygame.Surface((CELL_SIZE-4, CELL_SIZE-4), pygame.SRCALPHA)
            s.fill((255, 255, 100, 100))
            self.screen.blit(s, highlight_rect)

        # Hiệu ứng hover: vẽ X mờ tại ô đang trỏ (chỉ lượt người)
        if not self.game.is_game_over and self.game.current_player == PLAYER_X:
            mx, my = mouse_pos
            if MARGIN <= mx < MARGIN + BOARD_SIZE * CELL_SIZE and MARGIN <= my < MARGIN + BOARD_SIZE * CELL_SIZE:
                c = (mx - MARGIN) // CELL_SIZE
                r = (my - MARGIN) // CELL_SIZE
                if self.game.board.grid[r][c] == EMPTY:
                    self.draw_x(r, c, alpha=100)

        # Vẽ toàn bộ quân cờ trên bàn
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.game.board.grid[r][c] == PLAYER_X:
                    self.draw_x(r, c)
                elif self.game.board.grid[r][c] == PLAYER_O:
                    self.draw_o(r, c)

        # Vẽ đường thắng nếu game kết thúc
        if getattr(self.game, 'win_coords', None):
            coords = self.game.win_coords
            start_r, start_c = coords[0]
            end_r, end_c = coords[-1]
            start_pos = (MARGIN + start_c * CELL_SIZE + CELL_SIZE//2, MARGIN + start_r * CELL_SIZE + CELL_SIZE//2)
            end_pos = (MARGIN + end_c * CELL_SIZE + CELL_SIZE//2, MARGIN + end_r * CELL_SIZE + CELL_SIZE//2)
            pygame.draw.line(self.screen, (255, 50, 50), start_pos, end_pos, 8)

        self.draw_status_bar(mouse_pos)
        pygame.display.flip()

    def draw_status_bar(self, mouse_pos):
        """
        Vẽ thanh trạng thái phía dưới màn hình chơi.
        - Khi game kết thúc: hiện kết quả (thắng/thua/hòa) và nút "CHƠI LẠI".
        - Khi đang chơi: hiện lượt hiện tại và thống kê AI (thời gian, số node).
        """
        status_y = HEIGHT - 100

        if self.game.is_game_over:
            # Hiển thị kết quả và màu theo người thắng
            if self.game.winner == PLAYER_X:
                msg, color = "KẾT QUẢ: BẠN THẮNG!", X_COLOR
            elif self.game.winner == PLAYER_O:
                msg, color = "KẾT QUẢ: MÁY THẮNG!", O_COLOR
            else:
                msg, color = "KẾT QUẢ: HÒA!", TEXT_COLOR

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
            self.screen.blit(btn_text, (btn_x + (btn_w - btn_text.get_width()) // 2,
                                        btn_y + (btn_h - btn_text.get_height()) // 2))
        else:
            # Hiện lượt đi hiện tại
            if self.game.current_player == PLAYER_X:
                turn_str, color = "LƯỢT CỦA BẠN (X)", X_COLOR
            else:
                turn_str, color = "AI ĐANG SUY NGHĨ...", O_COLOR

            text = self.large_font.render(turn_str, True, color)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, status_y))

            # Hiện thống kê lần AI đi vừa rồi
            if getattr(self.game, 'last_ai_time', 0) > 0:
                stats = self.font.render(f"AI: {self.game.last_ai_time:.0f}ms | Duyệt: {self.game.last_ai_nodes} node", True, TEXT_COLOR)
                self.screen.blit(stats, (WIDTH//2 - stats.get_width()//2, status_y + 45))

    def draw_x(self, row, col, alpha=255):
        """
        Vẽ quân X tại ô (row, col).
        Nếu alpha < 255: vẽ mờ lên surface phụ (dùng cho hiệu ứng hover).
        Nếu alpha = 255: vẽ đầy đủ kèm bóng đổ.
        """
        center_x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        center_y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        offset = CELL_SIZE // 3 - 2

        surface = self.screen
        color = X_COLOR
        if alpha < 255:
            surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            color = (*X_COLOR, alpha)
            center_x, center_y = CELL_SIZE // 2, CELL_SIZE // 2
        else:
            # Bóng đổ
            pygame.draw.line(self.screen, (100, 50, 20), (center_x - offset + 2, center_y - offset + 3), (center_x + offset + 2, center_y + offset + 3), 6)
            pygame.draw.line(self.screen, (100, 50, 20), (center_x + offset + 2, center_y - offset + 3), (center_x - offset + 2, center_y + offset + 3), 6)

        pygame.draw.line(surface, color, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 5)
        pygame.draw.line(surface, color, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 5)

        if alpha < 255:
            self.screen.blit(surface, (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE))

    def draw_o(self, row, col):
        """Vẽ quân O (hình tròn rỗng) tại ô (row, col) kèm bóng đổ."""
        center_x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        center_y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 3

        pygame.draw.circle(self.screen, (100, 50, 20), (center_x + 2, center_y + 3), radius, 5)  # Bóng
        pygame.draw.circle(self.screen, O_COLOR, (center_x, center_y), radius, 4)                # Quân

    def handle_events(self):
        """
        Xử lý toàn bộ sự kiện Pygame trong một frame:
        - Đóng cửa sổ → thoát chương trình.
        - Click chuột trái:
            + Ở MENU: chọn thuật toán / điều chỉnh độ sâu / bật-tắt AI nâng cao.
            + Ở PLAYING + game kết thúc: click "Chơi lại" → reset game về MENU.
            + Ở PLAYING + lượt người: click ô hợp lệ → gọi handle_human_move().
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1: continue  # Chỉ xử lý chuột trái
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
                        config.MAX_DEPTH = max(1, config.MAX_DEPTH - 1)   # Giảm độ sâu (tối thiểu 1)
                    elif self.btn_plus_rect.collidepoint(x, y):
                        config.MAX_DEPTH = min(5, config.MAX_DEPTH + 1)   # Tăng độ sâu (tối đa 5)
                    elif self.btn_adv_rect.collidepoint(x, y):
                        config.USE_ADVANCED_HEURISTIC = not config.USE_ADVANCED_HEURISTIC  # Toggle
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
