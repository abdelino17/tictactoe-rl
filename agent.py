import numpy as np
import random

GAME_LENGTH=3

class Agent:
    
    def __init__(self, eps=0.1, alpha=0.5):
      self.eps = eps # probability of choosing random action instead of greedy
      self.alpha = alpha # learning rate
      self.verbose = False
      self.state_history = []
    
    def setV(self, V):
      self.V = V
  
    def set_symbol(self, sym):
      self.sym = sym
  
    def set_verbose(self, v):
      # if true, will print values for each position on the board
      self.verbose = v
  
    def reset_history(self):
      self.state_history = []
  
    def take_action(self, env):
      # choose an action based on epsilon-greedy strategy
      r = np.random.rand()
      best_state = None
      if r < self.eps:
        # take a random action
        if self.verbose:
            print("Taking a random action")
  
        possible_moves = []
        for i in range(GAME_LENGTH):
          for j in range(GAME_LENGTH):
            if env.is_empty(i, j):
              possible_moves.append((i, j))
        idx = np.random.choice(len(possible_moves))
        next_move = possible_moves[idx]
      else:
        # choose the best action based on current values of states
        # loop through all possible moves, get their values
        # keep track of the best value
        pos2value = {} # for debugging
        next_move = None
        best_value = -1
        for i in range(GAME_LENGTH):
          for j in range(GAME_LENGTH):
            if env.is_empty(i, j):
              # what is the state if we made this move?
              env.board[i,j] = self.sym
              state = env.get_state()
              env.board[i,j] = 0 # don't forget to change it back!
              pos2value[(i,j)] = self.V[state]
              if self.V[state] > best_value:
                best_value = self.V[state]
                best_state = state
                next_move = (i, j)
  
        # if verbose, draw the board w/ the values
        if self.verbose:
          print("Taking a greedy action")
          for i in range(GAME_LENGTH):
            print("------------------")
            for j in range(GAME_LENGTH):
              if env.is_empty(i, j):
                # print the value
                print(" %.2f|" % pos2value[(i,j)], end="")
              else:
                print("  ", end="")
                if env.board[i,j] == env.x:
                  print("x  |", end="")
                elif env.board[i,j] == env.o:
                  print("o  |", end="")
                else:
                  print("   |", end="")
            print("")
          print("------------------")
  
      # make the move
      env.board[next_move[0], next_move[1]] = self.sym
  
    def update_state_history(self, s):
      self.state_history.append(s)
  
    def update(self, env):
      # we want to BACKTRACK over the states, so that:
      # V(prev_state) = V(prev_state) + alpha*(V(next_state) - V(prev_state))
      # where V(next_state) = reward if it's the most current state
      reward = env.reward(self.sym)
      target = reward
      for prev in reversed(self.state_history):
        value = self.V[prev] + self.alpha*(target - self.V[prev])
        self.V[prev] = value
        target = value
      self.reset_history()