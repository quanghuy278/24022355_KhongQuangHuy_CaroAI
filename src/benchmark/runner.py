# src/benchmark/runner.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from rich.console import Console
from rich.table import Table
from src.benchmark.states import BENCHMARK_STATES
from src.ai.minimax import get_best_move_minimax
from src.ai.alphabeta import get_best_move_alphabeta

def run_benchmark():
    console = Console()
    console.print("[bold green]BẮT ĐẦU CHẠY BENCHMARK SO SÁNH MINIMAX VÀ ALPHA-BETA[/bold green]\n")
    
    depths_to_test = [1, 2, 3] # Thử nghiệm ở độ sâu 1, 2, 3
    
    table = Table(title="Kết quả Thực nghiệm")
    
    table.add_column("Trạng thái", style="cyan")
    table.add_column("Depth", justify="right")
    table.add_column("Thuật toán", style="magenta")
    table.add_column("Nước đi", justify="center")
    table.add_column("Điểm", justify="right")
    table.add_column("Số trạng thái xét", justify="right")
    table.add_column("Thời gian (ms)", justify="right")
    table.add_column("Nhận xét", style="yellow")
    
    for state_name, board in BENCHMARK_STATES.items():
        for depth in depths_to_test:
            # Chạy Minimax
            board_minimax = board.copy()
            res_mm = get_best_move_minimax(board_minimax, depth)
            
            # Chạy Alpha-Beta
            board_ab = board.copy()
            res_ab = get_best_move_alphabeta(board_ab, depth)
            
            # Kiểm tra tính đúng đắn
            match_score = "Khớp" if res_mm.score == res_ab.score else "Lệch"
            pruned = res_mm.states_visited - res_ab.states_visited
            percent_pruned = (pruned / res_mm.states_visited * 100) if res_mm.states_visited > 0 else 0
            
            table.add_row(
                state_name,
                str(depth),
                "Minimax",
                str(res_mm.move),
                str(res_mm.score),
                str(res_mm.states_visited),
                f"{res_mm.time_ms:.2f}",
                ""
            )
            
            table.add_row(
                "",
                str(depth),
                "Alpha-Beta",
                str(res_ab.move),
                str(res_ab.score),
                str(res_ab.states_visited),
                f"{res_ab.time_ms:.2f}",
                f"Giảm {percent_pruned:.1f}% ({match_score})"
            )
            table.add_section() # Ngăn cách các lượt test
            
    console.print(table)
    
if __name__ == "__main__":
    run_benchmark()
