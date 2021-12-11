class Board:
    
    def __init__(self, render = True):
        self.board = [[0,0,0] for _ in range(3)]
        self.player = 1 
        self.repr = {0:'.', 1:'x', -1:'o'}
        self.render = render

    def get_winner(self):
       
       # Horizontal win
        for i in range(3):
           if abs(sum(self.board[i])) ==3:
               #print('H win')
               return self.board[i][0]
        
        # Vertical win   
        for i in range(3):
            if abs(sum(self.board[j][i] for j in range(3))) == 3:
                #print('V win')
                return self.board[0][i]   
                
        # Diagonal win(L-R)
        for i in range(3):
            
                
                # Diagonal win(L-R)
                if abs(sum(self.board[i][i] for i in range(3))) ==3:
                    #print(' D L-R win')
                    return self.board [0][0]
                
                # Diagonal win(R-L)
                if abs(sum(self.board[i][2-i] for i in range(3))) == 3:
                    #print(' D R-L win')
                    return self.board [0][2]
                
        return None
    
    def get_state(self):
        return str(self.board)
        
    def get_valid_actions(self):
        actions = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] ==0:
                    actions.append((row, col))
            
        return actions
    
    def is_ended(self):
        
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    return False
        return True
    
    def _print(self):
        
        for row in self.board:
            for item in row:
                print('  ',self.repr[item], end ='\t')
            print('\n')
        print('#'*25,'\n')
    
    def play(self, x, y):
        
        if self.render:
            if self.player == 1:
                print("\n ------------------------\n      'o' to move: \n ------------------------\n\n")
            if self.player ==-1:
                print("\n ------------------------\n      'x' to move: \n ------------------------\n\n")
            
        if self.board [x][y] !=0:
            return None
    
        self.board[x][y] = self.player
        
        if self.render:
            self._print()
                   
        winner = self.get_winner()

        if winner:
            return winner 

        self.player *=-1
        
        return None