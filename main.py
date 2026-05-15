# main.py
import argparse
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from src.game import Game
import config

def main():
    print(f"Khởi động Game Caro. Vui lòng chọn thuật toán và độ sâu AI ở giao diện Menu!")
    game = Game(use_gui=True)
    game.run_gui()

if __name__ == "__main__":
    main()
