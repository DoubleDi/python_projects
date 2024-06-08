"""
Task:
1. Come up with a data structure to represent the board and the falling piece
2. Implement three methods:
    - move left (don't go outside of the board, don't overlap another piece)
    - move right
    - rotate (somewhat around the centre)
"""

""" Example of a board and a falling piece
   0 1 2 3 4 5 6 7
 0 
 1     
 2
 3     ■ ■ ■
 4         ■
 5    
 6  
 7   
 8
 9   
10   
11
12   ■ ■   ■ ■ ■  
13   ■       ■   
14 ■ ■ ■   ■ ■ ■ 
15 ■ ■ ■ ■ ■ ■ ■ ■
"""

""" Examples of tetris pieces
          ■ ■ 
          ■ ■
 ■ ■ ■
     ■

       ■ ■
         ■ ■
     
  ■ ■ ■
    ■

      ■ ■ ■ ■

    ■ ■
  ■ ■
"""


""" Example of rotation
     ■
     ■
   X X X X
     ■
"""

class Piece:
  
	
  
  def __init__(self, type_):
    self.type = type_
    self.pos = 1 # 1,2,3,4
  
  def rotate(self, board, x, y):
    pass
  
class Line(Piece):
  # pos = 1 -1 -1 -1 -1
  #
  # pos = 2 -1
  #         -1
  #         -1 
  #         -1 
  #
  # pos = 3 -1 -1 -1 -1
  #
  # pos = 4 -1
  #         -1
  #         -1 
  #         -1 
  
  box_size = 4
  
  def rotate(self, board, x, y):
    
    if self.pos == 1:
      # x, y => x - 1, y + 1
      # x, y + 1 => x, y + 1
      # x, y + 2 => x + 1, y + 1
      # x, y + 3 => x + 2, y + 1
    	self.pos = 2 
  
  def rotate2(self, board, x, y):
    for i in range(x, x+self.box_size):
      for j in range(y, y+self.box_size):
        if board[i][j] != -1:
					continue
        # 0, 0 => n-1, 0
        # 1, 0 => n-1, 1
        # 2, 0 => n-1, 2
        # 1, 1 => n-1, 1
      	# x, y => n-y, x
        if n-j <0 or i >= len(board[0]) or board[n-j][i] == 1:
          return None
        
    for i in range(x, x+self.box_size):
      for j in range(y, y+self.box_size):
        if board[i][j] != -1:
					continue
        board[i][j] = board[n-j][i]
    
        
        
    (x, y) +1 +1 +1
     +1
      +1
      +1
    
      
      
      
      
      
  
  
class Tetris:
  # 0 - empty
  # 1 - filled
  # -1 - current piece
  
	def __init__(self):
		self.board = []
    for i in range(16):
      	self.board.append([0] * 8)
    self.piece = Piece()
  
  
#   0 0 0 -1 0 
#   0 0 0 -1 0 
#   1 1 1 -1 0 
#   1 1 1 -1 0
  
#   0 0 0 0 0 
#   -1 -1 -1 -1 0 
#   0 0 0 0 0 
#   1 1 1 0 0
  
  def move(self, direction='left'):
    # n ** 2
    can_move = True
    for i, row in enumerate(self.board):
      for j, cell in enumerate(row):
        if cell == -1:
          if direction == 'left':
          	if j == 0 or row[j-1] == 1:
            	return None
          if direction = 'right':
            if j == n-1 or row[j+1] == 1:
            	return None
    # move ...
      
  def rotate(self):
    x, y = # locate left top angle piece
    self.piece.rotate(self.board, x, y)
    
  
  def next_piece(self):
    pass
    
  def step(self):
    pass
    # 1. move down
    # 2. check if piece at final state
    # 3. remove full rows
    # 4. move top rows down
  
  
    


















