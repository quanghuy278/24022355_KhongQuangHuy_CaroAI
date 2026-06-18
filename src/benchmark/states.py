# src/benchmark/states.py - Định nghĩa các trạng thái bàn cờ dùng để benchmark
from src.board import Board
from config import PLAYER_X, PLAYER_O


def create_board_from_strings(board_strs):
    """
    Tạo đối tượng Board từ danh sách chuỗi ký tự.
    Mỗi chuỗi đại diện một hàng; 'X'/'O' là quân đã đánh, '.' là ô trống.
    """
    board = Board()
    for r, row_str in enumerate(board_strs):
        for c, char in enumerate(row_str):
            if char in (PLAYER_X, PLAYER_O):
                board.make_move(r, c, char)
    return board


# ── Các trạng thái bàn cờ mẫu để kiểm thử ──────────────────

# 1. Đầu ván: chỉ có 1 quân X ở giữa
STATE_OPENING = create_board_from_strings([
    ".........",
    ".........",
    ".........",
    ".........",
    "....X....",
    ".........",
    ".........",
    ".........",
    ".........",
])

# 2. Giữa ván: cả hai bên đã có vài quân xen kẽ
STATE_MIDGAME = create_board_from_strings([
    ".........",
    ".........",
    ".........",
    "...XO....",
    "...OXX...",
    "....O....",
    ".........",
    ".........",
    ".........",
])

# 3. AI có thể thắng ngay: O có 3 quân thẳng hàng
STATE_AI_WIN = create_board_from_strings([
    ".........",
    ".........",
    ".........",
    ".........",
    "....O....",
    "....O....",
    "....O....",
    ".........",
    ".........",
])

# 4. Người sắp thắng, AI phải chặn: X có 3 quân chéo liên tiếp
STATE_MUST_BLOCK = create_board_from_strings([
    ".........",
    ".........",
    ".........",
    "....X....",
    ".....X...",
    "......X..",
    ".........",
    ".........",
    ".........",
])

# 5. Hai bên cùng tấn công: cả X lẫn O đều đang phát triển
STATE_MUTUAL_ATTACK = create_board_from_strings([
    ".........",
    ".........",
    "..X......",
    "...XO....",
    "...XOO...",
    ".....O...",
    ".........",
    ".........",
    ".........",
])

# Dictionary tổng hợp: tên trạng thái → đối tượng Board, dùng trong runner.py
BENCHMARK_STATES = {
    "Opening": STATE_OPENING,
    "Midgame": STATE_MIDGAME,
    "AI Can Win": STATE_AI_WIN,
    "Must Block": STATE_MUST_BLOCK,
    "Mutual Attack": STATE_MUTUAL_ATTACK
}
