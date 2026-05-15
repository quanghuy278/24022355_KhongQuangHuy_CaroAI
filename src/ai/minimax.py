# src/ai/minimax.py
import time
from src.ai.evaluate import evaluate
from config import PLAYER_X, PLAYER_O

class MinimaxResult:
    def __init__(self, move, score, states_visited, time_ms):
        self.move = move
        self.score = score
        self.states_visited = states_visited
        self.time_ms = time_ms

def minimax_search(board, depth, is_maximizing):
    """Đệ quy Minimax"""
    is_over, winner = board.is_game_over()
    
    if is_over:
        if winner == PLAYER_O:
            return None, 10000000 + depth # Ưu tiên thắng nhanh
        elif winner == PLAYER_X:
            return None, -10000000 - depth # Tránh thua nhanh
        else:
            return None, 0 # Hòa
            
    if depth <= 0:
        score, _ = evaluate(board, is_maximizing)
        return None, score
        
    candidates = board.get_candidate_moves()
    if not candidates:
        return None, 0
        
    best_move = candidates[0]
    states_visited = 1 # Đếm node hiện tại
    
    if is_maximizing:
        best_score = -float('inf')
        for r, c in candidates:
            board.make_move(r, c, PLAYER_O)
            _, score, child_states = minimax_recursive(board, depth - 1, False)
            board.grid[r][c] = '.' # Hoàn tác
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
            board.grid[r][c] = '.' # Hoàn tác
            board.move_count -= 1
            
            states_visited += child_states
            if score < best_score:
                best_score = score
                best_move = (r, c)
        return best_move, best_score, states_visited

def minimax_recursive(board, depth, is_maximizing, extensions=0):
    """Hàm đệ quy trả về (move, score, states_visited)"""
    is_over, winner = board.is_game_over()
    if is_over:
        if winner == PLAYER_O: return None, 10000000 + depth, 1
        elif winner == PLAYER_X: return None, -10000000 - depth, 1
        else: return None, 0, 1
        
    import config
    if depth <= 0:
        score, is_volatile = evaluate(board, is_maximizing)
        # Search Extension
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
    start_time = time.time()
    move, score, states_visited = minimax_recursive(board, depth, True) # AI luôn là Max
    time_ms = (time.time() - start_time) * 1000
    return MinimaxResult(move, score, states_visited, time_ms)
