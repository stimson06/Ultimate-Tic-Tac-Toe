from agent import Agent
from ultimate_ttt import Board
import time

def play(agent):
    
    game  = Board()
    
    while True:
        
        action = agent.qlearner.get_best_action(game.get_state())
        winner = game.play(*action)
        
        if winner:
            print("Player '%s' won" %game.repr[game.player])
            return
        if game.is_ended():
            print("Match Tie, Better Luck next time!")
            return
        
        user = ((input("\nboard, row, col >")))
        action =tuple(map(int, user.split(',')))
        winner = game.play(*action)
        
        if winner:
            print("Player '%s' won" %game.repr[game.player])
            return
        if game.is_ended():
            print("Match Tie, Better Luck next time!")
            return
            
if __name__ == "__main__":
    
    q_agent = Agent()
    start = time.time()
    q_agent.learn()
    end = time.time()

    print('Runtime :{:.2f}s'.format(end - start))
    print("\n Let's play Ultimate TIC-TAC-TOE \n")
    print("Type 'exit' to quit the game")
    
    play(q_agent)