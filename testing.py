from mcts import MCTS
from amaf import A_MCTS
from isolation import Board
import random

FIXED_TIME = 0.1
VARIABLE_TIME = [0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.5]
SIDES = ["white", "black"]
NUM_GAMES = 50

avg_win_rate = []
for i in range(len(VARIABLE_TIME)):
    idx = random.choice([0,1])
    var_bot = SIDES[idx]
    fixed_bot = SIDES[1-idx]
    win_count = 0
    for n in range(NUM_GAMES):
        gs = Board(fixed_bot, var_bot, 8, 6)
        while(not gs.is_winner(fixed_bot) and not gs.is_winner(var_bot)):
            move = MCTS(gs, FIXED_TIME, fixed_bot)
            gs.apply_move(move)
            if(gs.is_winner(fixed_bot) or gs.is_winner(var_bot)):
                break
            move = A_MCTS(gs, VARIABLE_TIME[i], var_bot)
            gs.apply_move(move)
        
        if(gs.is_winner(var_bot)):
            win_count += 1
        if(n % 10 == 0):
            print(f"game no: {n} and win count {win_count}")
    
    print(f"For {VARIABLE_TIME[i]}s the avg win rate is: {win_count*2}%")
    avg_win_rate.append(win_count/100)
    

from matplotlib import pyplot as plt

plt.title("Time in sec vs Win Rate")
plt.xlabel("Time (s)")
plt.ylabel("Win Rate (out of 100)")
plt.plot(VARIABLE_TIME, avg_win_rate)
plt.legend(['Standard','AMAF'])
plt.show()
    