import random 
from ultimate_ttt import Board
from q_learning import Q_learning
from tqdm import tqdm

class Agent:
    
    def __init__(self):
        
        self.eps = 1.0
        self.qlearner = Q_learning()
        
    def get_actions(self, state, valid_actions):
        
        if random.random() < self.eps:
            return random.choice(valid_actions)
        
        best = self.qlearner.get_best_action(state)
        if best is None:
            return random.choice(valid_actions)
        
        return best
    
    def learn_one_game(self):
        
        game = Board(render = False)
        
        while True:
            
            state = game.get_state()
            action = self.get_actions(state, game.get_valid_actions())
            game.prev_move = action
            winner = game.play(*action)
            
            # agent wins 
            if winner or game.is_ended():
                self.qlearner.update(state, action, game.get_state(), 100)
                break
            action = random.choice(game.get_valid_actions())
            winner = game.play(*action)
            game.prev_move = action
            
            # agent losses
            if winner or game.is_ended():
                self.qlearner.update(state, action, game.get_state(), -100)
                break
            
            # No win / loss
            self.qlearner.update(state, action, game.get_state(), 0)
            
    def learn(self, n = 1000):
        
        for _ in tqdm(range(n), desc = 'Training AI'):
            self.learn_one_game()
            self.eps -= 0.0001