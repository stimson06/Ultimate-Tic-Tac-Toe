import random
from tic_tac_toe import Board
from q_learning import Q_learning
from tqdm import tqdm

class Agent:
    """ The Agent class  creates/updates the q-table with the 
        appropriate parameters and values used when playing  """
    
    def __init__(self):
        """ Intializing variables."""
        
        # Epsilon (randomness)
        self.eps = 1.0
        self.qlearner = Q_learning()
        
    def get_actions(self, state, valid_actions):
        """ Picks a random choice on the valid actions
            for the current state in board.

        Args:
            state : Current state of the board.
            valid_actions : Valid actions that can be made.
        Returns:
            best: Random action from the 'valid actions'. """
        
        # Random action other than the highest q-value(randomness)
        if random.random() < self.eps:
            return random.choice(valid_actions)
        
        # Best move with highest calculated Q-value
        best = self.qlearner.get_best_action(state)
        if best is None:
            return random.choice(valid_actions)
        
        return best
    
    def learn_one_game(self):
        """ Simulates a single game and updates the Q-value
             in the Q-table. """
        
        # Intialize the game board (No print)
        game = Board(render = False)
        
        while True:
            
            # Get state & actions of the current board 
            state = game.get_state()
            action = self.get_actions(state, game.get_valid_actions())
            winner = game.play(*action)
            
            # agent wins 
            if winner or game.is_ended():
                self.qlearner.update(state, action, game.get_state(), 100)
                break
                
            winner = game.play(*random.choice(game.get_valid_actions()))
            
            # agent losses
            if winner or game.is_ended():
                self.qlearner.update(state, action, game.get_state(), -100)
                break
            
            # No win / loss
            self.qlearner.update(state, action, game.get_state(), 0)
            
    def learn(self, n = 20000):
        """ Repeats the learning cycle for n times.

        Args:
            n : Number of simulations/learning. Defaults to 20000. """
        
        # Simulate the game
        for _ in tqdm(range(n), desc = 'Training AI'):
            self.learn_one_game()
            self.eps -= 0.0001