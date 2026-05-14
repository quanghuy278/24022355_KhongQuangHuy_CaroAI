# main.py
import argparse
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from src.game import Game
import config

def main():
    parser = argparse.ArgumentParser(description="Caro AI - Minimax & Alpha-Beta")
    parser.add_argument("--depth", type=int, help="Độ sâu tìm kiếm")
    
    args = parser.parse_args()
    
    if args.depth:
        config.MAX_DEPTH = args.depth
        
    print(f"Khởi động Game Caro. Vui lòng chọn thuật toán AI ở giao diện Menu! (Độ sâu: {config.MAX_DEPTH})")
    game = Game(use_gui=True)
    game.run_gui()

if __name__ == "__main__":
    main()
