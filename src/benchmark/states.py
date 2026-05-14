# src/benchmark/states.py
from src.board import Board
from config import PLAYER_X, PLAYER_O

def create_board_from_strings(board_strs):
    """Tạo bàn cờ từ danh sách chuỗi ký tự"""
    board = Board()
    for r, row_str in enumerate(board_strs):
        for c, char in enumerate(row_str):
            if char in (PLAYER_X, PLAYER_O):
                board.make_move(r, c, char)
    return board

# 1. Trạng thái đầu ván (Opening)
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

# 2. Trạng thái giữa ván (Midgame)
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

# 3. Trạng thái AI có thể thắng ngay (AI_WIN) - O có 3 quân
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

# 4. Trạng thái người chơi sắp thắng, AI phải chặn (MUST_BLOCK) - X có 3 quân
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

# 5. Trạng thái hai bên cùng tấn công (MUTUAL_ATTACK)
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

BENCHMARK_STATES = {
    "Opening": STATE_OPENING,
    "Midgame": STATE_MIDGAME,
    "AI Can Win": STATE_AI_WIN,
    "Must Block": STATE_MUST_BLOCK,
    "Mutual Attack": STATE_MUTUAL_ATTACK
}
