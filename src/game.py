# src/game.py
from src.board import Board
from src.ai.minimax import get_best_move_minimax
from src.ai.alphabeta import get_best_move_alphabeta
import config

class Game:
    def __init__(self, use_gui=True):
        self.board = Board()
        self.current_player = config.PLAYER_X # Người luôn đi trước
        self.is_game_over = False
        self.winner = None
        self.use_gui = use_gui
        self.last_ai_time = 0
        self.last_ai_nodes = 0
        self.last_move = None
        self.win_coords = None
        
    def reset(self):
        self.board = Board()
        self.current_player = config.PLAYER_X
        self.is_game_over = False
        self.winner = None
        self.last_ai_time = 0
        self.last_ai_nodes = 0
        self.last_move = None
        self.win_coords = None
        
    def switch_turn(self):
        self.current_player = config.PLAYER_O if self.current_player == config.PLAYER_X else config.PLAYER_X
        
    def check_game_state(self):
        is_over, winner = self.board.is_game_over()
        if is_over:
            self.is_game_over = True
            self.winner = winner
            if winner:
                self.win_coords = self.board.get_winning_line(winner)
            
    def handle_human_move(self, row, col):
        if self.board.make_move(row, col, config.PLAYER_X):
            self.last_move = (row, col)
            self.check_game_state()
            if not self.is_game_over:
                self.switch_turn()
                
    def make_ai_move(self):
        if self.is_game_over: return
        
        print(f"AI đang suy nghĩ bằng thuật toán {config.AI_ALGO} ở độ sâu {config.MAX_DEPTH}...")
        
        if config.AI_ALGO == "minimax":
            result = get_best_move_minimax(self.board, config.MAX_DEPTH)
        else:
            result = get_best_move_alphabeta(self.board, config.MAX_DEPTH)
            
        move = result.move
        if move:
            self.board.make_move(move[0], move[1], config.PLAYER_O)
            self.last_move = (move[0], move[1])
            self.last_ai_time = result.time_ms
            self.last_ai_nodes = result.states_visited
            
            print(f"AI đánh: {move}, Điểm: {result.score}, Duyệt: {result.states_visited} nodes, Thời gian: {result.time_ms:.2f} ms")
            
            self.check_game_state()
            if not self.is_game_over:
                self.switch_turn()

    def run_gui(self):
        from src.ui.gui import GUI
        import pygame
        gui = GUI(self)
        clock = pygame.time.Clock()
        
        while True:
            gui.handle_events()
            
            if getattr(gui, 'state', 'PLAYING') == 'PLAYING' and self.current_player == config.PLAYER_O and not self.is_game_over:
                gui.draw() # Vẽ trước khi AI nghĩ
                self.make_ai_move()
                
            gui.draw()
            clock.tick(30)
