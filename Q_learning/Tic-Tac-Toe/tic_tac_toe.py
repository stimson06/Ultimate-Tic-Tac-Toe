class Board:
    " Functions requried to build a 3X3 Tic-Tac-Toe board."
    
    def __init__(self, render = True):
        """ Intializing the variables.

        Args:
            render : Printing the board. Defaults to True. """
            
        self.board = [[0,0,0] for _ in range(3)]
        self.player = 1 
        self.repr = {0:'.', 1:'x', -1:'o'}
        self.render = render

    def get_winner(self):
        """ Checks the win state of the board.

        Returns:
            Player / None based on the board state. """
       
       # Horizontal win
        for i in range(3):
           if abs(sum(self.board[i])) ==3:
               return self.board[i][0]
        
        # Vertical win   
        for i in range(3):
            if abs(sum(self.board[j][i] for j in range(3))) == 3:
                return self.board[0][i]   
                
        # Diagonal win
        for i in range(3):
                # Diagonal win(L-R)
                if abs(sum(self.board[i][i] for i in range(3))) ==3:
                    return self.board [0][0]
                
                # Diagonal win(R-L)
                if abs(sum(self.board[i][2-i] for i in range(3))) == 3:
                    return self.board [0][2]
                
        return None
    
    def is_ended(self):
        """ Checks if the game is draw between the player/bot.

        Returns:
            True / False if the board is completely fill(end)
        """
        
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    return False
        return True
    
    def get_state(self):
        """ Returns the board in the string representation. """
        
        return str(self.board)
        
    def get_valid_actions(self):
        """ Creates a list of available actions for the current state.

        Returns:
            actions: Set of available actions in the board. """
        
        # Check for avalilable positions in the board.
        actions = []
        for row in range(3):
            for col in range(3):
                # Append if there is a space in the board
                if self.board[row][col] ==0:
                    actions.append((row, col))
            
        return actions
    
    def _print(self):
        """ Function to print the board. """
        
        for row in self.board:
            for item in row:
                print('  ',self.repr[item], end ='\t')
            print('\n')
        print('#'*25,'\n')
    
    def play(self, row, col):
        """ Function to play the game.

        Args:
            row : Position of row in the board.
            col : Position of row in the board.  """
        
        # Print the players
        if self.render:
            if self.player == 1:
                print("\n ------------------------\n      'o' to move: \n ------------------------\n\n")
            if self.player ==-1:
                print("\n ------------------------\n      'x' to move: \n ------------------------\n\n")
            
        # Return if the position if already taken
        if self.board [row][col] !=0:
            return None
    
        # Make a move in the board
        self.board[row][col] = self.player
        
        # Print the board
        if self.render:
            self._print()
                   
        # Check for the win state
        winner = self.get_winner()
        if winner:
            return winner 

        # Switch players
        self.player *=-1
        
        return None