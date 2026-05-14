# main.py
import argparse
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from src.game import Game
import config

def main():
    parser = argparse.ArgumentParser(description="Caro AI - Minimax & Alpha-Beta")
    parser.add_argument("--algo", type=str, choices=["minimax", "alphabeta"], help="Thuật toán AI sử dụng (minimax/alphabeta)")
    parser.add_argument("--depth", type=int, help="Độ sâu tìm kiếm")
    
    args = parser.parse_args()
    
    if args.algo:
        config.AI_ALGO = args.algo
    if args.depth:
        config.MAX_DEPTH = args.depth
        
    print(f"Khởi động Game Caro với AI: {config.AI_ALGO.upper()} (Độ sâu: {config.MAX_DEPTH})")
    game = Game(use_gui=True)
    game.run_gui()

if __name__ == "__main__":
    main()
