# src/board.py - Lớp Board quản lý trạng thái bàn cờ Caro
import copy
from config import BOARD_SIZE, WIN_LENGTH, EMPTY, CANDIDATE_RADIUS


class Board:
    """Bàn cờ Caro N×N. Lưu trạng thái các ô, kiểm tra thắng/thua/hòa."""

    def __init__(self, size=BOARD_SIZE):
        """Khởi tạo bàn cờ trống kích thước size×size."""
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.move_count = 0  # Số nước đã đánh

    def copy(self):
        """Trả về bản sao độc lập của bàn cờ (dùng cho AI khi thử nước đi)."""
        new_board = Board(self.size)
        new_board.grid = copy.deepcopy(self.grid)
        new_board.move_count = self.move_count
        return new_board

    def is_valid_move(self, row, col):
        """Kiểm tra ô (row, col) có nằm trong bàn cờ và còn trống không."""
        return 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == EMPTY

    def make_move(self, row, col, player):
        """
        Đặt quân player vào ô (row, col) nếu hợp lệ.
        Trả về True nếu thành công, False nếu không hợp lệ.
        """
        if self.is_valid_move(row, col):
            self.grid[row][col] = player
            self.move_count += 1
            return True
        return False

    def is_full(self):
        """Kiểm tra bàn cờ đã đầy chưa (dùng để xác định hòa)."""
        return self.move_count >= self.size * self.size

    def get_candidate_moves(self):
        """
        Sinh danh sách nước đi ứng viên cho AI.
        Chỉ xét các ô trống nằm trong bán kính CANDIDATE_RADIUS quanh quân đã đánh,
        giúp giảm không gian tìm kiếm. Nếu bàn trống, trả về ô trung tâm.
        """
        if self.move_count == 0:
            return [(self.size // 2, self.size // 2)]

        candidates = set()
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != EMPTY:
                    for i in range(-CANDIDATE_RADIUS, CANDIDATE_RADIUS + 1):
                        for j in range(-CANDIDATE_RADIUS, CANDIDATE_RADIUS + 1):
                            nr, nc = r + i, c + j
                            if self.is_valid_move(nr, nc):
                                candidates.add((nr, nc))
        return list(candidates)

    def check_win(self, player):
        """
        Kiểm tra player có WIN_LENGTH quân liên tiếp chưa.
        Xét 4 hướng: ngang, dọc, chéo chính, chéo phụ.
        Không áp dụng luật chặn 2 đầu.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

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
        """
        Kiểm tra ván cờ đã kết thúc chưa.
        Trả về (True/False, người_thắng):
          - (True, 'X')   : Người thắng
          - (True, 'O')   : AI thắng
          - (True, None)  : Hòa
          - (False, None) : Ván chưa kết thúc
        """
        from config import PLAYER_X, PLAYER_O
        if self.check_win(PLAYER_X):
            return True, PLAYER_X
        if self.check_win(PLAYER_O):
            return True, PLAYER_O
        if self.is_full():
            return True, None
        return False, None

    def get_winning_line(self, player):
        """
        Tìm tọa độ WIN_LENGTH quân liên tiếp tạo nên chiến thắng của player.
        Dùng để vẽ đường gạch đỏ trên GUI sau khi game kết thúc.
        Trả về list[(row, col)] hoặc None nếu không tìm thấy.
        """
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
        """In bàn cờ dạng text ra console (dùng để debug)."""
        print("  " + " ".join([str(i) for i in range(self.size)]))
        for r in range(self.size):
            print(f"{r} " + " ".join(self.grid[r]))
