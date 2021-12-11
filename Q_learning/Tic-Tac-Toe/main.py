from agent import Agent
from tic_tac_toe import Board
import time

def play(agent):
    
    #
    game = Board()
    play_game = True
    while play_game:
        
        action = agent.qlearner.get_best_action(game.get_state())
        winner = game.play(*action)
        
        if winner:
            play_game = False
            print("Player '%s' won" %game.repr[game.player])
            return
        if game.is_ended():
            play_game = False
            print("Match Tie, Better Luck next time!")
            return
    
        user = input("row, col > ")
        
        if user == 'exit':
            break
        elif user == '':
            game.play(agent)
        else:
            row, col = map(int, user.split(','))
        
        winner = game.play(row-1, col-1)
        
        if winner:
            play_game = False
            print("Player '%s' won" %game.repr[game.player])
            return
        if game.is_ended():
            play_game = False
            print("Match Tie, Better Luck next time!")
            return
  
if __name__ == "__main__":
    
    q_agent = Agent()
    start = time.time()
    q_agent.learn()
    end = time.time()
   
    print('Runtime :{:.2f}s'.format(end - start))
    print("\n Let's play TIC-TAC-TOE \n")
    print("Type 'exit' to quit the game")
    
    play(q_agent)