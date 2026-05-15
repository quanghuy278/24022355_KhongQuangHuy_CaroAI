# src/ai/evaluate.py
from config import WIN_LENGTH, PLAYER_X, PLAYER_O, EMPTY

# Trọng số điểm cho các trường hợp
SCORES = {
    "WIN": 1000000,       # 4 quân liên tiếp (Thắng luôn)
    "OPEN_3": 10000,      # 3 quân 2 đầu trống (Gần thắng)
    "HALF_OPEN_3": 1000,  # 3 quân 1 đầu trống, 1 đầu bị chặn
    "OPEN_2": 100,        # 2 quân 2 đầu trống
    "HALF_OPEN_2": 10,    # 2 quân 1 đầu bị chặn
}

def evaluate_line(line, player, opponent):
    """Đánh giá điểm của 1 đường (mảng 1 chiều)"""
    score = 0
    i = 0
    n = len(line)
    
    while i < n:
        if line[i] == player:
            count = 1
            while i + count < n and line[i + count] == player:
                count += 1
            
            # Kiểm tra 2 đầu
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
    """Trích xuất tất cả các hàng, cột, đường chéo từ bàn cờ"""
    lines = []
    size = board.size
    grid = board.grid
    
    # Hàng ngang
    for r in range(size):
        lines.append(grid[r])
        
    # Cột dọc
    for c in range(size):
        lines.append([grid[r][c] for r in range(size)])
        
    # Đường chéo chính (trên trái xuống dưới phải)
    for d in range(-size + 1, size):
        line = []
        for r in range(size):
            c = r - d
            if 0 <= c < size:
                line.append(grid[r][c])
        if len(line) >= WIN_LENGTH:
            lines.append(line)
            
    # Đường chéo phụ (trên phải xuống dưới trái)
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
    Tính điểm của trạng thái bàn cờ.
    Bởi vì AI là PLAYER_O (Max), Người chơi là PLAYER_X (Min).
    Score > 0 có lợi cho AI, Score < 0 có lợi cho người chơi.
    Trả về (score, is_volatile)
    is_volatile = True nếu bàn cờ đang ở trạng thái có đe dọa trực tiếp (vd: Open 3)
    """
    score = 0
    lines = get_lines(board)
    
    ai_score_raw = 0
    player_score_raw = 0
    
    is_volatile = False
    
    for line in lines:
        ai_val = evaluate_line(line, PLAYER_O, PLAYER_X)
        player_val = evaluate_line(line, PLAYER_X, PLAYER_O)
        
        ai_score_raw += ai_val
        player_score_raw += player_val
        
        # Kiểm tra tính biến động khốc liệt (có đe dọa sinh tử)
        if ai_val >= SCORES["OPEN_3"] or player_val >= SCORES["OPEN_3"]:
            is_volatile = True

    if getattr(config, 'USE_ADVANCED_HEURISTIC', False) and is_maximizing is not None:
        # TÍNH QUYỀN CHỦ ĐỘNG (INITIATIVE)
        # Nếu is_maximizing = True => Lượt tiếp theo là của AI (Max). Nghĩa là Người chơi vừa đi xong.
        # Nếu is_maximizing = False => Lượt tiếp theo là của Người (Min). Nghĩa là AI vừa đi xong.
        
        if is_maximizing:
            # Tới lượt AI đi. AI có quyền chủ động.
            # Nếu AI có OPEN_3, AI sẽ thắng ngay, thưởng mạnh.
            score = ai_score_raw * 1.5 - player_score_raw * 1.1
        else:
            # Tới lượt người chơi đi. Người chơi có quyền chủ động.
            score = ai_score_raw * 1.0 - player_score_raw * 1.5
    else:
        # Chế độ tĩnh mặc định
        score = ai_score_raw - player_score_raw * 1.1 
        
    return score, is_volatile

