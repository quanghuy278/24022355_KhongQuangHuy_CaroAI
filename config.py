# config.py

BOARD_SIZE = 9       # Kích thước bàn cờ (N×N)
WIN_LENGTH = 4       # Số quân liên tiếp để chiến thắng
MAX_DEPTH = 3        # Độ sâu tìm kiếm mặc định
AI_ALGO = "alphabeta" # Thuật toán mặc định: "minimax" | "alphabeta"
CANDIDATE_RADIUS = 1  # Bán kính tìm kiếm nước đi quanh các quân đã đánh

# Ký hiệu trên bàn cờ
PLAYER_X = 'X' # Người
PLAYER_O = 'O' # Máy
EMPTY = '.'

# Màu sắc giao diện (Pygame)
BG_COLOR = (245, 245, 220) # Màu nền (màu gỗ nhạt)
GRID_COLOR = (0, 0, 0)     # Màu đường kẻ
X_COLOR = (200, 50, 50)    # Màu quân X
O_COLOR = (50, 50, 200)    # Màu quân O
TEXT_COLOR = (0, 0, 0)
