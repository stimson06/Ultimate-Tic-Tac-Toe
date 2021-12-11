from collections import defaultdict

class Q_learning:
    
    def __init__(self, alpha = 0.01, discount = 0.9):
        self.alpha = alpha
        self.discount = discount
        self.values = defaultdict(lambda: defaultdict(lambda: 0.0))
        
    def update(self, state, action, next_state, reward):
        
        # Get the value of the current state
        
        #print(action)
        value = self.values[state][action]
        
        # Get the max q-value in the current state
        v =list(self.values[next_state].values())
        next_q = max(v) if v else 0
        
        # Bellmans equation
        value = value + self.alpha * (reward + self.discount * next_q - value)
        self.values[state][action] = value
        
    def get_best_action(self, state):
        
        keys = list(self.values[state].keys())
        
        if not keys:
            return None

        return max(keys, key = lambda x: self.values[state][x])