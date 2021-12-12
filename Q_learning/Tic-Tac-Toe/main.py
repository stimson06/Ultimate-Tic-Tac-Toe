from agent import Agent
from tic_tac_toe import Board
import time

def play(agent):
    """ Loop to play the game untill win / loss / tie state 
        is achieved.

    Args:
        agent : trained / updated Q-table . """
    
    # Intialize the board class
    game = Board()
    
    # Loop to play the game
    play_game = True
    while play_game:
        
        # Play by the AI
        action = agent.qlearner.get_best_action(game.get_state())
        winner = game.play(*action)
        
        # Check for win / loss / tie state.
        if winner:
            play_game = False
            print("Player '%s' won" %game.repr[game.player])
            return
        if game.is_ended():
            play_game = False
            print("Match Tie, Better Luck next time!")
            return
    
        # Play by the user
        user = input("row, col > ")
        
        # user input
        if user == 'exit':
            break
        elif user == '':
            game.play(agent)
        else:
            row, col = map(int, user.split(','))
        
        # make move on the board
        winner = game.play(row-1, col-1)
        
        # Check for win / loss / tie state.
        if winner:
            play_game = False
            print("Player '%s' won" %game.repr[game.player])
            return
        if game.is_ended():
            play_game = False
            print("Match Tie, Better Luck next time!")
            return
  
if __name__ == "__main__":
    
    # Train the Q-table 
    q_agent = Agent()
    start = time.time()
    q_agent.learn()
    end = time.time()
   
    # Print the runtime
    print('Runtime :{:.2f}s'.format(end - start))
    print("\n Let's play TIC-TAC-TOE \n")
    print("Type 'exit' to quit the game")
    
    # Play the game.
    play(q_agent)