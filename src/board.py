# src/board.py
import copy
from config import BOARD_SIZE, WIN_LENGTH, EMPTY, CANDIDATE_RADIUS

class Board:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.move_count = 0

    def copy(self):
        new_board = Board(self.size)
        new_board.grid = copy.deepcopy(self.grid)
        new_board.move_count = self.move_count
        return new_board

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == EMPTY

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.grid[row][col] = player
            self.move_count += 1
            return True
        return False

    def is_full(self):
        return self.move_count >= self.size * self.size

    def get_candidate_moves(self):
        """
        Sinh các nước đi hợp lệ. Để giảm không gian tìm kiếm,
        chỉ xét các ô trống nằm quanh các ô đã có quân trong bán kính CANDIDATE_RADIUS.
        """
        if self.move_count == 0:
            return [(self.size // 2, self.size // 2)] # Đi giữa bàn cờ nếu là nước đầu

        candidates = set()
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != EMPTY:
                    # Xét các ô xung quanh
                    for i in range(-CANDIDATE_RADIUS, CANDIDATE_RADIUS + 1):
                        for j in range(-CANDIDATE_RADIUS, CANDIDATE_RADIUS + 1):
                            nr, nc = r + i, c + j
                            if self.is_valid_move(nr, nc):
                                candidates.add((nr, nc))
        return list(candidates)

    def check_win(self, player):
        """
        Kiểm tra xem player đã có đủ WIN_LENGTH quân liên tiếp chưa.
        Không xét luật chặn 2 đầu.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # Ngang, Dọc, Chéo chính, Chéo phụ

        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == player:
                    for dr, dc in directions:
                        count = 0
                        for i in range(WIN_LENGTH):
                            nr, nc = r + dr * i, c + dc * i
                            if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == player:
                                count += 1
                            else:
                                break
                        if count == WIN_LENGTH:
                            return True
        return False

    def is_game_over(self):
        """Trả về (True/False, Người thắng)"""
        from config import PLAYER_X, PLAYER_O
        if self.check_win(PLAYER_X):
            return True, PLAYER_X
        if self.check_win(PLAYER_O):
            return True, PLAYER_O
        if self.is_full():
            return True, None # Hòa
        return False, None

    def get_winning_line(self, player):
        """Trả về danh sách tọa độ các quân cờ tạo nên chiến thắng, hoặc None"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == player:
                    for dr, dc in directions:
                        coords = []
                        for i in range(WIN_LENGTH):
                            nr, nc = r + dr * i, c + dc * i
                            if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == player:
                                coords.append((nr, nc))
                            else:
                                break
                        if len(coords) == WIN_LENGTH:
                            return coords
        return None

    def print_board(self):
        print("  " + " ".join([str(i) for i in range(self.size)]))
        for r in range(self.size):
            print(f"{r} " + " ".join(self.grid[r]))
