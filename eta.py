import util3 as util
import heritage3

#number of columns >= num of rows (because mirroring)

#for square
#G MUST BE SQUARE OR IT BREAK
def eta(g, l, n, evens):
	#print("\n\neta for g: "+str(g)+" l: "+str(l))
	#rank(g) < n-1 and file(g) < n-1
	#first part for if square
	if g[0] == len(g)  and util.rank(g) < n-1 and util.file(g) < n-1:
		#if g = correct first move for a bite
		if g[0] == n-1 and len(g) > 1 and g[1] == 1:
			#print("SQUARE bite detected for " + str(g))
			if l == (n-1, n-1):
				return 0
			elif l == (n, n-1):
				return 1
			else:
				print("This should not have happend - eta case 1")
		#bite at winning square move then calc remaining moves
		else:
			#if l doesn't extend into first col or top row
			if l[0] < n and l[1] < n:
				return 1
			#turned into a rectangle board
			#if l[1] = n then l[0] = n which isn't in L therefore this is for l[0] = n
			#l[0] = n
			else:
				#getLPrime is adding a col to the right
				#getLPrime shouldn't return a full L
				#l[1] was util.getLPrime(g)
				return etaPrime(g, l[1]-1, evens)
	else:
		#print("wants to be elsa")
		return etaPrime(g, l[1]-(n-len(g)), evens)

#for not square, only called by eta
def etaPrime(gP, lP, evens):
	#print("etaPrime gP: " + str(gP)+"\tlP: " + str(lP))
	if str(gP) in evens:
		return 1
	N = util.combineGP_LP(gP, lP)
	#print("etaPrime N: "+str(N))
	return etaGraph(N, evens)

@profile
def etaGraph(node, evens):
	"""
	get children of node,
	for child:
		if childNum is even:
			return 1
	return 0
	"""
	bites = util.getChoices(node)
	mirrors = []
	for bite in bites:
		child = util.bite(node, bite)
		if str(child) in evens:
			return 1
		else:
			mirrors.append(child)
		#elif str(util.mirror(child)) in evens:
			#return 1
	for mirror in mirrors:
		if str(util.mirror(child)) in evens:
			return 1
	return 0
