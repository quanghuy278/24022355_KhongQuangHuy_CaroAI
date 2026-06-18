# src/ai/evaluate.py - Hàm đánh giá điểm trạng thái bàn cờ cho AI
from config import WIN_LENGTH, PLAYER_X, PLAYER_O, EMPTY

# Bảng điểm cho các mẫu quân trên một đường
SCORES = {
    "WIN": 1000000,       # 4 quân liên tiếp → thắng ngay
    "OPEN_3": 10000,      # 3 quân, 2 đầu trống → gần thắng, nguy hiểm nhất
    "HALF_OPEN_3": 1000,  # 3 quân, 1 đầu trống, 1 đầu bị chặn
    "OPEN_2": 100,        # 2 quân, 2 đầu trống
    "HALF_OPEN_2": 10,    # 2 quân, 1 đầu bị chặn
}


def evaluate_line(line, player, opponent):
    """
    Tính điểm cho một đường đi (mảng 1 chiều: hàng / cột / chéo).
    Quét từ trái sang phải, đếm chuỗi liên tiếp của player
    và kiểm tra 2 đầu có trống không để phân loại điểm.
    """
    score = 0
    i = 0
    n = len(line)

    while i < n:
        if line[i] == player:
            # Đếm độ dài chuỗi quân liên tiếp
            count = 1
            while i + count < n and line[i + count] == player:
                count += 1

            # Kiểm tra 2 đầu của chuỗi
            left_empty = (i > 0 and line[i - 1] == EMPTY)
            right_empty = (i + count < n and line[i + count] == EMPTY)

            if count >= WIN_LENGTH:
                score += SCORES["WIN"]
            elif count == 3:
                if left_empty and right_empty:
                    score += SCORES["OPEN_3"]
                elif left_empty or right_empty:
                    score += SCORES["HALF_OPEN_3"]
            elif count == 2:
                if left_empty and right_empty:
                    score += SCORES["OPEN_2"]
                elif left_empty or right_empty:
                    score += SCORES["HALF_OPEN_2"]
            i += count
        else:
            i += 1
    return score


def get_lines(board):
    """
    Trích xuất tất cả các đường có thể thắng từ bàn cờ:
    tất cả hàng ngang, cột dọc, đường chéo chính và chéo phụ
    (chỉ lấy các đường có độ dài >= WIN_LENGTH).
    """
    lines = []
    size = board.size
    grid = board.grid

    # Hàng ngang
    for r in range(size):
        lines.append(grid[r])

    # Cột dọc
    for c in range(size):
        lines.append([grid[r][c] for r in range(size)])

    # Đường chéo chính (trên trái → dưới phải)
    for d in range(-size + 1, size):
        line = []
        for r in range(size):
            c = r - d
            if 0 <= c < size:
                line.append(grid[r][c])
        if len(line) >= WIN_LENGTH:
            lines.append(line)

    # Đường chéo phụ (trên phải → dưới trái)
    for d in range(2 * size - 1):
        line = []
        for r in range(size):
            c = d - r
            if 0 <= c < size:
                line.append(grid[r][c])
        if len(line) >= WIN_LENGTH:
            lines.append(line)

    return lines


import config


def evaluate(board, is_maximizing=None):
    """
    Tính điểm tổng thể của trạng thái bàn cờ.

    AI là PLAYER_O (Max), người chơi là PLAYER_X (Min).
    - Score > 0 : có lợi cho AI
    - Score < 0 : có lợi cho người chơi

    Nếu USE_ADVANCED_HEURISTIC = True và is_maximizing được truyền vào,
    áp dụng trọng số theo quyền chủ động (bên đến lượt được hưởng thêm 1.5×).

    Trả về (score, is_volatile):
    - is_volatile = True nếu có OPEN_3 trở lên (đe dọa trực tiếp),
      dùng để kích hoạt Search Extension trong minimax/alpha-beta.
    """
    lines = get_lines(board)
    ai_score_raw = 0
    player_score_raw = 0
    is_volatile = False

    for line in lines:
        ai_val = evaluate_line(line, PLAYER_O, PLAYER_X)
        player_val = evaluate_line(line, PLAYER_X, PLAYER_O)

        ai_score_raw += ai_val
        player_score_raw += player_val

        # Đánh dấu volatile nếu có đe dọa OPEN_3 từ bất kỳ bên nào
        if ai_val >= SCORES["OPEN_3"] or player_val >= SCORES["OPEN_3"]:
            is_volatile = True

    if getattr(config, 'USE_ADVANCED_HEURISTIC', False) and is_maximizing is not None:
        # Bên đến lượt có quyền chủ động, được nhân hệ số cao hơn
        if is_maximizing:
            score = ai_score_raw * 1.5 - player_score_raw * 1.1
        else:
            score = ai_score_raw * 1.0 - player_score_raw * 1.5
    else:
        # Heuristic tĩnh mặc định
        score = ai_score_raw - player_score_raw * 1.1

    return score, is_volatile
