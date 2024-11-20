import copy
import sys
import pygame
import random
import numpy as np

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(Background)

class Board:
    
    def __init__(self):
        self.Squares = np.zeros ( (ROWS,COLS) )
        self.empty_squares = self.Squares
        self.mark_count = 0
    
    def final(self):
        
        for Col in range(COLS):
            if self.Squares[0][Col] == self.Squares[1][Col] == self.Squares[2][Col] != 0:
                return self.Squares[0][Col]
            
        for Row in range(ROWS):
            if self.Squares[Row][0] == self.Squares[Row][1] == self.Squares[Row][2] != 0:
                return self.Squares[Row][0]
        
            
        if self.Squares[0][0] == self.Squares[1][1] == self.Squares[2][2] != 0:
            return self.Squares[0][0]
        
        if self.Squares[0][2] == self.Squares[1][1] == self.Squares [2][0] != 0:
            return self.Squares[1][1]
        
        return 0
            
    def Mark_Square(self, Row, Col, Player):
        self.Squares[Row][Col] = Player
        self.mark_count += 1
        
    def empty_square(self, Row, Col):
        return self.Squares[Row][Col] == 0
    
    def get_empty(self):
        empty_sqrs = []
        for Row in range(ROWS):
            for Col in range(COLS):
                if self.empty_square(Row,Col):
                    empty_sqrs.append((Row,Col))
        return empty_sqrs
    
    def isfull(self):
        return self.mark_count == 9
    
    def isempty(self):
        return self.mark_count == 0
    
class AI:
    
    def __init__(self, level=1, Player=2):
        self.level = level
        self.player = Player
    
    def rnd_choice(self, Board):
        empty_sqrs = Board.get_empty()
        idx = random.randrange(0 , len(empty_sqrs))
        return empty_sqrs[idx]         
    
    def minimax(self, Board, maximizing):
    
    
        case = Board.final()        
        #Player 1 wins
        
        if case == 1:
            return 1, None 
        
        #Player 2 wins
        
        if case == 2:
            return -1, None
        
        #Draw
        
        elif Board.isfull():
            return 0, None
        
        if maximizing :
            max_eval = -100
            best_move = None
            empty_squares = Board.get_empty()
            
            for (Row, Col) in empty_squares:
                temp_board = copy.deepcopy(Board)
                temp_board.Mark_Square(Row, Col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (Row,Col)
                
            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = Board.get_empty()
            
            for (Row, Col) in empty_sqrs:
                temp_board = copy.deepcopy(Board)
                temp_board.Mark_Square(Row, Col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (Row,Col)
                
            return min_eval, best_move
                
                
        
    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.rnd_choice(main_board)
        else: 
            eval, move = self.minimax(main_board, False)
        
        print(f'AI has chosen to mark square in pos {move} with an eval of {eval}')
        
        return move
    
    
class Game:
    
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.Player = 1
        self.gamemode = 'ai'
        self.running = True
        self.Show_Lines()

    def Show_Lines(self):
        #VERTICALS
        pygame.draw.line(screen, Lines, (SQSIZE ,0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, Lines, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        #HORIZONTALS
        pygame.draw.line(screen, Lines, (0 , SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, Lines, (0, HEIGHT-SQSIZE), (WIDTH, HEIGHT-SQSIZE), LINE_WIDTH)
    
    def draw_fig(self, Row, Col):
        if self.Player == 1:
            #draw Cross
            start_desc = (Col * SQSIZE + OFFSET, Row * SQSIZE + OFFSET)
            end_desc = (Col * SQSIZE + SQSIZE - OFFSET, Row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            start_asc = (Col * SQSIZE + OFFSET, Row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (Col * SQSIZE + SQSIZE - OFFSET, Row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        
        elif self.Player == 2:
            #draw Circle
            center = (Col * SQSIZE + SQSIZE//2, Row * SQSIZE + SQSIZE//2)
            pygame.draw.circle(screen, CIRC_COlOR, center, RADIUS, CIRC_WIDTH)
        
    def Next_Turn(self):
        self.Player = self.Player % 2 + 1
    
    def make_move(self, Row, Col):
        self.board.Mark_Square(Row, Col, self.Player)
        self.draw_fig(Row, Col)
        self.Next_Turn()
def main():
    game = Game()
    board = game.board
    ai = game.ai
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pos = event.pos
                Row = pos[1] // SQSIZE
                Col = pos[0] // SQSIZE
                Row = int(Row)
                Col = int(Col)
                
                if board.empty_square(Row, Col):
                    game.make_move(Row, Col)
        if game.gamemode == 'ai' and game.Player == ai.player:
            pygame.display.update()
            Row, Col = ai.eval(board)
            game.make_move(Row, Col)
        pygame.display.update()
                
main()
