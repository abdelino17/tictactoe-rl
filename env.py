import numpy as np

GAME_LENGTH = 3

class Environment:

    def __init__(self):
      self.board = np.zeros((GAME_LENGTH, GAME_LENGTH))
      self.x = -1 # represents an x on the board, player 1
      self.o = 1 # represents an o on the board, player 2
      self.winner = None
      self.ended = False
      self.num_states = 3 ** (GAME_LENGTH*GAME_LENGTH)
    
    def is_empty(self, i, j):
      return self.board[i,j] == 0
    
    def reward(self, sym):
      # no reward until game is over
      if not self.game_over():
        return 0
    
      # if we get here, game is over
      # sym will be self.x or self.o
      return 1 if self.winner == sym else 0
    
    def get_state(self):
      # returns the current state, represented as an int
      # from 0...|S|-1, where S = set of all possible states
      k = 0
      h = 0
      for i in range(GAME_LENGTH):
        for j in range(GAME_LENGTH):
          if self.board[i,j] == 0:
            v = 0
          elif self.board[i,j] == self.x:
            v = 1
          elif self.board[i,j] == self.o:
            v = 2
          h += (3**k) * v
          k += 1
      return h
    
    def game_over(self, force_recalculate=False):
      # returns true if game over (a player has won or it's a draw)
      # otherwise returns false
      # also sets 'winner' instance variable and 'ended' instance variable
      if not force_recalculate and self.ended:
        return self.ended
      
      # check rows
      for i in range(GAME_LENGTH):
        for player in (self.x, self.o):
          if self.board[i].sum() == player * GAME_LENGTH:
            self.winner = player
            self.ended = True
            return True
    
      # check columns
      for j in range(GAME_LENGTH):
        for player in (self.x, self.o):
          if self.board[:,j].sum() == player * GAME_LENGTH:
            self.winner = player
            self.ended = True
            return True
    
      # check diagonals
      for player in (self.x, self.o):
        # top-left -> bottom-right diagonal
        if self.board.trace() == player * GAME_LENGTH:
          self.winner = player
          self.ended = True
          return True
        # top-right -> bottom-left diagonal
        if np.fliplr(self.board).trace() == player * GAME_LENGTH:
          self.winner = player
          self.ended = True
          return True
    
      # check if draw
      if np.all((self.board == 0) == False):
        # winner stays None
        self.winner = None
        self.ended = True
        return True
    
      # game is not over
      self.winner = None
      return False
    
    def is_draw(self):
      return self.ended and self.winner is None
    
    def get_winner(self):
        return self.winner
    
    # Example board
    # -------------
    # | x |   |   |
    # -------------
    # |   |   |   |
    # -------------
    # |   |   | o |
    # -------------
    def draw_board(self):
      for i in range(GAME_LENGTH):
        print("-------------")
        for j in range(GAME_LENGTH):
          print("  ", end="")
          if self.board[i,j] == self.x:
            print("x ", end="")
          elif self.board[i,j] == self.o:
            print("o ", end="")
          else:
            print("  ", end="")
        print("")
      print("-------------")