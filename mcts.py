import math 
import random

class TreeNode():
    """ Initialize the variables that are needed to initialize
        execute the Monter Carlo Tree Search
    """
    
    def __init__(self, board, parent):
        
        self.board = board 
                
        if self.board.is_win() or self.board.is_draw():
            self.is_terminal = True
        else:
            self.is_terminal = False
        
        self.is_fully_expanded = self.is_terminal          
        
        
        self.visits = 0
        self.score = 0
        
        self.parent = parent 
        self.children = {}
        
class MCTS():
    
    def __init__(self):
        """ Intializing the hyperparameter variables """
        
        self.exploration_constant = 0.5 
        self.simulations =10 # depth
    
    def search(self, inital_state):
        """ Searches for the best move in the current position

        Args:
            inital_state : current state of the tic-tac-toe board """
        
        self.root = TreeNode(inital_state, None)
        
        for _ in range(self.simulations):
            node = self.select(self.root) # Selection / Expanding Phase

            score = self.rollout(node.board) # Simulation  Phase
            
            self.backpropagate (node, score)# Backpropagation Phase
        
        # Best move
        try:
            return self.get_best_move(self.root, self.exploration_constant)
        except :
            pass
        
    def select(self, node):
        """ Select a node and expands it full to the terminal state
            adding all the child nodes to the parent node respectively
            
        Args:
            node : Current state of the board

        Returns:
            node: Computed best move by the Tree using 
            score from get_best_move function
        """
        
        # Expand the node until the terminal state
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, self.exploration_constant)
            else:
                return self.expand(node)
            
        return node
    
    def expand(self, node):
        """ Expands the current state and populates the children 
            dictionary with appropriate parent node

        Args:
            node : current state of the game

        Returns:
            new_node: Updated list that has the child nodes
        """
        
        # Generating legal states (actions) for the given node (current state)
        states = node.board.generate_states()
        
        # Adds all the possible states as child node to the parent if not present in the children dictionary
        for state in states:
            
            if str(state.position) not in node.children:
                new_node = TreeNode(state, node)
                node.children[str(state.position)] = new_node
            
                if len(states) == len(node.children):
                    node.is_fully_expanded = True
                    
                #print(new_node)
                return new_node
    
    def rollout(self,board):
        """ Makes a random choice to make an actino on the generate states (legal states)
            and returns a value to maxime the win of AI ('o')

        Args:
            board : Current state of the game 

        Returns:
            +1: If the AI win's
             0: Tie
            -1: If the player wins  """
            
        # makes a random choice on the genrated states as an action
        while not board.is_win():
            try:
                board = random.choice(board.generate_states())
            except:
                return 0 # Tie
            
        
        if board.player_2 == 'x': 
            return 1 # AI wins
        elif board.player_2 == 'o':
            return -1 # player's win
        
    def backpropagate(self,node, score):
        """ Backpropogate all the vaules back to the root node

        Args:
            node : current state of the game
            score : score computed (1,0,-1) by the rollout function
        """
        
        # updating the score & visits to the parent node
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent
        
    def get_best_move(self, node, exploration_constant):
        """ Computes the best move based on the number of visits and scores in each
            nodes using the UCT (Upper Confidence Tree)

        Args:
            node ([type]): Currnet state of the game
            exploration_constant: Constant that controls exploration / exploitation

        Returns:
            best_move: random choice on the best move available
        """
        
        # Define best score and best move
        best_score = float('-inf')
        best_moves = []
        
        # looping over child nodes 
        for child_node in node.children.values():
            if child_node.board.player_2 == 'x':
                current_player = 1 
            elif child_node.board.player_2 == 'o':
                current_player = -1
            
            # UCT formula
            move_score = current_player * child_node.score / child_node.visits + exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))
            
            # update the best_score and append the move to best move to make a random choice
            if move_score > best_score:
                best_score = move_score
                best_moves =[child_node]
            elif move_score == best_score:
                best_moves.append(child_node)
                
        return random.choice(best_moves)