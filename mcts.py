import random
from node import Node
from math import sqrt, log, inf
import time
from copy import deepcopy


def MCTS(game_env, time_alloc, player):
    
    st_time = time.time()
    current_player = 0 if player == "white" else 1
    root_node = Node('Root',{'action':None,'n':0,'avail':0,'mark':False, 'player':current_player, 'reward':[0,0]})
    focus_node = root_node
    while(time.time() - st_time < time_alloc):
        temp_env = deepcopy(game_env)
        focus_node = root_node
        focus_node,temp_env = SELECT(focus_node,temp_env)
        if CHECKFORNEWACTIONS(focus_node, temp_env):
            focus_node, temp_env = EXPAND(focus_node, temp_env)
        reward = SIMULATE(temp_env)
        BACKPROPAGATE(reward, focus_node)

    action = avg_max(root_node)
    return action

def SELECT(focus_node, temp_env):
    while not (temp_env.is_winner("white") or temp_env.is_winner("black")) and not CHECKFORNEWACTIONS(focus_node, temp_env):
        focus_node = UCB1_max(focus_node, temp_env)
        action = focus_node.data['action']
        temp_env.apply_move(action)
    
    return focus_node, temp_env

def EXPAND(focus_node, temp_env):
    new_actions = GETNEWACTIONS(focus_node, temp_env)
    action = random.choice(new_actions)
    current_player = 0 if temp_env.active_player == "white" else 1
    child_node = Node(action, {'action':action,'n':0,'avail':0, 'reward':[0,0],'mark':True, 'player':current_player})
    focus_node.set_child(child_node)
    temp_env.apply_move(action)
    focus_node = child_node
    
    return focus_node, temp_env


def SIMULATE(temp_env):
    while(not (temp_env.is_winner("white") or temp_env.is_winner("black"))):
        actions = temp_env.get_legal_moves()
        temp_env.apply_move(random.choice(actions))
    
    return [int(temp_env.is_winner("white")), int(temp_env.is_winner("black"))]

def BACKPROPAGATE(reward, focus_node):
    while(focus_node != None):
        focus_node.data['n'] += 1
        for i in range(2):
            focus_node.data['reward'][i] += reward[i]
        
        focus_node = focus_node.parent
        
        
def CHECKFORNEWACTIONS(focus_node, temp_env):
    avail = temp_env.get_legal_moves()
    old_actions = []
    for child in focus_node.children:
        old_actions.append(child.data['action'])
    for action in avail:
        if(action not in old_actions):
            return True
    
    return False


def GETNEWACTIONS(focus_node, temp_env):
    avail = temp_env.get_legal_moves()
    old_actions = []
    new_actions = []
    for child in focus_node.children:
        old_actions.append(child.data['action'])
    for action in avail:
        if(action not in old_actions):
            new_actions.append(action)
    
    return new_actions


def avg_max(focus_node):
    max_val = -inf
    max_node = None
    for child in focus_node.children:
        idx = child.data['player']
        avg_reward = child.data['reward'][idx] / child.data['n']
        if(avg_reward > max_val):
            max_node = child
            max_val = avg_reward
    
    return max_node.data['action']

def UCB1_max(focus_node, temp_env):
    max_val = -inf
    max_node = None
    for i in range(len(focus_node.children)):
        val = UCB1(focus_node.children[i]) 
        if(val > max_val):
            max_val = val
            max_node = focus_node.children[i]

    return max_node


def UCB1(focus_node):
    n = focus_node.data['n']
    N = focus_node.parent.data['n']
    k = sqrt(2)
    reward_vec = focus_node.data['reward']
    idx = focus_node.data['player']
    reward_val = reward_vec[idx]
    if(n == 0):
        return inf
    else:
        return (reward_val/n) + k * sqrt(log(N)/n)

