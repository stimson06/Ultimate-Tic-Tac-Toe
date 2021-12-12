from collections import defaultdict

class Q_learning:
    """ Creates & updates the Q-table with the Bellman's equation. """
    
    def __init__(self, alpha = 0.01, discount = 0.9):
        """ Initializing the required parameters.

        Args:
            alpha : Learning rate. Defaults to 0.01.
            discount : Discount factor. Defaults to 0.9. """
        
        self.alpha = alpha
        self.discount = discount
        self.values = defaultdict(lambda: defaultdict(lambda: 0.0))
        
    def update(self, state, action, next_state, reward):
        """ Updates the Q-table with appropriate parameters.

        Args:
            state : Current state of the board.
            action : action available (or) best action by get_best_action function.
            next_state : Future state after the move.
            reward : Reward for the current move made.
        """
        
        # Get the value of the current state
        value = self.values[state][action]
        
        # Get the max q-value in the current state
        v =list(self.values[next_state].values())
        next_q = max(v) if v else 0
        
        # Bellmans equation
        value = value + self.alpha * (reward + self.discount * next_q - value)
        self.values[state][action] = value
        
    def get_best_action(self, state):
        """ Returns best actions (or) None based on the state of 
            the board.

        Args:
            state : Current state of the board.

        Returns:
            max: actions with highest Q-value.
        """
        
        # Keys of the state
        keys = list(self.values[state].keys())
        
        if not keys:
            return None
        
        # key with highest Q-value
        return max(keys, key = lambda x: self.values[state][x])