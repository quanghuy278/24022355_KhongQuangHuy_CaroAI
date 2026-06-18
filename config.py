# config.py - Các hằng số cấu hình toàn cục của dự án

# ── Tham số logic trò chơi ──────────────────────────────────
BOARD_SIZE = 9        # Kích thước bàn cờ (N×N)
WIN_LENGTH = 4        # Số quân liên tiếp để chiến thắng
MAX_DEPTH = 3         # Độ sâu tìm kiếm mặc định của AI
AI_ALGO = None        # Thuật toán AI đang dùng ("minimax" / "alphabeta"), chọn ở Menu
CANDIDATE_RADIUS = 1  # Bán kính tìm nước đi ứng viên quanh các quân đã đánh
USE_ADVANCED_HEURISTIC = False  # Bật/Tắt heuristic nâng cao (trọng số chủ động + Search Extension)

# ── Ký hiệu trên bàn cờ ────────────────────────────────────
PLAYER_X = 'X'  # Người chơi (đi trước)
PLAYER_O = 'O'  # AI (Max trong Minimax)
EMPTY = '.'     # Ô trống

# ── Màu sắc giao diện Pygame - Theme Bảng Gỗ (R, G, B) ────
BG_COLOR = (245, 222, 179)       # Màu nền ngoài lề (Wheat)
BOARD_COLOR = (222, 184, 135)    # Màu nền bàn cờ (Burlywood)
GRID_COLOR = (139, 69, 19)       # Màu đường kẻ lưới (Nâu sẫm)
X_COLOR = (200, 40, 40)          # Màu quân X (Đỏ đậm)
O_COLOR = (30, 80, 200)          # Màu quân O (Xanh biển)
TEXT_COLOR = (60, 30, 10)        # Màu chữ (Nâu đen)
BTN_COLOR = (160, 82, 45)        # Màu nút bấm (Sienna)
BTN_HOVER_COLOR = (205, 133, 63) # Màu nút bấm khi hover (Peru)
