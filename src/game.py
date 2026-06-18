# src/game.py - Lớp Game điều phối toàn bộ luồng chạy của trò chơi
from src.board import Board
from src.ai.minimax import get_best_move_minimax
from src.ai.alphabeta import get_best_move_alphabeta
import config


class Game:
    """
    Lớp quản lý trạng thái và luồng chạy của ván cờ.
    Kết nối Board, AI và GUI với nhau.
    """

    def __init__(self, use_gui=True):
        """Khởi tạo ván cờ mới. use_gui=True khi chạy giao diện đồ họa."""
        self.board = Board()
        self.current_player = config.PLAYER_X  # Người luôn đi trước
        self.is_game_over = False
        self.winner = None
        self.use_gui = use_gui
        self.last_ai_time = 0       # Thời gian AI suy nghĩ (ms), hiển thị trên GUI
        self.last_ai_nodes = 0      # Số node đã duyệt, hiển thị trên GUI
        self.last_move = None       # Nước đi cuối cùng, dùng để highlight ô vừa đánh
        self.win_coords = None      # Tọa độ đường thắng, dùng để vẽ gạch đỏ

    def reset(self):
        """Đặt lại toàn bộ trạng thái về đầu ván mới (không tạo đối tượng mới)."""
        self.board = Board()
        self.current_player = config.PLAYER_X
        self.is_game_over = False
        self.winner = None
        self.last_ai_time = 0
        self.last_ai_nodes = 0
        self.last_move = None
        self.win_coords = None

    def switch_turn(self):
        """Chuyển lượt từ X sang O hoặc ngược lại."""
        self.current_player = config.PLAYER_O if self.current_player == config.PLAYER_X else config.PLAYER_X

    def check_game_state(self):
        """
        Kiểm tra trạng thái ván cờ sau mỗi nước đi.
        Nếu game kết thúc, lưu winner và tọa độ đường thắng (win_coords).
        """
        is_over, winner = self.board.is_game_over()
        if is_over:
            self.is_game_over = True
            self.winner = winner
            if winner:
                self.win_coords = self.board.get_winning_line(winner)

    def handle_human_move(self, row, col):
        """
        Xử lý nước đi của người chơi tại ô (row, col).
        Đặt quân X, kiểm tra game, rồi chuyển lượt sang AI nếu ván chưa kết thúc.
        """
        if self.board.make_move(row, col, config.PLAYER_X):
            self.last_move = (row, col)
            self.check_game_state()
            if not self.is_game_over:
                self.switch_turn()

    def make_ai_move(self):
        """
        Gọi thuật toán AI để tìm và thực hiện nước đi tốt nhất cho PLAYER_O.
        Thuật toán được chọn từ config.AI_ALGO ("minimax" hoặc "alphabeta").
        Lưu thông tin thời gian và số node duyệt để hiển thị trên GUI.
        """
        if self.is_game_over:
            return

        print(f"AI đang suy nghĩ bằng thuật toán {config.AI_ALGO} ở độ sâu {config.MAX_DEPTH}...")

        if config.AI_ALGO == "minimax":
            result = get_best_move_minimax(self.board, config.MAX_DEPTH)
        else:
            result = get_best_move_alphabeta(self.board, config.MAX_DEPTH)

        move = result.move
        if move:
            self.board.make_move(move[0], move[1], config.PLAYER_O)
            self.last_move = (move[0], move[1])
            self.last_ai_time = result.time_ms
            self.last_ai_nodes = result.states_visited

            print(f"AI đánh: {move}, Điểm: {result.score}, Duyệt: {result.states_visited} nodes, Thời gian: {result.time_ms:.2f} ms")

            self.check_game_state()
            if not self.is_game_over:
                self.switch_turn()

    def run_gui(self):
        """
        Vòng lặp chính của game khi chạy chế độ giao diện đồ họa.
        Mỗi frame: xử lý sự kiện → nếu đến lượt AI thì gọi make_ai_move() → vẽ màn hình.
        Giới hạn 30 FPS bằng pygame clock.
        """
        from src.ui.gui import GUI
        import pygame
        gui = GUI(self)
        clock = pygame.time.Clock()

        while True:
            gui.handle_events()

            # Nếu đang chơi và đến lượt AI, vẽ trước rồi để AI suy nghĩ
            if getattr(gui, 'state', 'PLAYING') == 'PLAYING' and self.current_player == config.PLAYER_O and not self.is_game_over:
                gui.draw()
                self.make_ai_move()

            gui.draw()
            clock.tick(30)
