# src/benchmark/runner.py - Chạy benchmark so sánh hiệu năng Minimax và Alpha-Beta
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Thêm thư mục gốc vào sys.path để import các module dự án
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from rich.console import Console
from rich.table import Table
from src.benchmark.states import BENCHMARK_STATES
from src.ai.minimax import get_best_move_minimax
from src.ai.alphabeta import get_best_move_alphabeta


def run_benchmark():
    """
    Chạy thực nghiệm so sánh Minimax và Alpha-Beta trên các trạng thái bàn cờ mẫu.

    Với mỗi cặp (trạng thái bàn cờ, độ sâu):
    - Chạy Minimax và Alpha-Beta trên bản sao bàn cờ riêng biệt.
    - So sánh điểm trả về (phải khớp nhau vì Alpha-Beta là tối ưu hóa của Minimax).
    - Tính % số node được cắt tỉa bởi Alpha-Beta so với Minimax.
    - In kết quả ra bảng đẹp bằng thư viện rich.
    """
    console = Console()
    console.print("[bold green]BẮT ĐẦU CHẠY BENCHMARK SO SÁNH MINIMAX VÀ ALPHA-BETA[/bold green]\n")

    depths_to_test = [1, 2, 3]  # Thử nghiệm ở 3 mức độ sâu

    # Tạo bảng kết quả
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
            # Chạy Minimax trên bản sao riêng
            board_minimax = board.copy()
            res_mm = get_best_move_minimax(board_minimax, depth)

            # Chạy Alpha-Beta trên bản sao riêng
            board_ab = board.copy()
            res_ab = get_best_move_alphabeta(board_ab, depth)

            # Kiểm tra tính đúng đắn: điểm 2 thuật toán phải bằng nhau
            match_score = "Khớp" if res_mm.score == res_ab.score else "Lệch"

            # Tính % node được cắt tỉa
            pruned = res_mm.states_visited - res_ab.states_visited
            percent_pruned = (pruned / res_mm.states_visited * 100) if res_mm.states_visited > 0 else 0

            # Thêm hàng Minimax
            table.add_row(
                state_name, str(depth), "Minimax",
                str(res_mm.move), str(res_mm.score),
                str(res_mm.states_visited), f"{res_mm.time_ms:.2f}", ""
            )

            # Thêm hàng Alpha-Beta (kèm nhận xét % cắt tỉa)
            table.add_row(
                "", str(depth), "Alpha-Beta",
                str(res_ab.move), str(res_ab.score),
                str(res_ab.states_visited), f"{res_ab.time_ms:.2f}",
                f"Giảm {percent_pruned:.1f}% ({match_score})"
            )

            table.add_section()  # Ngăn cách các lượt test

    console.print(table)


if __name__ == "__main__":
    run_benchmark()
