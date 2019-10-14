import multiprocessing as mp
#import etaExpansion as eE
import eta
import os
import util3 as util

def etaProcess(q, outQ):
	while True:
		if not q.empty():
			item = q.get()
			#print("item: " + str(item))
			#print(str(os.getppid()) + " processing " + str(item[0]))
			outQ.put(multiExpandProc(item))
			q.task_done()

	

class ProccesHandler:
	q = None
	outQ = None

	def __init__(self, workers=6):
		self.q = mp.JoinableQueue()
		self.outQ = mp.JoinableQueue()
		#states processes
		self.processes = [mp.Process(target=etaProcess, args=(self.q, self.outQ), daemon=True) for i in range(workers)]
		

		for p in self.processes:
			p.start()

	def add(self, item):
		self.q.put(item)




	def terminate(self):
		""" wait until queue is empty and terminate processes """ #-except don't cause queue will never empty
		#self.queue.join()

		for p in self.processes:
			p.terminate()

def multiExpandProc(item):

	G = item[0]
	n = item[1]
	etaData = item[2]
	#newGs = gInGs(G, etaData)

	

	newNodes = gInNewGs(G, n)
	sortNodes(newNodes)
	return(multiNodeInNodes(newNodes, etaData, n))
"""
def gInGs(G, etaData):
	print("gInGs G:" + str(G) + " in " + str(os.getppid()))
	newGs = []

	if (g[0], g[1]) not in newGs:
		newGs.append((g[0], g[1]))
	else:
		print("DUPLICATE G: "+str((g[0], g[1])))
	if len(g[0]) == g[0][0] and util.file(g[0]) > util.rank(g[0]):
		mir = util.mirror(g[0])
		#print("Adding a mirror: " + str(mir) + "<-")
		mirT = (mir, g[1])
		if mirT not in newGs:
			newGs.append(mirT)
		else:
			print("DUPLICATE MIR: "+str(mirT))
		etaData[str(mir)] = g[1]


	return newGs
"""
def gInNewGs(g, n):
	newNodes = []

	#print("\n\ng: " + str(g))
	L = util.getL(g[0],n)
	#print("L: " + str(L))
	for l in L:
		N = util.combineG_L(g[0] ,l)
		#print("g: " + str(g)+"\tl: "+str(l) +" => " + str(N))
		#print("N: " + str(n))
		#print(N)
		dat = [N, g[0], l, g[1]]
		# ifDat(dat, newNodes)
		# if dat not in newNodes:
		newNodes.append(dat)
		# else:
			# print("DUPLICATE!!!!!!!")
	return newNodes

def sortNodes(newNodes):
	newNodes.sort(key = lambda x: sum(x[0]))
	#print("new nodes: " + str(newNodes))

def multiNodeInNodes(newNodes, etaData, n):
	ret = []
	for node in newNodes:

		N = node[0]
		g0 = node[1]
		l = node[2]
		g1 = node[3]
		#print("eta of " + str(N))
		num = eta.eta(g0, l, g1, n, etaData)
		etaData[str(N)] = num
		ret.append((N, num))
	return ret