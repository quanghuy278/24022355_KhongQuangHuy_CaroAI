# Caro AI - Minimax & Alpha-Beta

Dự án cài đặt game Cờ Caro AI (bàn cờ 9x9, luật 4 quân thắng) với giao diện đồ họa. AI được sử dụng hai thuật toán Minimax và Alpha-Beta Pruning.

## Cài đặt thư viện

Mở terminal và chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Cách chạy chương trình

**1. Chơi trực tiếp với AI (Mặc định dùng Alpha-Beta, độ sâu 3)**
```bash
python main.py
```

**2. Chọn thuật toán và độ sâu muốn chơi**
```bash
# Chơi với Minimax độ sâu 2
python main.py --algo minimax --depth 2

# Chơi với Alpha-Beta độ sâu 4
python main.py --algo alphabeta --depth 4
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