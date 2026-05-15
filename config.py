# config.py

BOARD_SIZE = 9       # Kích thước bàn cờ (N×N)
WIN_LENGTH = 4       # Số quân liên tiếp để chiến thắng
MAX_DEPTH = 3        # Độ sâu tìm kiếm mặc định
AI_ALGO = None       # Thuật toán sẽ được chọn thông qua giao diện menu
CANDIDATE_RADIUS = 1  # Bán kính tìm kiếm nước đi quanh các quân đã đánh
USE_ADVANCED_HEURISTIC = False # Bật/Tắt AI Nâng Cao (Thêm điểm quyền chủ động & Mở rộng nhánh)

# Ký hiệu trên bàn cờ
PLAYER_X = 'X' # Người
PLAYER_O = 'O' # Máy
EMPTY = '.'

# Màu sắc giao diện (Pygame) - Cải tiến theme Bảng Gỗ
BG_COLOR = (245, 222, 179)      # Màu nền ngoài lề (Wheat)
BOARD_COLOR = (222, 184, 135)   # Màu nền bàn cờ (Burlywood)
GRID_COLOR = (139, 69, 19)      # Màu đường kẻ lưới (Nâu sẫm)
X_COLOR = (200, 40, 40)         # Màu quân X (Đỏ đậm)
O_COLOR = (30, 80, 200)         # Màu quân O (Xanh biển)
TEXT_COLOR = (60, 30, 10)       # Màu chữ (Nâu đen)
BTN_COLOR = (160, 82, 45)       # Màu nút bấm (Sienna)
BTN_HOVER_COLOR = (205, 133, 63) # Màu nút bấm khi hover (Peru)
