# src/ai/alphabeta.py - Thuật toán Alpha-Beta Pruning (cải tiến của Minimax)
import time
from src.ai.evaluate import evaluate
from config import PLAYER_X, PLAYER_O


class AlphaBetaResult:
    """Lưu kết quả trả về của một lần chạy Alpha-Beta."""

    def __init__(self, move, score, states_visited, time_ms):
        self.move = move                      # Nước đi tốt nhất (row, col)
        self.score = score                    # Điểm đánh giá của nước đi đó
        self.states_visited = states_visited  # Tổng số node đã duyệt
        self.time_ms = time_ms                # Thời gian chạy (milliseconds)


def alphabeta_recursive(board, depth, alpha, beta, is_maximizing, extensions=0):
    """
    Hàm đệ quy Alpha-Beta Pruning có hỗ trợ Search Extension.

    Alpha-Beta cắt tỉa các nhánh không cần duyệt:
    - alpha: điểm tốt nhất Max đã đảm bảo được
    - beta : điểm tốt nhất Min đã đảm bảo được
    - Nếu beta <= alpha: cắt tỉa (không duyệt tiếp nhánh hiện tại)

    Search Extension (khi USE_ADVANCED_HEURISTIC = True):
    Nếu bàn cờ đang biến động (is_volatile = True), tăng thêm 1 depth
    để không bỏ sót mối đe dọa ngay sau node lá (tối đa 1 lần).

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
        # Search Extension: mở rộng nhánh cục bộ nếu cờ đang biến động
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
            _, score, child_states = alphabeta_recursive(board, depth - 1, alpha, beta, False, extensions)
            board.grid[r][c] = '.'
            board.move_count -= 1
            states_visited += child_states

            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)
            if beta <= alpha:  # Cắt tỉa Beta: Min sẽ không chọn nhánh này
                break
        return best_move, best_score, states_visited
    else:
        best_score = float('inf')
        for r, c in candidates:
            board.make_move(r, c, PLAYER_X)
            _, score, child_states = alphabeta_recursive(board, depth - 1, alpha, beta, True, extensions)
            board.grid[r][c] = '.'
            board.move_count -= 1
            states_visited += child_states

            if score < best_score:
                best_score = score
                best_move = (r, c)
            beta = min(beta, best_score)
            if beta <= alpha:  # Cắt tỉa Alpha: Max sẽ không chọn nhánh này
                break
        return best_move, best_score, states_visited


def get_best_move_alphabeta(board, depth):
    """
    Hàm giao tiếp chính cho Alpha-Beta.
    Gọi alphabeta_recursive() với alpha = -∞, beta = +∞, AI là lượt Max,
    đo thời gian chạy và đóng gói kết quả vào AlphaBetaResult.
    """
    start_time = time.time()
    move, score, states_visited = alphabeta_recursive(board, depth, -float('inf'), float('inf'), True)
    time_ms = (time.time() - start_time) * 1000
    return AlphaBetaResult(move, score, states_visited, time_ms)
