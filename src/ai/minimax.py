# src/ai/minimax.py - Thuật toán Minimax tìm nước đi tốt nhất cho AI
import time
from src.ai.evaluate import evaluate
from config import PLAYER_X, PLAYER_O


class MinimaxResult:
    """Lưu kết quả trả về của một lần chạy Minimax."""

    def __init__(self, move, score, states_visited, time_ms):
        self.move = move                    # Nước đi tốt nhất (row, col)
        self.score = score                  # Điểm đánh giá của nước đi đó
        self.states_visited = states_visited  # Tổng số node đã duyệt
        self.time_ms = time_ms              # Thời gian chạy (milliseconds)


def minimax_search(board, depth, is_maximizing):
    """
    Hàm đệ quy Minimax cơ bản (không có Search Extension).
    AI (PLAYER_O) là Max, người chơi (PLAYER_X) là Min.
    Duyệt toàn bộ cây đến độ sâu depth.
    Trả về (best_move, best_score, states_visited).
    """
    is_over, winner = board.is_game_over()

    # Trường hợp kết thúc: thưởng/phạt thêm depth để ưu tiên thắng nhanh / tránh thua nhanh
    if is_over:
        if winner == PLAYER_O:
            return None, 10000000 + depth
        elif winner == PLAYER_X:
            return None, -10000000 - depth
        else:
            return None, 0

    if depth <= 0:
        score, _ = evaluate(board, is_maximizing)
        return None, score

    candidates = board.get_candidate_moves()
    if not candidates:
        return None, 0

    best_move = candidates[0]
    states_visited = 1  # Đếm node hiện tại

    if is_maximizing:
        best_score = -float('inf')
        for r, c in candidates:
            board.make_move(r, c, PLAYER_O)
            _, score, child_states = minimax_recursive(board, depth - 1, False)
            board.grid[r][c] = '.'  # Hoàn tác nước đi
            board.move_count -= 1

            states_visited += child_states
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move, best_score, states_visited
    else:
        best_score = float('inf')
        for r, c in candidates:
            board.make_move(r, c, PLAYER_X)
            _, score, child_states = minimax_recursive(board, depth - 1, True)
            board.grid[r][c] = '.'  # Hoàn tác nước đi
            board.move_count -= 1

            states_visited += child_states
            if score < best_score:
                best_score = score
                best_move = (r, c)
        return best_move, best_score, states_visited


def minimax_recursive(board, depth, is_maximizing, extensions=0):
    """
    Hàm đệ quy Minimax có hỗ trợ Search Extension.
    Nếu USE_ADVANCED_HEURISTIC = True và bàn cờ ở trạng thái biến động
    (is_volatile = True từ evaluate), tự động tăng thêm 1 depth để tìm sâu hơn
    (tối đa 1 lần mở rộng, kiểm soát bằng biến extensions).
    Trả về (best_move, best_score, states_visited).
    """
    is_over, winner = board.is_game_over()
    if is_over:
        if winner == PLAYER_O: return None, 10000000 + depth, 1
        elif winner == PLAYER_X: return None, -10000000 - depth, 1
        else: return None, 0, 1

    import config
    if depth <= 0:
        score, is_volatile = evaluate(board, is_maximizing)
        # Search Extension: nếu đang biến động và chưa mở rộng, tăng thêm 1 depth
        if getattr(config, 'USE_ADVANCED_HEURISTIC', False):
            if is_volatile and extensions < 1:
                depth += 1
                extensions += 1
            else:
                return None, score, 1
        else:
            return None, score, 1

    candidates = board.get_candidate_moves()
    if not candidates:
        return None, 0, 1

    best_move = candidates[0]
    states_visited = 1

    if is_maximizing:
        best_score = -float('inf')
        for r, c in candidates:
            board.make_move(r, c, PLAYER_O)
            _, score, child_states = minimax_recursive(board, depth - 1, False, extensions)
            board.grid[r][c] = '.'
            board.move_count -= 1
            states_visited += child_states
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move, best_score, states_visited
    else:
        best_score = float('inf')
        for r, c in candidates:
            board.make_move(r, c, PLAYER_X)
            _, score, child_states = minimax_recursive(board, depth - 1, True, extensions)
            board.grid[r][c] = '.'
            board.move_count -= 1
            states_visited += child_states
            if score < best_score:
                best_score = score
                best_move = (r, c)
        return best_move, best_score, states_visited


def get_best_move_minimax(board, depth):
    """
    Hàm giao tiếp chính cho Minimax.
    Gọi minimax_recursive() với AI là lượt Max (is_maximizing=True),
    đo thời gian chạy và đóng gói kết quả vào MinimaxResult.
    """
    start_time = time.time()
    move, score, states_visited = minimax_recursive(board, depth, True)
    time_ms = (time.time() - start_time) * 1000
    return MinimaxResult(move, score, states_visited, time_ms)
