from copy import deepcopy
from mcts import *

class Board:
    
    def __init__ (self, board =None ):
            self.player_1 = 'x'
            self.player_2 = 'o'
            self.empty_square = '.'
            self.position = {}
            self. init_board ()
            if board is not None:
                self.__dict__= deepcopy(board.__dict__)
                
    def init_board(self):
        """ Intializing the board with the position. """
        
        for row in range (3):
            for col in range(3):
                self.position[row, col] = self.empty_square
                
    def make_move(self, row, col):
        """ Helps in making a move in desired location
            by player/bot.

        Args:
            row : Row to move
            col : Column to move

        Returns:
            board: Board with the move played. """
            
        # Intializing the board with the previous available board
        board = Board(self)
        
        # Make move if it is an empty space
        if board.position[row, col] == self.empty_square:
            board.position[row, col] = self.player_1
            (board.player_1, board.player_2) = (board.player_2, board.player_1)
        
        return board
    
    def is_draw(self):
        """ Check the board if all the positions have been played 
            and returns the draw state.

        Returns:
            Boolean: True(draw), False(not a draw). """
        
        # Check if all the position is played
        for row, col in self.position:
            if self.position[row, col] == self.empty_square:
                return False
            
        return True
    
    def is_win(self):
        """ Checks if the board is in win/not a win state .

        Returns:
            Boolean: True(win), False(not a win). """
        
        #vertical win
        for col in range(3):
            winning_sequence = []
            for row in range(3):
                if self.position[row, col] == self.player_2:
                    winning_sequence.append((row,col))

                if len(winning_sequence) == 3:
                    
                    return True
                
        # horizontal win
        for row in range(3):
            winning_sequence = []
            for col in range(3):
                if self.position[row, col] == self.player_2:
                    winning_sequence.append((row,col))

                if len(winning_sequence) == 3:
                   
                    return True
                
        # diagonal win( L- R)
        winning_sequence=[]
        for row in range(3):
            col = row
            if self.position[row, col] == self.player_2:
                winning_sequence.append((row,col))

            if len(winning_sequence) == 3:
                return True
            
        # diagonal win(R - L)
        winning_sequence= []
        for row in range(3):
            col = 3- row -1
            if self.position[row, col] == self.player_2:
                winning_sequence.append((row,col))

            if len(winning_sequence) == 3:
                return True
                
        return False 
    
    def generate_states(self ):
        """ Loops over the board and generates all the possible
            moves that can be played.

        Returns:
            actions: list of all possible positions in the board.
        """
        
        # List to store all the possible board moves
        actions = []
        
        # check for the empty positions in the board and append to actions
        for row, col in self.position:
            if self.position[row, col] == self.empty_square:
                actions.append(self.make_move(row,col))
        
        return actions
    
    def game_loop(self):
        """ Loops the game untill win/draw state is achieved. """

                
        print("Type 'exit' to quit the game")
        print('Move (row, col) :')
        
        # Print the inital empty board
        print(self)
        
        # Intializing Monte Carlo module
        mcts = MCTS()
        
        # Loop untill win/draw state is achieved
        while True:
            
            # user input
            user = input('> ' )
        
            # Different user inputs
            if user == 'exit':
                break
            if user == '':
                continue

            try:
                # Map the user input to the variables
                row, col = (map(int, user.split(',')))
                row, col = row-1, col-1
                
                # Make a move (player)
                if self.position[row, col] == self.empty_square:
                    self = self.make_move(row, col)
                    
                    # Make a move (AI)
                    best_move = mcts.search(self)
                    try:
                        self = best_move.board
                    except :
                        pass
                        
                    # Print the board after moves
                    print(self)
                    
                    # Check for the win state
                    if self.is_win():
                        print("Player '%s' won" % self.player_2 )
                        break
                    
                    # Check for the draw state
                    elif self.is_draw():
                        print('Match Tie, Better Luck next time!')
                        break
                    
                # Illegal user inputs (for already played position)
                else:
                    print('Illegal move')
                    continue
            
            # Invalid inputs by the user
            except Exception as e:
                print('Error :', e)
                print('Invalid input / illegal move ')
                
    def __str__ (self ):
        """ Magic funtion to print the board. """
        
        board_string = ''
        for row in range (3):
            for col in range(3):
                board_string += ' %s' % self.position[row, col]
            board_string +='\n'
            
        if self.player_1 == 'x':
            board_string = '\n ----------------\n "x" to move: \n ----------------\n' + board_string
        elif self.player_1 == 'o':
            board_string = '\n ----------------\n "o" to move: \n ----------------\n' + board_string
        
        return board_string
                
# Main
if __name__ == '__main__':
    
    # Intialize board class
    board = Board()
        
    # Start playing
    board.game_loop()
 