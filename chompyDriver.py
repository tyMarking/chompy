import utility as util
import numpy as np

"""
Data structure:
index.txt - contains current state data
	JSON of [[solved - tuple (mxn)], [working nodes]] //working nodes even necesary?
solved/mXn - [(board,[parents,],num),] for m x n board
firstMoves.txt - list of first moves for mxn boards. JSON or CSV?
"""
DATA_FOLDER = "./data/epoc1/"
THREAD_MAX = 6

def main():
	"""
	1. read index
		a. get list of current working nodes 
			(unsolved nodes for which we have mXn-1 solved or the next square)
	2. for each working node create new thread (up to thread max)
	3. In thread:
		a. load data from mxn-1 or m-1xn if square
		b. extend board states
		c. extend heritage
		d. calculate state nums.
		e. find best first move
		f. open up next node and repeat
	"""









if __name__ == "__main__":
	main()