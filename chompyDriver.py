import numpy as np
import multiprocessing as mp
import time
import os

import utility as util
import extendBoardStates as ebs

"""
Data structure:
index.txt - contains current state data
	JSON of ([solved - tuple (mxn)], [working nodes]) //working nodes even necesary?
solved/mXn - [(board,[parents,],num),] for m x n board
firstMoves.txt - list of first moves for mxn boards. JSON or CSV?
"""
DATA_FOLDER = "./data/epoc1/"
SOLVED_FOLDER = DATA_FOLDER + "solved/"
THREAD_MAX = 16

#have to seed 2x2 

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

	solved,nodes = genIndexData()

	pHandler = ProccesHandler(THREAD_MAX)

	for node in nodes:
		pHandler.run( node )
	time.sleep(100)
	pHandler.terminate()

#gets the list of solved sizes and gens the list of current nodes to be worked on
def genIndexData():
	files = os.listdir(SOLVED_FOLDER)
	if ".DS_Store" in files:
		files.remove(".DS_Store")

	solved = []
	#each file shoud be in form of mXn.json 0 - not fully checking yet
	for file in files:
		#rudementry check for format
		if file[1] == "X" and file[3] == ".":
			solved.append( (int(file[0]), int(file[2])) )

	nodes = []
	for size in solved:
		#the next one in form mXn+1
		if not ((size[0], size[1]+1) in solved):
			nodes.append( (size[0], size[1]+1) )
		#for adding square nodes (stats another m value chain)
		if size[0] + 1 == size[1] and not ((size[0]+1, size[1]) in solved):
			nodes.append( (size[0]+1, size[1]) )

	return (solved, nodes)
	

def solveThread(q):
	while True:
			size = q.get()
			if size is None:
				time.sleep(1)
				continue

			# process your item here
			print("Processing "  +str(size[0])+"X"+str(size[1]) + " in " + str(os.getpid()))
			
			states = []
			#square node, start of new column
			if size[0] == size[1]:
				data = util.load(DATA_FOLDER + "solved/" + str(size[0]-1)+"X"+str(size[1]) + ".json")
				#expand vert
				#get states of root size - this case m-1Xn since square
				#data = [(board,[parents,],num),]
				oldData = util.load(SOLVED_FOLDER+str(size[0]-1)+"X"+str(size[1])+".json")
				oldStates = oldData[:,0] 
				states = appendRowToBoardStates(oldStates)
			#not square
			else:
				data = util.load(DATA_FOLDER + "solved/" + str(size[0])+"X"+str(size[1]-1) + ".json")
				#extend horiz
				#get states of root size - this case mXn-1
				#data = [(board,[parents,],num),]
				oldData = util.load(SOLVED_FOLDER+str(size[0]-1)+"X"+str(size[1])+".json")
				oldStates = oldData[:,0] 
				states = appendColToBoardStates(oldStates)

			#extend heritage
			#calc state nums
			#find best first move(s)
			#save data

			#MAKE SURE TO REMOVE THIS LOL
			time.sleep( float(size[0]*size[1]) ** 0.5 )

			util.store(["FILLER"], DATA_FOLDER + "solved/" + str(size[0]) + "X" + str(size[1]) + ".json")
			


			#put mXn+1
			q.put( (size[0], size[1]+1) )
			print("Added " + str(size[0]) + "X" + str(size[1]+1) + " to queue")
			
			#if m+1Xn is square (root of new column)
			if size[0]+1 == size[1]:
				q.put( (size[0]+1, size[1]) )
				print("Added " + str(size[0]+1) + "X" + str(size[1]) + " to queue")
			
			q.task_done()

class ProccesHandler:
	queue = None

	def __init__(self, nb_workers=6):
		self.queue = mp.JoinableQueue()
		self.processes = [mp.Process(target=solveThread, args=(self.queue,), daemon=False) for i in range(nb_workers)]
		
		for p in self.processes:
			p.start()

	def run(self, item):
		self.queue.put(item)


	

	def terminate(self):
		""" wait until queue is empty and terminate processes """ #-except don't cause queue will never empty
		#self.queue.join()

		for p in self.processes:
			p.terminate()
	

#Creates the 2x2 solved case to act as seed for the expansion cycles
def seed():
	#Replace filler with actual data
	util.store(["FILLER"], DATA_FOLDER + "solved/2X2.json")
	util.store([[[2, 2]], [[2, 3]]], DATA_FOLDER + "index.json")


if __name__ == "__main__":
	mp.set_start_method('spawn')
	#seed()
	main()


	
