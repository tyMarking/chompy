import numpy as np
import multiprocessing as mp
import time
import os
import queue
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
STATES_FOLDER = DATA_FOLDER + "states/"
SOLVED_FOLDER = DATA_FOLDER + "solved/"
SOLVE_THREADS = 8
GRAPH_THREADS = 8

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

	pHandler = ProccesHandler(SOLVE_THREADS, GRAPH_THREADS)

	for node in nodes:
		pHandler.run( node )
	time.sleep(100)
	pHandler.terminate()

class ProccesHandler:
	permQueue = None
	graphQueue = None

	def __init__(self, perm_workers=6, graph_workers=6):
		self.permQueue = mp.JoinableQueue()
		self.processes = [mp.Process(target=statesThread, args=(self.permQueue,), daemon=False) for i in range(perm_workers)]
		self.gProcesses = [mp.Process(target=graphThread, args=(self.graphQueue,), daemon=False) for i in range(graph_workers)]
		self.cleanupProcesses = mp.Process(target=cleanup)
		self.cleanupProcesses.start()
		for p in self.processes:
			p.start()
		for p in self.gProcesses:
			p.start()

	def run(self, item):
		self.permQueue.put(item)


	

	def terminate(self):
		""" wait until queue is empty and terminate processes """ #-except don't cause queue will never empty
		#self.queue.join()

		for p in self.processes:
			p.terminate()
		for p in self.gProcesses:
			p.terminate
		self.cleanupProcesses.terminate()


#gets the list of solved sizes and gens the list of current nodes to be worked on
def genIndexData():
	files = os.listdir(STATES_FOLDER)
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
	


def statesThread(q):
	while True:
		size = q.get()
		if size is None:
			time.sleep(1)
			continue

		# process your item here
		print("Processing "  +str(size[0])+"X"+str(size[1]) + " in " + str(os.getpid()))
		
		#data = [[states],hertitigeDict]
		data = []
		#square node, start of new column
		if size[0] == size[1]:
			#expand vert
			#get states of root size - this case m-1Xn since square
			
			oldData = util.load(STATES_FOLDER+str(size[0]-1)+"X"+str(size[1])+".json")
			states = ebs.appendRowToBoardStates(oldData[0], oldData[1])
			
			pass
		#not square
		else:
			#extend horiz
			#get states of root size - this case mXn-1
			oldData = util.load(STATES_FOLDER+str(size[0])+"X"+str(size[1]-1)+".json")
			print("\n\n\nOld Data: " + str(oldData) + "\n\n\n")
			states = ebs.appendColToBoardStates(oldData[0], oldData[1])
			
			pass

		#save data

		#MAKE SURE TO REMOVE THIS LOL
		#time.sleep( (float(size[0]*size[1]) ** 0.5) / 2 )

		util.store(data.tolist(), STATES_FOLDER + str(size[0]) + "X" + str(size[1]) + ".json")
		


		#put mXn+1
		q.put( (size[0], size[1]+1) )
		print("Added " + str(size[0]) + "X" + str(size[1]+1) + " to queue")
		
		#if m+1Xn is square (root of new column)
		if size[0]+1 == size[1]:
			q.put( (size[0]+1, size[1]) )
			print("Added " + str(size[0]+1) + "X" + str(size[1]) + " to queue")
		
		q.task_done()

def graphThread(q):
	while True:
		while q.empty():
			time.sleep(1)
		file = q.get()
		fileName = STATES_FOLDER + file
		#[[states],{stateXchild}]
		fData = util.load(fileName, False)
		"""
		states = fData[0]
		bXchild = fData[1]

		#Gen parent dict
		bXparent = {}
		for b in states:
			bXparent[dKey(b)] = []
		for b in states:
			for child in bXchild[dKey(b)]:
				if not b in bXparent[dKey(parent)]:
					bXparent[dKey(child)].append(b)

		bXnum = gen_path_numbers(states, bXparents)

		data = [states, bXchild, bXparents, bXnum]
		"""
		data = "filler + graph"

		util.store(data, SOLVED_FOLDER + file)
		os.remove(fileName)
		q.task_done()


def gen_path_numbers(perms, bXparents):
	#dictionary of board permutations with their playable options
	#build perms as it goes?
	#start with fully bitten board

	endBoard = util.genEndBoard(len(perms[0]), len(perms[0][0]))

	bXnum = {util.dKey(endBoard) : 0}
	#sorted by least number of choices
	evalQ = queue.PriorityQueue()
	for b in perms:
		evalQ.put((len(util.get_choices(b)), b))

	evalQ.put((-1, endBoard))

	checked = []

	while evalQ.qsize() > 0:
		#print("Q size: " + str(evalQ.qsize()))
		cB = evalQ.get()[1]
		#print("cB:")
		#display(cB)
		num = bXnum[util.dKey(cB)]
		#print("cB's num: " + str(num))

		for parent in bXparents[util.dKey(cB)]:
			#print("parent:")
			#display(parent)
			#print(bXnum.keys())
			#print("parent key: " + str(dKey(parent)))
			pKey = util.dKey(parent)

			if not (pKey in bXnum.keys()):
				#print("condition 1")
				bXnum[pKey] = num + 1
			elif (num + 1) % 2 == 1 and (bXnum[pKey] % 2 == 0 or (num+1) < bXnum[pKey]):
				#print("condition 2")
				bXnum[pKey] = num + 1
			elif (num + 1) < bXnum[pKey] and bXnum[pKey] % 2 == 0:
				#print("condition 3")
				bXnum[pKey] = num + 1
			
	return bXnum



