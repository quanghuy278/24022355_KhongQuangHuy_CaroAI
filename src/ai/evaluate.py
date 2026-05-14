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

def evaluate(board):
    """
    Tính điểm của trạng thái bàn cờ.
    Bởi vì AI là PLAYER_O (Max), Người chơi là PLAYER_X (Min).
    Score > 0 có lợi cho AI, Score < 0 có lợi cho người chơi.
    """
    score = 0
    lines = get_lines(board)
    
    for line in lines:
        # Điểm của máy
        score += evaluate_line(line, PLAYER_O, PLAYER_X)
        # Điểm của người (trừ đi)
        # Sử dụng trọng số cao hơn một chút cho người chơi để AI ưu tiên phòng thủ khi người chơi sắp thắng
        score -= evaluate_line(line, PLAYER_X, PLAYER_O) * 1.1 
        
    return score
