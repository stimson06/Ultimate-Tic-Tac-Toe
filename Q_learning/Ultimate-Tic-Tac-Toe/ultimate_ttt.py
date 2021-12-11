from itertools import combinations

class Board:
    
    def __init__(self, render = True):
        self.board = [[[0,0,0],[0,0,0],[0,0,0]] for _ in range(9)]
        self.player = 1 
        self.repr = {0:'.', 1:'x', -1:'o', 0.01:'*'}
        self.next_play = {(1,1):1, (1,2):2, (1,3):3, (2,1):4, (2,2):5, (2,3):6, (3,1):7, (3,2):8, (3,3):9}
        self.render = render
        self.board_sq = []
        self.init_board ()
        self.prev_move = (1, 1, 1)
        
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
            
    def _print(self):
        count = 0
        print('|--------------------|')
        print('|',  sep=' ', end='', flush=True)
        for space in self.board_sq:
            count += 1
            print(self.repr[self.board[space[0]][space[1]][space[2]]], sep=' ', end=' ', flush=True)
            if count%9 == 0:
                print('|\n',  sep=' ', end='', flush=True)
            if count>0 and count%3 == 0:
                print('|',  sep=' ', end='', flush=True)
            if count%27 == 0:
                print('--------------------|',  sep=' ', end='', flush=True)
                print('\n|',  sep=' ', end='', flush=True)
     
    def lock_board(self, won_boards):
        """ This function locks all the empty spaces with '*'
            if player/bot won the sub-board

        Args:
            won_boards : Boards that are won by the player/bot. """
        
        # lock the empty spaces in the won board
        for sub_board in won_boards:
            for row in range(3):
                for col in range(3):
                    if self.board[sub_board-1][row][col] == 0:
                        self.board[sub_board-1][row][col] = 0.01 
    
    def get_winner(self):
        
                       #-- Horizontal wins --#    #---Vertical Wins ----#   # Diagonal Win #
        wining_pos = [(1,2,3), (4,5,6), (7,8,9), (1,4,7), (2,5,8), (3,6,9), (1,5,9), (3,5,7)]
        won_boards = [[],[]]
        player = []
        
        for sub_board in range(0,9):
            # Horizontal win
            for i in range(3):
                if (sum(self.board[sub_board][i])) == 3:
                    #print('H win')
                    won_boards[0].append(sub_board+1)
                if (sum(self.board[sub_board][i])) == -3:
                    #print('H win')
                    won_boards[1].append(sub_board+1)
                   
                    
            
            # Vertical win   
            for i in range(3):
                if (sum(self.board[sub_board][j][i] for j in range(3))) == 3:
                    #print('V win')
                    won_boards[0].append(sub_board+1)
                    
                if (sum(self.board[sub_board][j][i] for j in range(3))) == -3:
                    #print('V win')
                    won_boards[1].append(sub_board+1)
                    
                    
            # Diagonal win(L-R)
            for i in range(3):
                
                    
                    # Diagonal win(L-R)
                    if (sum(self.board[sub_board][i][i] for i in range(3))) ==3:
                        #print(' D L-R win')
                        won_boards[0].append(sub_board+1)    
                        
                    if (sum(self.board[sub_board][i][i] for i in range(3))) ==-3:
                        #print(' D L-R win')
                        won_boards[1].append(sub_board+1)                    
                    
                    # Diagonal win(R-L)
                    if (sum(self.board[sub_board][i][2-i] for i in range(3))) == 3:
                        #print(' D R-L win')
                        won_boards[0].append(sub_board+1)
                    if (sum(self.board[sub_board][i][2-i] for i in range(3))) == -3:
                        #print(' D R-L win')
                        won_boards[1].append(sub_board+1)
            
        # Lock all other positions if a board is won
        for won_board in won_boards:            
            if len(list(set(won_board))) >=1:
                self.lock_board(list(set(won_board)))
        
        player = 1      
        for won_board in won_boards:
            
            if len(list(set(won_board))) >=3:       
                board_combinations =  combinations(won_board,3)    
                #print('Checking',won_boards)
                for comb in board_combinations:
                    comb = tuple(sorted(comb))
                    if comb in wining_pos:
                        #print("Player  won" ,self.repr[player])
                        return player
            player *=-1
        
        #print(won_boards)
        return None
         
    def is_ended(self):
        """ Checks if the game is draw between the player/bot. """
        
        # Check for the empty space in all the sub-boards
        space_available = 0
        for board in range(0,9):
            for row in range(3):
                for col in range(3):
                    if self.board[board][row][col] == 0:
                        space_available +=1
         
        # Return True if there is no moves left               
        if space_available >0:
            return False
        else:
            return True
    
    def get_state(self):
        return str(self.board)
     
    def previous_move(self):
        return self.prev_move
       
    def get_valid_actions(self):
        
        prev_mov = self.previous_move()
        remaining_board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        #print(prev_mov)
        # Find the sub-board to play
        #print(prev_mov)
        prev_mov = (prev_mov[1], prev_mov[2])
        #print(prev_mov)
        for key, value in self.next_play.items():
            if key == prev_mov:
                sub_board = value
                
        # Append the possible moves in the sub-board if available into actions
        actions = []
        for  row in range (3):
            for col in range(3):
                if self.board[sub_board-1][row][col] == 0:
                    actions.append((sub_board, row+1, col+1))
                    
        # Append possible move if sub-board is won/draw into actions
        if len(actions) ==0:  
            remaining_board.remove(sub_board)
            for board in remaining_board:
                #print('chosen board:', board)
                for  row in range (3):
                    for col in range(3):
                        if self.board[board-1][row][col] == 0:
                            actions.append((board, row+1, col+1))
        
        #print(actions)
        return actions

    def play(self, board, row, col):
        
        if self.render:
            if self.player == 1:
                print("\n ------------------------\n      'o' to move: \n ------------------------\n")
            if self.player ==-1:
                print("\n ------------------------\n      'x' to move: \n ------------------------\n")
        
        if self.board[board-1][row-1][col-1] !=0:
            return None
        
        self.board[board-1][row-1][col-1] = self.player
        
        if self.render:
            self._print()
        
        winner = self.get_winner()
        
        if winner:
            return winner
        
        self.player *=-1
        
        return None    