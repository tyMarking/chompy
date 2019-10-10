"""
A mXn board is an array of ints with length m.
The fist value must be exactly n.
Each subsequent value must be less than or equal to the previous.
Each value represents the number of squares in the row.
The poison is at coordinate 0, 0 (in the top left).
The poison is counted in the number of squares in the first row.
"""

#bite the matrix based board at the coordinates x, y
#x, y are 0 indexed. X is the column, Y is the row
def bite(board, x, y):
	#loop through the rows of board, starting at y
	#if the value of board at the current row is greater than x,
		#set the value of the new board at the row to x
	#else
		#none of the others will have a greater length value, so we can end
		#return
