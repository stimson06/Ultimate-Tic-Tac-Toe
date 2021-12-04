from copy import deepcopy
import random
from itertools import combinations
from mcts import *
import traceback

class Board:
    
    def __init__ (self, board =None ):
            self.player_1 = 'x'
            self.player_2 = 'o'
            self.sub_board = None
            self.empty_square = '.'
            self.position = {}
            self.board_sq=[]
            self. init_board ()
            self.next_play = {(1,1):1, (1,2):2, (1,3):3, (2,1):4, (2,2):5, (2,3):6, (3,1):7, (3,2):8, (3,3):9}
            self.prev_mov = []
            if board is not None:
                self.__dict__= deepcopy(board.__dict__)
                
    def init_board(self):
        """ Function to initialize the board with the squecence such that it can be
            easily read. """
        
        # Local boards / sub boards      
        sub_boards = [0,1,2,3,4,5,6,7,8]

        # Generates the sequence of numbers useful for making the ultimate tic-tac-toe board
        for pos in range(0,9,3):
            seq_1 = [[0,0], [0,1], [0,2], [0,0], [0,1], [0,2], [0,0], [0,1], [0,2]]
            seq_2 = [[1,0], [1,1], [1,2], [1,0], [1,1], [1,2], [1,0], [1,1], [1,2]]
            seq_3 = [[2,0], [2,1], [2,2], [2,0], [2,1], [2,2], [2,0], [2,1], [2,2]]
            
            # sequence for 1, 4, 7 row respectively
            for j in range(9):
                if j <3:
                    seq_1[j].insert(0, sub_boards[pos]) 
                if j >=3 and j<6:    
                    seq_1[j].insert(0, sub_boards[pos+1]) 
                if j>=6 and j <9:
                    seq_1[j].insert(0, sub_boards[pos+2]) 
            self.board_sq+=seq_1
                    
            # sequence for 2, 5, 8 row respectively
            for j in range(9):
                if j <3:
                    seq_2[j].insert(0, sub_boards[pos+0])
                if j >=3 and j<6:    
                    seq_2[j].insert(0, sub_boards[pos+1])
                if j>=6 and j <9:
                    seq_2[j].insert(0, sub_boards[pos+2])
            self.board_sq+=seq_2
            
            # sequence for 3, 6, 9 row respectively
            for j in range(9):
                if j <3:
                    seq_3[j].insert(0, sub_boards[pos+0])
                if j >=3 and j<6:    
                    seq_3[j].insert(0, sub_boards[pos+1])
                if j>=6 and j <9:
                    seq_3[j].insert(0, sub_boards[pos+2])
            self.board_sq+=seq_3
            
        # assinging empty_square value('.') in all the subboards
        for intial in range(len(self.board_sq)):
            self.position[self.board_sq[intial][0], self.board_sq[intial][1], self.board_sq[intial][2]] = self.empty_square
                          # sub-board               # row                     # col
   
    def make_move(self, sub_board, row, col):
        """ Function to make a move by the player/bot
            in a specified locations.
            
        Args:
            sub_board : The sub board that player/bot needs to play.
            row : The row in sub board that player/bot needs to play.
            col : The column in sub board that player/bot needs to play.

        Returns:
            board: Complete board where the move has made. """
        
        # Initalizing class with previous made move
        board = Board(self)
        
        # Make a move in the desires location if the space has not been played
        if board.position[sub_board-1, row-1, col-1] == self.empty_square:
            board.position[sub_board-1, row-1, col-1] = self.player_1
            (board.player_1, board.player_2) = (board.player_2, board.player_1) # switching over next player
        
        return board
    
    def previous_move(self):
        """ Helper fucnction for generate states
        
        Returns:
            prev_mov : previous move made by the player. """

        return self.prev_mov  
    
    def generate_states(self ):
        """ Helper fucnction for the bot to generate states/legal moves 
    
        Returns:
            actions: list of possible move according to the rules. """
        
        prev_mov = self.previous_move()
        remaining_board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        # Find the sub-board to play
        prev_mov = (prev_mov[1], prev_mov[2])
        for key, value in self.next_play.items():
            if key == prev_mov:
                sub_board = value
                
        # Append the possible moves in the sub-board if available into actions
        actions = []
        for  row in range (3):
            for col in range(3):
                if self.position[sub_board-1, row, col] == self.empty_square:
                    actions.append(self.make_move(sub_board, row+1, col+1))
                    
        # Append possible move if sub-board is won/draw into actions
        if len(actions) ==0:  
            remaining_board.remove(sub_board)
            for board in remaining_board:
                #print('chosen board:', board)
                for  row in range (3):
                    for col in range(3):
                        if self.position[board-1, row, col] == self.empty_square:
                            actions.append(self.make_move(board, row+1, col+1))
        
        return actions 
    
    def lock_board(self, won_boards):
        """ This function locks all the empty spaces with '*'
            if player/bot won the sub-board

        Args:
            won_boards : Boards that are won by the player/bot. """
        
        # lock the empty spaces in the won board
        for board in won_boards:
            for row in range(3):
                for col in range(3):
                    if self.position[board-1, row, col] == self.empty_square:
                        self.position[board-1, row, col] = '*'
    
    def player_next_move(self, player_move, bot_move):
        """ Helps the player to find the next local board to move 
            with that of move by bot

        Args:
            player_move : Position of the board when player moved
            bot_move ([type]): Position of the board when bot(AI) moved. """
        
        # moves after bot(AI) played
        played_mov = dict(bot_move - player_move)
        
        # find playable board
        board_found = False
        for key, value in played_mov.items():
            if value == 'o' or value == 'x':
                mov = list(key)
                nxt = ((mov[1])+1, (mov[2])+1)
                
                # find the board with the dictionary
                for key, value in self.next_play.items():
                    if nxt == key:
                        for row in range(3):
                            for col in range(3):
                                if self.position[value-1, row, col] == self.empty_square:
                                    board_found = True
                                    self.sub_board = value
                                    
        # If board is full / not found
        if board_found == False: 
            print('Chose board of your choice')
            self.sub_board = None
            
        return      
                        
    def is_win(self):
        """checks if the game is won by player/bot. """
        
                       #-- Horizontal wins --#    #---Vertical Wins ----#   # Diagonal Win #
        wining_pos = [(1,2,3), (4,5,6), (7,8,9), (1,4,7), (2,5,8), (3,6,9), (1,5,9), (3,5,7)]
        won_boards = []
        
        # check for winning positions in each board and add to won_boards
        for board in range(0,9):
            
            # Vertical win
            for col in range(3):
                winning_sequence = []
                for row in range(3):
                    if self.position[board, row, col] == self.player_2:
                        winning_sequence.append((row,col))

                    if len(winning_sequence) == 3:
                        won_boards.append(board+1)
                    
            # Horizontal win
            for row in range(3):
                winning_sequence = []
                for col in range(3):
                    if self.position[board, row, col] == self.player_2:
                        winning_sequence.append((row,col))

                    if len(winning_sequence) == 3:
                    
                        won_boards.append(board+1)
                    
            # Diagonal win( L- R)
            winning_sequence=[]
            for row in range(3):
                col = row
                if self.position[board, row, col] == self.player_2:
                    winning_sequence.append((row,col))

                if len(winning_sequence) == 3:
                    won_boards.append(board+1)
                    
            # Diagonal win(R - L)
            winning_sequence= []
            for row in range(3):
                col = 3- row -1
                if self.position[board, row, col] == self.player_2:
                    winning_sequence.append((row,col))

                if len(winning_sequence) == 3:
                    won_boards.append(board+1)
        
        # Lock all other positions if a board is won            
        if len(list(set(won_boards))) >=1:
            self.lock_board(list(set(won_boards)))
        
        # Check for winning in the global board           
        if len(list(set(won_boards))) >=3:       
            board_combinations =  combinations(won_boards,3)    
            #print('Checking',won_boards)
            for comb in board_combinations:
                comb = tuple(sorted(comb))
                if comb in wining_pos:
                    #print("Player '%s' has won" % self.player_2)
                    return True
                
        return False
            
    def is_draw(self):
        """ Checks if the game is draw between the player/bot. """
        
        # Check for the empty space in all the sub-boards
        space_available = 0
        for board in range(0,9):
            for row in range(3):
                for col in range(3):
                    if self.position[board, row, col] == self.empty_square:
                        space_available +=1
         
        # Return True if there is no moves left               
        if space_available >0:
            return False
        else:
            return True                      

    def game_loop(self):
        """Loops the game untill win/draw state is reached. """
        
        print("Type 'exit' to quit the game")
        
        print(self)
        
        # Intialize Monte Carlo
        mcts = MCTS()
        
        while True:
            
            # Take the input from the player
            if self.sub_board == None:
                user = input('board, row, col > ' )
            else: 
                print('playable board: ',self.sub_board)
                user = input('row, col > ')
            if user == 'exit':
                break
            if user == '':
                continue

            try:
                # Make move desired by user
                if self.sub_board == None:
                    self.sub_board, row, col = (map(int, user.split(',')))
                else:
                    #print('Enter only row, col')
                    row, col = map(int, user.split(','))
                    
                self.prev_mov = [self.sub_board, row, col]
                if self.position[self.sub_board-1, row-1, col-1] == self.empty_square:
                    self = self.make_move(self.sub_board, row, col)
                    player_move = self.position
                    
                    # Bot(AI) turn 
                    print("\nAI Thinking...\n")
                    player_move= set(player_move.items())
                    best_move = mcts.search(self)
                    
                    try:
                        self = best_move.board
                        bot_move = self.position
                        bot_move = set(bot_move.items())
                        
                        
                    except :
                        pass

                    print(self)
                    self.player_next_move(player_move, bot_move)
                    
                    # Check for win / draw state
                    if self.is_win():
                        print("Player '%s' won" % self.player_2 )
                        break
                    elif self.is_draw():
                        print('Match Tie, Better Luck next time!')
                        break
                    
                # If already the position is taken/locked
                else:
                    print('Illegal move')
                    continue
            
            # Invalid input from the user
            except :
                print(traceback.format_exc())
                print('Invalid input / illegal move ')    
                        
    def __str__ (self ):
        """Magic function to print the board"""
        
        board_string = '-------------------------\n|'

        count = 0
        for intial in range(len(self.board_sq)):
            
            if count > 0 and count %3 == 0 :
                board_string +=' |'
            if count > 0 and count %9 == 0:
                board_string += '\n|'
            if count > 0 and count % 27 == 0:
                board_string += '------------------------\n|'
                
            board_string += ' %s' % self.position[self.board_sq[intial][0], self.board_sq[intial][1], self.board_sq[intial][2]]
            count+=1
        
        board_string += ' |\n-------------------------\n'
            
        if self.player_1 == 'x':
            board_string = '\n ------------------------\n      "x" to move: \n ------------------------\n' + board_string
        elif self.player_1 == 'o':
            board_string = '\n ------------------------\n      "o" to move: \n ------------------------\n' + board_string
    
        return board_string
    
if __name__ == '__main__':

    #Intialize the board
    board = Board()
           
    # Start playing the game           
    board.game_loop() 