def getFirstMove(perms, bXparent):
	
	bXchild = {}
	for b in perms:
		bXchild[dKey(b)] = []
	for b in perms:
		for parent in bXparent[dKey(b)]:
			if not b in bXchild[dKey(parent)]:
				bXchild[dKey(parent)].append(b)

	moves = []
	for c in bXchild[dKey(board)]:
		if bXnum[dKey(c)] % 2 == 0:
			moves.append(c)
	return moves


def stateReader(q):
	#read files names from folder
	#find all redundent files (not going to be used for inheriting by any nodes)
	#read storage file
	#add new data to old data from storage file
	#write to storage file
	#delet redundent files
	while True:
		files = os.listdir(STATES_FOLDER)
		if ".DS_Store" in files:
			files.remove(".DS_Store")

		#Keep the seed to replant if neccessary
		files.remove("2X2.json")
		#indexes should corresponnd
		solvedFiles = []
		solvedSizeOnly = []
		#each file shoud be in form of mXn.json 0 - not fully checking yet
		for file in files:
			#rudementry check for format
			#if file[1] == "X" and file[3] == ".":
			#print(file)
			charI = 0
			while file[charI] != "X":
				charI += 1
			m = int(file[:charI])
			charI2 = charI
			while file[charI2] != ".":
				charI2 += 1
			n = int(file[charI+1:charI2])

			solvedFiles.append( file )
			solvedSizeOnly.append( (m, n) )
		#print("Solved: " + str(solvedFiles))
		redundent = []
		for i in range(len(solvedFiles)):
			size = solvedSizeOnly[i]
			print(size)
			#if the next one in form mXn+1 is solved then redundent
			if ((size[0], size[1]+1) in solvedSizeOnly):
				#if needed for the m+1 square node
				if size[0] + 1 == size[1] and not ((size[0]+1, size[1]) in solvedSizeOnly):
					continue
				redundent.append( solvedFiles[i] )

		
		for file in redundent:
			q.put(file)

		
		"""
		#remove old files
		for file in redundent:
			fileName = STATES_FOLDER + file
			os.remove(fileName)
		"""

		time.sleep(5)

def cleanup():
	#read files names from folder
	#find all redundent files (not going to be used for inheriting by any nodes)
	#read storage file
	#add new data to old data from storage file
	#write to storage file
	#delet redundent files
	while True:
		files = os.listdir(STATES_FOLDER)
		if ".DS_Store" in files:
			files.remove(".DS_Store")

		#Keep the seed to replant if neccessary
		files.remove("2X2.json")
		#indexes should corresponnd
		solvedFiles = []
		solvedSizeOnly = []
		#each file shoud be in form of mXn.json 0 - not fully checking yet
		for file in files:
			#rudementry check for format
			#if file[1] == "X" and file[3] == ".":
			#print(file)
			charI = 0
			while file[charI] != "X":
				charI += 1
			m = int(file[:charI])
			charI2 = charI
			while file[charI2] != ".":
				charI2 += 1
			n = int(file[charI+1:charI2])

			solvedFiles.append( file )
			solvedSizeOnly.append( (m, n) )
		#print("Solved: " + str(solvedFiles))
		redundent = []
		for i in range(len(solvedFiles)):
			size = solvedSizeOnly[i]
			print(size)
			#if the next one in form mXn+1 is solved then redundent
			if ((size[0], size[1]+1) in solvedSizeOnly):
				#if needed for the m+1 square node
				if size[0] + 1 == size[1] and not ((size[0]+1, size[1]) in solvedSizeOnly):
					continue
				redundent.append( solvedFiles[i] )

		#print("redundent: " + str(redundent))
		data = util.load(DATA_FOLDER + "index.json", False)

		#means could not find file
		if type(data) == type([]):
			data = {}

		#print("DATA BITCHES")
		#print(data)
		#print("Type: " + str(type(data)))
		for file in redundent:
			fileName = STATES_FOLDER + file

			fData = util.load(fileName, False)


			#if fData == []:
				#util.store("THIS WAS DONE THROUGH CLEANUP", fileName)
			data[file] = fData
		#print("Storing")
		#print(data)
		util.store(data, DATA_FOLDER + "index.json")

		#remove old files
		for file in redundent:
			fileName = STATES_FOLDER + file
			os.remove(fileName)

		time.sleep(5)


	



	

#Creates the 2x2 solved case to act as seed for the expansion cycles
def seed():
	#Replace filler with actual data
	dataTwo = np.array(util.extendToMxN(2,2)).tolist()
	print("2data: " + str(dataTwo))
	util.store(dataTwo, DATA_FOLDER + "solved/2X2.json")
	util.store({}, DATA_FOLDER + "index.json")


if __name__ == "__main__":
	mp.set_start_method('spawn')
	seed()
	main()


	
