import utility as util
import numpy as np
import multiprocessing as mp
import time
import os
from ctypes import Structure, c_int

"""
Data structure:
index.txt - contains current state data
	JSON of ([solved - tuple (mxn)], [working nodes]) //working nodes even necesary?
solved/mXn - [(board,[parents,],num),] for m x n board
firstMoves.txt - list of first moves for mxn boards. JSON or CSV?
"""
DATA_FOLDER = "./data/epoc1/"
SOLVED_FOLDER = DATA_FOLDER + "solved/"
THREAD_MAX = 6

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
	fileName = DATA_FOLDER + "index.json"
	index = util.load(fileName)
	print(index)
	solvedList = index[0]
	nodesList = index[1]
	solved = []
	nodes = []
	for s in solvedList:
		solved.append( (s[0], s[1]) )
	for n in nodesList:
		nodes.append( (n[0], n[1]) )


	pHandler = ProccesHandler(6, solved, nodes)


	for node in nodes:
		pHandler.run( (node[0], node[1]) )
	time.sleep(20)
	pHandler.terminate()


def genIndexData():
	files = os.listdir(SOLVED_FOLDER)
	if ".DS_Store" in files:
		files.remove(".DS_Store")

	solved = []
	#each file shoud be in form of mXn.json 0 - not checking yet
	for file in files:
		solved.append( (file[0], file[2]) )

	

class ProccesHandler:
	queue = None
	addToSolved = None
	addToNodes = None

	def __init__(self, nb_workers, solved, nodes):
		self.queue = mp.JoinableQueue()
		self.addToSolved = mp.JoinableQueue()
		self.addToNodes = mp.JoinableQueue()
		self.processes = [mp.Process(target=self.upload, daemon=False) for i in range(nb_workers)]
		self.indexHandlerProcesses = mp.Process(target=self.indexHandler, args=(solved, nodes),daemon=False)
		for p in self.processes:
			p.start()
		self.indexHandlerProcesses.start()

	def run(self, item):
		self.queue.put(item)

	def upload(self):
		while True:
			size = self.queue.get()
			if size is None:
				time.sleep(1)
				continue

			# process your item here
			print("Processing "  +str(size[0])+"X"+str(size[1]) + " in " + str(os.getpid()))
			

			#square node, start of new column
			if size[0] == size[1]:
				data = util.load(DATA_FOLDER + "solved/" + str(size[0]-1)+"X"+str(size[1]) + ".json")
				#expand vert
			#not square
			else:
				data = util.load(DATA_FOLDER + "solved/" + str(size[0])+"X"+str(size[1]-1) + ".json")
				#extend horiz

			#extend heritage
			#calc state nums
			#find best first move(s)
			#save data
			time.sleep( float(size[0]*size[1]) ** 0.5 )

			util.store(["FILLER"], DATA_FOLDER + "solved/" + str(size[0]) + "X" + str(size[1]) + ".json")
			


			#put mXn+1
			self.queue.put( (size[0], size[1]+1) )
			self.addToNodes.put( (size[0], size[1]+1) )
			print("Added " + str(size[0]) + "X" + str(size[1]+1) + " to queue")
			
			#if m+1Xn is square (root of new column)
			if size[0]+1 == size[1]:
				self.queue.put( (size[0]+1, size[1]) )
				self.addToNodes.put( (size[0]+1, size[1]) )
				print("Added " + str(size[0]+1) + "X" + str(size[1]) + " to queue")
				
			#update index

			
			self.addToSolved.put( (size[0], size[1]) )
			self.queue.task_done()

	"""
	def indexNodeHandler(self, solved, nodes):
		while True:
			nodeSize = self.addToNodes.get()
			print("\nNode Handler: ")
			print(nodeSize)
			print()
			if not (nodeSize is None):
				nodes.append(solvedSize)

			#util.store([solved, nodes], DATA_FOLDER + "index.json")
			self.queue.task_done()

	def indexSolvedHandler(self, solved, nodes):
		while True:
			solvedSize = self.addToSolved.get()
			print("\nSolved Handler: ")
			print(solvedSize)
			print()
			if not (solvedSize is None):
				print("Nodes & Solved before and after")
				print(nodes)
				print(solvedSize)
				solved.append(solvedSize)
				nodes.remove(solvedSize)
				print(nodes)
				print(solvedSize)

			util.store([solved, nodes], DATA_FOLDER + "index.json")
			self.queue.task_done()
	"""	
	def indexHandler(self, solved, nodes):
		while True:
			solvedSize = self.addToSolved.get()
			nodeSize = self.addToNodes.get()
			print("\nIndex Handler: solvedSize, nodeSize, solved, nodes ")
			print(solvedSize)
			print(nodeSize)
			print(solvedSize)
			print(nodes)
			print()

			while not (nodeSize is None):
				print("Adding node: " + str(nodeSize))
				nodes.append(nodeSize)
				self.addToNodes.task_done()
				nodeSize = self.addToNodes.get()

			while not (solvedSize is None):
				print("Solved & Nodes before and after")
				print(solvedSize)
				print(nodes)
				solved.append(solvedSize)
				nodes.remove(solvedSize)
				print(solvedSize)
				print(nodes)

				self.addToSolved.task_done()
				solvedSize.addToSolved.get()
			
			print("Storing...")
			util.store([solved, nodes], DATA_FOLDER + "index.json")
			
			

	

	def terminate(self):
		""" wait until queue is empty and terminate processes """
		#self.queue.join()
		self.addToNodes.join()
		self.addToSolved.join()

		self.indexHandlerProcesses.terminate()
		for p in self.processes:
			p.terminate()
	


def seed():
	#Replace filler with actual data
	util.store(["FILLER"], DATA_FOLDER + "solved/2X2.json")
	util.store([[[2, 2]], [[2, 3]]], DATA_FOLDER + "index.json")


if __name__ == "__main__":
	mp.set_start_method('spawn')
	#seed()
	genIndexData()
	#main()


	
