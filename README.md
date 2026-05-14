# Caro AI - Minimax & Alpha-Beta

Dự án cài đặt game Cờ Caro AI (bàn cờ 9x9, luật 4 quân thắng) với giao diện đồ họa. AI được sử dụng hai thuật toán Minimax và Alpha-Beta Pruning.

## Cài đặt thư viện

Mở terminal và chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```
*(**Lưu ý:** Dự án sử dụng `pygame-ce` (Pygame Community Edition) để tương thích tốt hơn với các phiên bản Python mới nhất (3.12+). Nếu bạn đã cài đặt `pygame` gốc từ trước và gặp lỗi xung đột, vui lòng gỡ cài đặt nó bằng lệnh `pip uninstall pygame` trước khi chạy lệnh trên).*

## Cách chạy chương trình

**1. Chơi trực tiếp với AI**
Chạy lệnh sau để khởi động game:
```bash
python main.py
```
Giao diện Menu sẽ hiện ra cho phép bạn chọn thuật toán (Minimax hoặc Alpha-Beta) để bắt đầu. Theo mặc định, độ sâu tìm kiếm của AI là 3.

**2. Tùy chỉnh tham số qua dòng lệnh (Command Line)**
Bạn có thể cấu hình độ sâu tìm kiếm bằng tham số `--depth` (thuật toán AI vẫn được chọn ở màn hình Menu):
```bash
# Cấu hình độ sâu tìm kiếm là 2
python main.py --depth 2

# Ngoài ra, cũng có thể cấu hình tham số thuật toán (mặc dù Menu vẫn sẽ hiển thị)
python main.py --algo minimax --depth 2
```

**3. Chạy chương trình kiểm thử (Benchmark)**
Đánh giá và so sánh thời gian, số lượng trạng thái duyệt giữa Minimax và Alpha-Beta:
```bash
python -m src.benchmark.runner
```

## Cấu trúc thư mục

- `src/board.py`: Cấu trúc dữ liệu bàn cờ, kiểm tra thắng thua.
- `src/ai/evaluate.py`: Hàm đánh giá (Heuristic) trạng thái bàn cờ.
- `src/ai/minimax.py`: Cài đặt thuật toán Minimax thuần.
- `src/ai/alphabeta.py`: Cài đặt thuật toán cắt tỉa Alpha-Beta.
- `src/ui/gui.py`: Giao diện đồ họa bằng thư viện `pygame`.
- `src/benchmark/`: Chứa các trạng thái test và kịch bản benchmark.
- `config.py`: File cấu hình chung của game.